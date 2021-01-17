# 3dObjectReconstruction
The goal of this project is to create a pipeline which completes the reconstruction of real life objects captured only through pictures. This reconstruction is three dimensional and maintains most of the color and texture of the object. I have demonstrated the use of the pipeline with a single 3d object, named “couple” which can be seen in the examples folder.

The pipeline is as follows:


1. Calibrate intrinsic and extrinsic camera parameters ![Alt text](couple/grab_0_u/color_C0_01.png?raw=true "Title")
1. For each pair of images:
    1. Decode the images to get valid pixels (non-background pixels)
    1. Triangulate pixels to get 3d location and color
    1. Trim 3d points using bounding box
    1. Uses Delauney Triangulation to create a mesh
    ![Alt text](Examples/images/no_bb.png?raw=true "Title")
    1. Remove any triangle with an edge greater than the max edge threshold
    1. Smooth the mesh
1. Using Meshlab:
    1. Merge the meshes
    ![Alt text](Examples/images/merged_back.png?raw=true "Title")
    1. Use poisson surface reconstruction to complete and smooth the merged meshes
    ![Alt text](Examples/images/final_back.png?raw=true "Title")

To run the project on your personal machine run main.py
ex: $python main.py

External libraries used:
Numpy
Scipy
Matplotlib
Pickle
Cv2
Meshlab
calibrate.py
meshutils.py
