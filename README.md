# 3dObjectReconstruction
The goal of this project is to create a pipeline which completes the reconstruction of real life objects captured only through pictures. This reconstruction is three dimensional and maintains most of the color and texture of the object. I have demonstrated the use of the pipeline with a single 3d object, named “couple” which can be seen in the examples folder.

The pipeline is as follows:


Calibrate intrinsic and extrinsic camera parameters ->
For each pair of images:
  Decode the images to get valid pixels (non-background pixels) ->
  Triangulate pixels to get 3d location and color ->
  Trim 3d points using bounding box->
  Uses Delauney Triangulation to create a mesh->
  Trim any triangle with an edge greater than the max edge threshold->
  smooth the mesh->
Using Meshlab:
  Merge the meshes->
  Use poisson surface reconstruction to complete and smooth the merged meshes

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
