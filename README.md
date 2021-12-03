<!-- # People Counting System

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
* Run main.ipynb with appropriate video_number (for choosing which video to evaluate) -->




# People Counting System for Getting In/Out of a Bus Based on Video Processing

## Problem Statement
* To implement an automatic system for counting people in a video recorded by zenith camera in the bus to capture the flow bi-directionally.

## Flow Diagram
<img src="https://user-images.githubusercontent.com/56213387/144610219-a024fcce-329c-4999-a8f6-414205a09396.jpeg" width="500" height="500">

## Motion Estimation
* Calculate optical flow between adjacent frames of the video
* Used to differentiate between a moving and stationary object 
* For identifying moving people

## Feature Pixel Selection
* Selects most significant feature.​
* Differential Matrix M is calculated in Neighborhood s(p) 3x3.
* ![R](https://user-images.githubusercontent.com/56213387/144610494-d40ff7d4-77f1-4711-9290-192fc7d5fb2c.jpeg)
* Pixels with greater feature value ( R ) are likely located on the moving object.
* R = det M – k (trace M)2

## Feature Pixel Selection
![image](https://user-images.githubusercontent.com/56213387/144610831-7868b5c6-90aa-42ab-a7a4-ad977772b70a.png)

## Region Growing
* Grouping pixels of moving object using seeds from feature pixel selection. 
* Used BFS for generation components using eight connection search.
![image](https://user-images.githubusercontent.com/56213387/144610940-a1b04aa2-ef3d-4d53-a497-45548e0a81d8.png)


## Connected Component Labelling
* Used DFS to calculate area of each separated components.
* Treated components having area less than a threshold as background.
* Later collected nearby components to treat it as one object.
![image](https://user-images.githubusercontent.com/56213387/144611085-f3a2ff0d-b765-4af1-b8fe-6b2f616f420e.png)

## Bounding Box & Centroid Detection
* Used BFS to visit all co-ordinates of each connected component and took their average to find the co-ordinate of centroid. 
* Bounding Box is calculated by taking the minimum/maximum x-y coordinates for each connected component.
![image](https://user-images.githubusercontent.com/56213387/144623777-a3ad2278-ca10-42ce-a3c1-785f28dba8b6.png)

## People Counting Algoritm
![image](https://user-images.githubusercontent.com/56213387/144611397-e1d14d3f-097a-4c3a-83de-e71d556a8a45.png)


## Evaluation Metric
* We are using Accuracy as an evaluation metric to understand how better the algorithm  is performing.

![image](https://user-images.githubusercontent.com/56213387/144611546-fc7d2e67-e542-49b4-a4da-8dca12ea4be7.png)

## Results
![image](https://user-images.githubusercontent.com/56213387/144611606-c66c6608-6565-415f-9efd-3d6fd8ac76d2.png)


    



