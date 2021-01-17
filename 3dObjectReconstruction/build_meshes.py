import numpy as np
import pickle
from meshutils import writeply
from mesh_creation import *

def get_calib_cams():
	return calibrate_ex_in('calibration.pickle', 'calib_jpg_u/frame_C0_01.jpg', 'calib_jpg_u/frame_C1_01.jpg')

def build_all_couple():
	#calibrate cameras
	(cam0,cam1) = calibrate_ex_in('calibration.pickle', 'calib_jpg_u/frame_C0_01.jpg', 'calib_jpg_u/frame_C1_01.jpg')
	#builds all couple scans
	#write file for grab 0 couple ***************************************************************
	#good params
	thresh = .02
	box_lim = np.array([-0,20,-100,22,-35,-6])
	trithresh = 4
	resultfile = 'couple/grab_0.pickle'
	dir_pref = 'couple/grab_0_u'
	mesh(resultfile,dir_pref,cam0, cam1, thresh,box_lim,trithresh)
	#read pickle file,smooth, and write ply file for grab 0
	open_f = 'couple/grab_0.pickle'
	save_f = 'couple/grab_0_mesh_smoothed_good.ply'
	fid = open(open_f,'rb')
	text = pickle.load(fid)
	fid.close
	pts3 = text['pts3']
	pts_color = text['pts_color']
	tri = text['tri']
	pts2L = text['pts2L']
	pts2R = text['pts2R']
	pts3 = smooth_mesh(pts3, tri, 3)
	writeply(pts3,pts_color,tri,save_f)
	print("wrote file "+save_f)
	#write file for grab 1 couple ***************************************************************
	#good params
	thresh = .02
	#box_lim = np.array([0,20,-100,23,-26,-5])
	box_lim = np.array([3,15,-100,22,-30,-6])
	trithresh = 4
	resultfile = 'couple/grab_1.pickle'
	dir_pref = 'couple/grab_1_u'
	mesh(resultfile,dir_pref,cam0, cam1, thresh,box_lim,trithresh)
	#read pickle file,smooth, and write ply file for grab 1
	open_f = 'couple/grab_1.pickle'
	save_f = 'couple/grab_1_mesh_smoothed_good.ply'
	fid = open(open_f,'rb')
	text = pickle.load(fid)
	fid.close
	pts3 = text['pts3']
	pts_color = text['pts_color']
	tri = text['tri']
	pts2L = text['pts2L']
	pts2R = text['pts2R']
	pts3 = smooth_mesh(pts3, tri, 2)
	writeply(pts3,pts_color,tri,save_f)
	print("wrote file "+save_f)
	#write file for grab 2 couple ***************************************************************
	#good params
	thresh = .02
	box_lim = np.array([-0,20,-100,22,-35,-6])
	trithresh = 6
	resultfile = 'couple/grab_2.pickle'
	dir_pref = 'couple/grab_2_u'
	mesh(resultfile,dir_pref,cam0, cam1, thresh,box_lim,trithresh)
	#read pickle file,smooth, and write ply file for grab 2
	open_f = 'couple/grab_2.pickle'
	save_f = 'couple/grab_2_mesh_smoothed_good.ply'
	fid = open(open_f,'rb')
	text = pickle.load(fid)
	fid.close
	pts3 = text['pts3']
	pts_color = text['pts_color']
	tri = text['tri']
	pts2L = text['pts2L']
	pts2R = text['pts2R']
	pts3 = smooth_mesh(pts3, tri, 2)
	writeply(pts3,pts_color,tri,save_f)
	print("wrote file "+save_f)
	#write file for grab 3 couple ***************************************************************
	#good params
	thresh = .02
	box_lim = np.array([-0,20,-100,22,-35,-6])
	trithresh = 6
	resultfile = 'couple/grab_3.pickle'
	dir_pref = 'couple/grab_3_u'
	mesh(resultfile,dir_pref,cam0, cam1, thresh,box_lim,trithresh)
	#read pickle file,smooth, and write ply file for grab 3
	open_f = 'couple/grab_3.pickle'
	save_f = 'couple/grab_3_mesh_smoothed_good.ply'
	fid = open(open_f,'rb')
	text = pickle.load(fid)
	fid.close
	pts3 = text['pts3']
	pts_color = text['pts_color']
	tri = text['tri']
	pts2L = text['pts2L']
	pts2R = text['pts2R']
	pts3 = smooth_mesh(pts3, tri, 2)
	writeply(pts3,pts_color,tri,save_f)
	print("wrote file "+save_f)
	#write file for grab 4 couple ***************************************************************
	#good params
	thresh = .02
	box_lim = np.array([-0,20,-100,22,-35,-6])
	trithresh = 6
	resultfile = 'couple/grab_4.pickle'
	dir_pref = 'couple/grab_4_u'
	mesh(resultfile,dir_pref,cam0, cam1, thresh,box_lim,trithresh)
	#read pickle file,smooth, and write ply file for grab 4
	open_f = 'couple/grab_4.pickle'
	save_f = 'couple/grab_4_mesh_smoothed_good.ply'
	fid = open(open_f,'rb')
	text = pickle.load(fid)
	fid.close
	pts3 = text['pts3']
	pts_color = text['pts_color']
	tri = text['tri']
	pts2L = text['pts2L']
	pts2R = text['pts2R']
	pts3 = smooth_mesh(pts3, tri, 2)
	writeply(pts3,pts_color,tri,save_f)
	print("wrote file "+save_f)
	#write file for grab 5 couple ***************************************************************
	#good params
	thresh = .02
	box_lim = np.array([-0,20,-100,22,-35,-6])
	trithresh = 5
	resultfile = 'couple/grab_5.pickle'
	dir_pref = 'couple/grab_5_u'
	mesh(resultfile,dir_pref,cam0, cam1, thresh,box_lim,trithresh, skip_col=True)
	#read pickle file,smooth, and write ply file for grab 5
	open_f = 'couple/grab_5.pickle'
	save_f = 'couple/grab_5_mesh_smoothed_good.ply'
	fid = open(open_f,'rb')
	text = pickle.load(fid)
	fid.close
	pts3 = text['pts3']
	pts_color = text['pts_color']
	tri = text['tri']
	pts2L = text['pts2L']
	pts2R = text['pts2R']
	pts3 = smooth_mesh(pts3, tri, 2)
	writeply(pts3,pts_color,tri,save_f)
	print("wrote file "+save_f)
	#write file for grab 6 couple ***************************************************************
	#good params
	thresh = .02
	box_lim = np.array([-5,20,-100,21,-25,-4])
	trithresh = 3.5
	resultfile = 'couple/grab_6.pickle'
	dir_pref = 'couple/grab_6_u'
	mesh(resultfile,dir_pref,cam0, cam1, thresh,box_lim,trithresh)
	#read pickle file,smooth, and write ply file for grab 6
	open_f = 'couple/grab_6.pickle'
	save_f = 'couple/grab_6_mesh_smoothed_good.ply'
	fid = open(open_f,'rb')
	text = pickle.load(fid)
	fid.close
	pts3 = text['pts3']
	pts_color = text['pts_color']
	tri = text['tri']
	pts2L = text['pts2L']
	pts2R = text['pts2R']
	pts3 = smooth_mesh(pts3, tri, 2)
	writeply(pts3,pts_color,tri,save_f)
	print("wrote file "+save_f)

def build_all_teapot():
	#calibrate cameras
	(cam0,cam1) = calibrate_ex_in('calibration.pickle', 'calib_jpg_u/frame_C0_01.jpg', 'calib_jpg_u/frame_C1_01.jpg')
	#builds all teapot scans
	#write file for grab 0
	#good params
	thresh = .04
	box_lim = np.array([-3,19,-4,18,10,35]) # for teapot
	trithresh = 3.7
	resultfile = 'teapot/grab_0.pickle'
	dir_pref = 'teapot/grab_0_u'
	mesh(resultfile,dir_pref,cam0, cam1, thresh,box_lim,trithresh)
	#read pickle file,smooth, and write ply file for grab 0
	open_f = 'teapot/grab_0.pickle'
	save_f = 'teapot/grab_0_mesh_smoothed.ply'
	fid = open(open_f,'rb')
	text = pickle.load(fid)
	fid.close
	pts3 = text['pts3']
	pts_color = text['pts_color']
	tri = text['tri']
	pts2L = text['pts2L']
	pts2R = text['pts2R']
	pts3 = smooth_mesh(pts3, tri, 3)
	writeply(pts3,pts_color,tri,save_f)
	print("wrote file "+save_f)
	#write file for grab 1
	#good params
	thresh = .04
	box_lim = np.array([0,15,0,18,15,28])
	trithresh = 3.5
	resultfile = 'teapot/grab_1.pickle'
	dir_pref = 'teapot/grab_1_u'
	mesh(resultfile,dir_pref,cam0, cam1, thresh,box_lim,trithresh)
	#read pickle file,smooth, and write ply file for grab 1
	open_f = 'teapot/grab_1.pickle'
	save_f = 'teapot/grab_1_mesh_smoothed.ply'
	fid = open(open_f,'rb')
	text = pickle.load(fid)
	fid.close
	pts3 = text['pts3']
	pts_color = text['pts_color']
	tri = text['tri']
	pts2L = text['pts2L']
	pts2R = text['pts2R']
	pts3 = smooth_mesh(pts3, tri, 1)
	writeply(pts3,pts_color,tri,save_f)
	print("wrote file "+save_f)
	#write file for grab 2
	#good params
	thresh = .04
	box_lim = np.array([-3,19,-4,18,10,35]) # for teapot
	trithresh = 3
	resultfile = 'teapot/grab_2.pickle'
	dir_pref = 'teapot/grab_2_u'
	mesh(resultfile,dir_pref,cam0, cam1, thresh,box_lim,trithresh)
	#read pickle file,smooth, and write ply file for grab 2
	open_f = 'teapot/grab_2.pickle'
	save_f = 'teapot/grab_2_mesh_smoothed.ply'
	fid = open(open_f,'rb')
	text = pickle.load(fid)
	fid.close
	pts3 = text['pts3']
	pts_color = text['pts_color']
	tri = text['tri']
	pts2L = text['pts2L']
	pts2R = text['pts2R']
	pts3 = smooth_mesh(pts3, tri, 3)
	writeply(pts3,pts_color,tri,save_f)
	print("wrote file "+save_f)
	#write file for grab 3
	#good params, still have little artifact in bottom right corner
	thresh = .04
	box_lim = np.array([-5,20,-5,20,10,35])
	trithresh = 4
	resultfile = 'teapot/grab_3.pickle'
	dir_pref = 'teapot/grab_3_u'
	mesh(resultfile,dir_pref,cam0, cam1, thresh,box_lim,trithresh)
	#read pickle file,smooth, and write ply file for grab 3
	open_f = 'teapot/grab_3.pickle'
	save_f = 'teapot/grab_3_mesh_smoothed.ply'
	fid = open(open_f,'rb')
	text = pickle.load(fid)
	fid.close
	pts3 = text['pts3']
	pts_color = text['pts_color']
	tri = text['tri']
	pts2L = text['pts2L']
	pts2R = text['pts2R']
	pts3 = smooth_mesh(pts3, tri, 1)
	writeply(pts3,pts_color,tri,save_f)
	print("wrote file "+save_f)
	#write file for grab 4
	#good params
	thresh = .04
	box_lim = np.array([-5,30,-4,20,15,30])
	trithresh = 3.4
	resultfile = 'teapot/grab_4.pickle'
	dir_pref = 'teapot/grab_4_u'
	mesh(resultfile,dir_pref,cam0, cam1, thresh,box_lim,trithresh)
	#read pickle file,smooth, and write ply file for grab 4
	open_f = 'teapot/grab_4.pickle'
	save_f = 'teapot/grab_4_mesh_smoothed.ply'
	fid = open(open_f,'rb')
	text = pickle.load(fid)
	fid.close
	pts3 = text['pts3']
	pts_color = text['pts_color']
	tri = text['tri']
	pts2L = text['pts2L']
	pts2R = text['pts2R']
	pts3 = smooth_mesh(pts3, tri, 0)
	writeply(pts3,pts_color,tri,save_f)
	print("wrote file "+save_f)
	#write file for grab 5
	thresh = .04
	box_lim = np.array([-5,20,-5,20,10,35])
	trithresh = 3.4
	resultfile = 'teapot/grab_5.pickle'
	dir_pref = 'teapot/grab_5_u'
	mesh(resultfile,dir_pref,cam0, cam1, thresh,box_lim,trithresh)
	#read pickle file,smooth, and write ply file for grab 5
	open_f = 'teapot/grab_5.pickle'
	save_f = 'teapot/grab_5_mesh_smoothed.ply'
	fid = open(open_f,'rb')
	text = pickle.load(fid)
	fid.close
	pts3 = text['pts3']
	pts_color = text['pts_color']
	tri = text['tri']
	pts2L = text['pts2L']
	pts2R = text['pts2R']
	pts3 = smooth_mesh(pts3, tri, 1)
	writeply(pts3,pts_color,tri,save_f)
	print("wrote file "+save_f)
	#write file for grab 6
	thresh = .04
	box_lim = np.array([-5,20,-5,20,10,35])
	trithresh = 7
	resultfile = 'teapot/grab_6.pickle'
	dir_pref = 'teapot/grab_6_u'
	mesh(resultfile,dir_pref,cam0, cam1, thresh,box_lim,trithresh)
	#read pickle file,smooth, and write ply file for grab 6
	open_f = 'teapot/grab_6.pickle'
	save_f = 'teapot/grab_6_mesh_smoothed.ply'
	fid = open(open_f,'rb')
	text = pickle.load(fid)
	fid.close
	pts3 = text['pts3']
	pts_color = text['pts_color']
	tri = text['tri']
	pts2L = text['pts2L']
	pts2R = text['pts2R']
	pts3 = smooth_mesh(pts3, tri, 0)
	writeply(pts3,pts_color,tri,save_f)
	print("wrote file "+save_f)
