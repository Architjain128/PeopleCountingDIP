


# People Counting System for Getting In/Out of a Bus Based on Video Processing

## Problem Statement
* To implement an automatic system for counting people in a video recorded by zenith camera in the bus to capture the flow bi-directionally.

## Flow Diagram
<img src="https://user-images.githubusercontent.com/56213387/144610219-a024fcce-329c-4999-a8f6-414205a09396.jpeg" width="600" height="300">

## Motion Estimation
* Calculate optical flow between adjacent frames of the video
* Used to differentiate between a moving and stationary object 
* For identifying moving people

## Feature Pixel Selection
* Selects most significant feature.​
* Differential Matrix M is calculated in Neighborhood s(p) 3x3.
* <img src="https://user-images.githubusercontent.com/56213387/144610494-d40ff7d4-77f1-4711-9290-192fc7d5fb2c.jpeg" width="600" height="300">
* Pixels with greater feature value ( R ) are likely located on the moving object.
* R = det M – k (trace M)2

## Feature Pixel Selection
<img src="https://user-images.githubusercontent.com/56213387/144610831-7868b5c6-90aa-42ab-a7a4-ad977772b70a.png" width="600" height="300">

## Region Growing
* Grouping pixels of moving object using seeds from feature pixel selection. 
* Used BFS for generation components using eight connection search.
* <img src="https://user-images.githubusercontent.com/56213387/144610940-a1b04aa2-ef3d-4d53-a497-45548e0a81d8.png" width="600" height="300">


## Connected Component Labelling
* Used DFS to calculate area of each separated components.
* Treated components having area less than a threshold as background.
* Later collected nearby components to treat it as one object.
<img src="https://user-images.githubusercontent.com/56213387/144611085-f3a2ff0d-b765-4af1-b8fe-6b2f616f420e.png" width="600" height="300">


## Bounding Box & Centroid Detection
* Used BFS to visit all co-ordinates of each connected component and took their average to find the co-ordinate of centroid. 
* Bounding Box is calculated by taking the minimum/maximum x-y coordinates for each connected component.
<img src="https://user-images.githubusercontent.com/56213387/144623777-a3ad2278-ca10-42ce-a3c1-785f28dba8b6.png" width="600" height="300">

## People Counting Algoritm
<img src="https://user-images.githubusercontent.com/56213387/144611397-e1d14d3f-097a-4c3a-83de-e71d556a8a45.png" width="600" height="300">

## Evaluation Metric
* We are using Accuracy as an evaluation metric to understand how better the algorithm  is performing.

![image](https://user-images.githubusercontent.com/56213387/144625790-3d2e159e-b722-427e-81b2-edb80b2e4b61.png)


## Results
<img src="https://user-images.githubusercontent.com/56213387/144611606-c66c6608-6565-415f-9efd-3d6fd8ac76d2.png" width="600" height="300">


    



