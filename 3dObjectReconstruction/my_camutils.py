import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt

def makerotation(rx,ry,rz):
    """
    Generate a rotation matrix    

    Parameters
    ----------
    rx,ry,rz : floats
        Amount to rotate around x, y and z axes in degrees

    Returns
    -------
    R : 2D numpy.array (dtype=float)
        Rotation matrix of shape (3,3)
    """
    rx_rad = np.radians(rx)
    ry_rad = np.radians(ry)
    rz_rad = np.radians(rz)
    rotx = np.array([[1,0,0],[0,np.cos(rx_rad), -np.sin(rx_rad)],[0,np.sin(rx_rad),np.cos(rx_rad)]])
    roty = np.array([[np.cos(ry_rad),0,np.sin(ry_rad)],[0,1,0],[-np.sin(ry_rad),0,np.cos(ry_rad)]])
    rotz = np.array([[np.cos(rz_rad), -np.sin(rz_rad),0],[np.sin(rz_rad),np.cos(rz_rad),0],[0,0,1]])
    return np.matmul(np.matmul(rotx,roty),rotz)
	
class Camera:
    """
    A simple data structure describing camera parameters 
    
    The parameters describing the camera
    cam.f : float   --- camera focal length (in units of pixels)
    cam.c : 2x1 vector  --- offset of principle point
    cam.R : 3x3 matrix --- camera rotation
    cam.t : 3x1 vector --- camera translation 
    
    """
    
    def __init__(self,f,c,R,t):
        self.f = f
        self.c = c
        self.R = R
        self.t = t

    def __str__(self):
        return f'Camera : \n f={self.f} \n c={self.c.T} \n R={self.R} \n t = {self.t.T}'
    
    def project(self,pts3):
        """
        Project the given 3D points in world coordinates into the specified camera    

        Parameters
        ----------
        pts3 : 2D numpy.array (dtype=float)
            Coordinates of N points stored in a array of shape (3,N)

        Returns
        -------
        pts2 : 2D numpy.array (dtype=float)
            Image coordinates of N points stored in an array of shape (2,N)

        """
        assert(pts3.shape[0]==3)
        r_inv = np.linalg.inv(self.R)
        pts2 = np.matmul(r_inv,pts3- self.t)
        pts2[0] = pts2[0]/pts2[2]
        pts2[1] = pts2[1]/pts2[2]
        pts2 =  self.f*pts2[0:2]+self.c  
        assert(pts2.shape[1]==pts3.shape[1])
        assert(pts2.shape[0]==2)  
        return pts2
 
    def update_extrinsics(self,params):
        """
        Given a vector of extrinsic parameters, update the camera
        to use the provided parameters.
  
        Parameters
        ----------
        params : 1D numpy.array of shape (6,) (dtype=float)
            Camera parameters we are optimizing over stored in a vector
            params[:3] are the rotation angles, params[3:] are the translation

        """ 
        #assuming rotation angles are in degrees
        assert(params.shape[0]==6)
        self.R = makerotation(params[0],params[1],params[2])
        self.t = np.array([[params[3]],[params[4]],[params[5]]])

def triangulate(pts2L,camL,pts2R,camR):
    """
    Triangulate the set of points seen at location pts2L / pts2R in the
    corresponding pair of cameras. Return the 3D coordinates relative
    to the global coordinate system


    Parameters
    ----------
    pts2L : 2D numpy.array (dtype=float)
        Coordinates of N points stored in a array of shape (2,N) seen from camL camera

    pts2R : 2D numpy.array (dtype=float)
        Coordinates of N points stored in a array of shape (2,N) seen from camR camera

    camL : Camera
        The first "left" camera view

    camR : Camera
        The second "right" camera view

    Returns
    -------
    pts3 : 2D numpy.array (dtype=float)
        (3,N) array containing 3D coordinates of the points in global coordinates

    """

    n = pts2L.shape[1]
    assert(pts2L.shape[0]==2)
    assert(pts2R.shape[0]==2)
    assert(n==pts2R.shape[1])
    
    b = camR.t-camL.t
    pts3 = np.zeros((3,n))
    for i in range(n):
        #find z coords for each point
        q_l = np.array([[(pts2L[0][i]-camL.c[0][0])/camL.f], [(pts2L[1][i]-camL.c[1][0])/camL.f], [1]])
        assert(q_l.shape==(3,1))
        q_r = np.array([[(pts2R[0][i]-camR.c[0][0])/camR.f], [(pts2R[1][i]-camR.c[1][0])/camR.f], [1]])
        a_l = np.matmul(camL.R,q_l)
        a_r = -1*np.matmul(camR.R,q_r)
        a = np.concatenate((a_l,a_r), axis = 1)
        z = np.linalg.lstsq(a, b)[0]
        z_l = z[0][0]
        z_r = z[1][0]
        
        p_l = z_l * q_l
        p_r = z_r * q_r
        p1 = np.matmul(camL.R,p_l)+camL.t
        p2 = np.matmul(camR.R,p_r)+camR.t
        p = .5*(p1+p2)
        pts3[:,i] = p[:,0]
    
    assert(pts3.shape[0] == 3)
    assert(pts3.shape[1] == n)

    return pts3
	
def residuals(pts3,pts2,cam,params):
    """
    Compute the difference between the projection of 3D points by the camera
    with the given parameters and the observed 2D locations

    Parameters
    ----------
    pts3 : 2D numpy.array (dtype=float)
        Coordinates of N points stored in a array of shape (3,N)

    pts2 : 2D numpy.array (dtype=float)
        Coordinates of N points stored in a array of shape (2,N)

    params : 1D numpy.array (dtype=float)
        Camera parameters we are optimizing stored in a vector of shape (6,)

    Returns
    -------
    residual : 1D numpy.array (dtype=float)
        Vector of residual 2D projection errors of size 2*N
        
    """
    cam.update_extrinsics(params)
    return (pts2 - cam.project(pts3)).flatten()
	
def calibratePose(pts3,pts2,cam,params_init):
    """
    Calibrate the provided camera by updating R,t so that pts3 projects
    as close as possible to pts2

    Parameters
    ----------
    pts3 : 2D numpy.array (dtype=float)
        Coordinates of N points stored in a array of shape (3,N)

    pts2 : 2D numpy.array (dtype=float)
        Coordinates of N points stored in a array of shape (2,N)

    cam : Camera
        Initial estimate of camera
        
    params_init : 1D numpy.array (dtype=float)
        Initial estimate of camera extrinsic parameters ()
        params[0:2] are the rotation angles, params[2:5] are the translation

    Returns
    -------
    cam : Camera
        Refined estimate of camera with updated R,t parameters
        
    """
    opt = scipy.optimize.leastsq(lambda l: residuals(pts3,pts2,cam,l),params_init)[0]
    cam.update_extrinsics(opt)
    return cam

def decode(imprefix,start,threshold):
    """
    Given a sequence of 20 images of a scene showing projected 10 bit gray code, 
    decode the binary sequence into a decimal value in (0,1023) for each pixel.
    Mark those pixels whose code is likely to be incorrect based on the user 
    provided threshold.  Images are assumed to be named "imageprefixN.png" where
    N is a 2 digit index (e.g., "img00.png,img01.png,img02.png...")
 
    Parameters
    ----------
    imprefix : str
       Image name prefix
      
    start : int
       Starting index
       
    threshold : float
       Threshold to determine if a bit is decodeable
       
    Returns
    -------
    code : 2D numpy.array (dtype=float)
        Array the same size as input images with entries in (0..1023)
        
    mask : 2D numpy.array (dtype=logical)
        Array indicating which pixels were correctly decoded based on the threshold
    
    """
    
    # we will assume a 10 bit code
    nbits = 10
    assert(-1<start<81)
    imagelist = []
    for i in range(nbits*2):
        if (i+start < 10):
            imagelist.append(imprefix+"0"+str(i+start)+".png")
        else:
            imagelist.append(imprefix+str(i+start)+".png")
    imgshape = plt.imread(imagelist[0]).shape
    mask = np.ones((imgshape[0],imgshape[1]))
    thresh = np.ones(mask.shape)*threshold
    grey_imgs = np.zeros((nbits,mask.shape[0],mask.shape[1]))
    for i in range(0,20,2):
        #using i and i+1 as pairs
        img1,img2 = plt.imread(imagelist[i]),plt.imread(imagelist[i+1])
        if(len(img1.shape)==3 and img1.shape[2]==3):
            img1 = np.dot(img1[...,:3], [.333, 0.333, 0.333])
            img2 = np.dot(img2[...,:3], [.333, 0.333, 0.333])
        grey_imgs[int(i/2)] = np.greater(img1,img2)
        mask = mask * np.greater_equal(np.abs(img1-img2),thresh)
    #convert from greycode to binary to decimal
    b_imgs = np.zeros((nbits,mask.shape[0],mask.shape[1]))
    b_imgs[0] = grey_imgs[0]
    for i in range(nbits-1):
        b_imgs[i+1] = np.logical_xor(b_imgs[i],grey_imgs[i+1])
    
    code = np.zeros(mask.shape)
    for i in range(nbits):
        code += (b_imgs[(nbits-1)-i]) * (2**i)
    
    return code,mask