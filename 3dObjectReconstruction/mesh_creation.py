import numpy as np
import matplotlib.pyplot as plt
from my_camutils import *
import pickle
from scipy.spatial import Delaunay
import cv2

def calibrate_ex_in(pickle_f, calib1_f, calib2_f):
    fid = open(pickle_f,'rb')
    text = pickle.load(fid)
    fid.close

    cam0 = Camera(f=(text['fx']+text['fy'])/2, c=np.array([[text['cx']],[text['cy']]]),
                  t=np.array([[0,0,0]]).T, R=makerotation(0,0,0))
    cam1 = Camera(f=(text['fx']+text['fy'])/2, c=np.array([[text['cx']],[text['cy']]]),
                  t=np.array([[0,0,0]]).T, R=makerotation(0,0,0))
    # load in the left and right images and find the coordinates of
    # the chessboard corners using OpenCV
    imgL = plt.imread(calib1_f)
    ret, cornersL = cv2.findChessboardCorners(imgL, (6,8), None)
    pts2L = cornersL.squeeze().T

    imgR = plt.imread(calib2_f)
    ret, cornersR = cv2.findChessboardCorners(imgR, (6,8), None)
    pts2R = cornersR.squeeze().T

    # generate the known 3D point coordinates of points on the checkerboard in cm
    pts3 = np.zeros((3,6*8))
    yy,xx = np.meshgrid(np.arange(6),np.arange(8))
    pts3[0,:] = 2.8*xx.reshape(1,-1)
    pts3[1,:] = 2.8*yy.reshape(1,-1)

    params = np.array([1,0,0,0,0,-20])

    cam0 = calibratePose(pts3,pts2L,cam0,params)
    cam1 = calibratePose(pts3,pts2R,cam1,params)
    return (cam0,cam1)
	
def reconstruct(imprefixL,imprefixR,threshold,camL,camR, imprefix_colorL, imprefix_colorR,skip_col=False):
    """
    Simple reconstruction based on triangulating matched pairs of points
    between to view which have been encoded with a 20bit gray code.

    Parameters
    ----------
    imprefix : str
      prefix for where the images are stored

    threshold : float
      decodability threshold

    camL,camR : Camera
      camera parameters

    Returns
    -------
    pts2L,pts2R : 2D numpy.array (dtype=float)

    pts3 : 2D numpy.array (dtype=float)

    """
    
    CLh,maskLh = decode(imprefixL,0,threshold)
    CLv,maskLv = decode(imprefixL,20,threshold)
    CRh,maskRh = decode(imprefixR,0,threshold)
    CRv,maskRv = decode(imprefixR,20,threshold)
    if(not skip_col):
    #color mask
        mask_colorL = np.ones(maskLh.shape)
        img_backL = plt.imread(imprefix_colorL+"00.png")
        img_colorL = plt.imread(imprefix_colorL+"01.png")
        mask_colorL3 = np.abs(img_colorL-img_backL)>threshold
        #if one of the colors is above threshold then they a diff colors and should be mask=1, | is bitwise or
        mask_colorL = mask_colorL * (mask_colorL3[:,:,0]|mask_colorL3[:,:,1]|mask_colorL3[:,:,2])

        mask_colorR = np.ones(maskRh.shape)
        img_backR = plt.imread(imprefix_colorR+"00.png")
        img_colorR = plt.imread(imprefix_colorR+"01.png")
        mask_colorR3 = np.abs(img_colorR-img_backR)>threshold
        mask_colorR = mask_colorR * (mask_colorR3[:,:,0]|mask_colorR3[:,:,1]|mask_colorR3[:,:,2])
    else:
        #no bkground color images
        mask_colorL = np.ones(maskLh.shape)
        img_colorL = plt.imread(imprefix_colorL+"00.png")

        mask_colorR = np.ones(maskRh.shape)
        img_colorR = plt.imread(imprefix_colorR+"00.png")
        
    #end color mask

    CL = CLh + 1024*CLv
    maskL = maskLh*maskLv*mask_colorL
    CR = CRh + 1024*CRv
    maskR = maskRh*maskRv*mask_colorR

    h = CR.shape[0]
    w = CR.shape[1]

    subR = np.nonzero(maskR.flatten())
    subL = np.nonzero(maskL.flatten())

    CRgood = CR.flatten()[subR]
    CLgood = CL.flatten()[subL]

    _,submatchR,submatchL = np.intersect1d(CRgood,CLgood,return_indices=True)

    matchR = subR[0][submatchR]
    matchL = subL[0][submatchL]

    xx,yy = np.meshgrid(range(w),range(h))
    xx = np.reshape(xx,(-1,1))
    yy = np.reshape(yy,(-1,1))

    pts2R = np.concatenate((xx[matchR].T,yy[matchR].T),axis=0)
    pts2L = np.concatenate((xx[matchL].T,yy[matchL].T),axis=0)
    #rn only get colors from the left image
    #keep track of colors
    
    pts3 = triangulate(pts2L,camL,pts2R,camR)
    
    pts_color = np.zeros(pts3.shape)
    for i in range(pts2L.shape[1]):
        pts_color[:,i] = img_colorL[pts2L[1,i],pts2L[0,i]]

    return pts2L,pts2R,pts3,pts_color
	
def mesh(resultfile, folder_prefix, cam0, cam1, threshold, boxlimits, trithresh, skip_col=False):
    imprefix_color0 = folder_prefix+'/color_C0_'
    imprefix_color1 = folder_prefix+'/color_C1_'
    imprefixC0 = folder_prefix+'/frame_C0_'
    imprefixC1 = folder_prefix+'/frame_C1_'

    pts2L,pts2R,pts3,pts_color = reconstruct(imprefixC0,imprefixC1,threshold,cam0,cam1,imprefix_color0,imprefix_color1,
                                             skip_col=skip_col)


    # Mesh cleanup parameters

    # Specify limits along the x,y and z axis of a box containing the object
    # we will prune out triangulated points outside these limits

    # Specify a longest allowed edge that can appear in the mesh. Remove triangles
    # from the final mesh that have edges longer than this value

    #
    # bounding box pruning
    #

    todelete = []
    for i in range(pts3.shape[1]):
        if ((pts3[0][i] < boxlimits[0] or pts3[0][i] > boxlimits[1]  or pts3[1][i] < boxlimits[2] or pts3[1][i] > boxlimits[3] 
             or pts3[2][i] < boxlimits[4] or pts3[2][i] > boxlimits[5])):
            todelete.append(i)
    pts3d = np.delete(pts3,todelete,1)
    pts2Ld = np.delete(pts2L,todelete,1)
    pts2Rd = np.delete(pts2R,todelete,1)
    pts_colord = np.delete(pts_color,todelete,1)
    
    
    #
    # triangulate the 2D points to get the surface mesh
    #
    #make more efficient by only modifiying the one variable(worse debugging)
    delan = Delaunay(pts2Ld.T)
    tri1 = delan.simplices
    
    #
    # new triangle pruning
    #
    tria = np.sqrt(np.sum(pow(pts3d[:, tri1[:, 0]] - pts3d[:, tri1[:, 1]], 2),0))
    trib = np.sqrt(np.sum(pow(pts3d[:, tri1[:, 0]] - pts3d[:, tri1[:, 2]], 2),0))
    tric = np.sqrt(np.sum(pow(pts3d[:, tri1[:, 1]] - pts3d[:, tri1[:, 2]], 2),0))

    tri_mask = (tria < trithresh) & (trib < trithresh) & (tric < trithresh)
    
    #
    # remove any points which are not refenced in any triangle
    #
    tri = tri1[tri_mask, :]
    
    #store data in pickle file as a dict
    pts_all = {}
    pts_all["pts3"] = pts3d
    pts_all["pts2L"] = pts2Ld
    pts_all["pts2R"] = pts2Rd
    pts_all["pts_color"] = pts_colord
    pts_all["tri"] = tri
    fid = open(resultfile, "wb" ) 
    pickle.dump(pts_all,fid)
    fid.close()
    print('wrote file '+resultfile)
	
def smooth_mesh(pts3_old,tri,reps):
    #smooth the mesh reps number of times
    pts3_new = pts3_old
    for r in range(reps):
        pts3_old = pts3_new
        for i in range(tri.shape[0]):
            pts3_new[:,tri[i,0]] = (pts3_old[:,tri[i,0]] + pts3_old[:,tri[i,1]] + pts3_old[:,tri[i,2]])/3
            pts3_new[:,tri[i,1]] = (pts3_old[:,tri[i,0]] + pts3_old[:,tri[i,1]] + pts3_old[:,tri[i,2]])/3
            pts3_new[:,tri[i,2]] = (pts3_old[:,tri[i,0]] + pts3_old[:,tri[i,1]] + pts3_old[:,tri[i,2]])/3
        
    return pts3_new
