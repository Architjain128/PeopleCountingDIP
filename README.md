# People Counting System

## File Structure
+ **src** will contain `main.ipynb` file that contains all the code for running the system.
+ **input_videos** will contain videos as `video1.avi`, `video2.avi` ..
+ **output_results** will contain results for all the videos as `result1.txt`, `result2.txt` ..
+ **requirements.txt** will contain the libraries required to run the code
+ [Link to dataset](https://iiitaphyd-my.sharepoint.com/:f:/g/personal/pulkit_g_students_iiit_ac_in/EvUJck1YpaREi6VRmrQZhX0Bde9a8aeW2JOR8MVyl1P3Sw?e=t5E7Ur), It will contains two folder one is input_videos (that will contain all the videos tested) and other is output_results (that store the result for each video)
+ Final Tree structure for files should look like this
    - dip-project-evil_morty
        - src
            - main.ipynb
        - input_videos
            - video1.avi
            - video2.avi
            - ..
        - output_results
            - result1.txt
            - result2.txt
            - ..      


### How to run
* Install appropriate package for running python notebook (ipykernel or jupyter)
* Install the following packages using pip or conda:
     + opencv-python
     + numpy
     + queue
* Run main.ipynb with appropriate video_number (for choosing which video to evaluate)

##### Shortcut
* Just clone this repo, open a terminal shell inside the repo and run the following commands
```
pip3 install -r requirements.txt
```
* Run main.ipynb with appropriate video_number (for choosing which video to evaluate)






# People Counting System for Getting In/Out of a Bus Based on Video Processing

## Problem Statement
* To implement an automatic system for counting people in a video recorded by zenith camera in the bus to capture the flow bi-directionally.

## Flow Diagram
![flow_diagram](https://user-images.githubusercontent.com/56213387/144610219-a024fcce-329c-4999-a8f6-414205a09396.jpeg)

## Motion Estimation
* Calculate optical flow between adjacent frames of the video
* Used to differentiate between a moving and stationary object 
* For identifying moving people

## Feature Pixel Selection
* Selects most significant feature.​
* Differential Matrix M is calculated in Neighborhood s(p) 3x3.​
* Pixels with greater feature value ( R ) are likely located on the moving object.​
 
* R = det M – k (trace M)2​


