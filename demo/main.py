import streamlit as st
import json
import os
import sys
import time
import numpy as np
import pandas as pd
from queue import Queue
import cv2,collections
import streamlit.components.v1 as components
sys.setrecursionlimit(1000000)

if not os.path.exists('./input_videos'):
    os.makedirs('./input_videos')

# #### change the video number to see the results on any video present in images folder
video_number = 1

# takes position(i,j), visited matrix, motion vector matrix and threshold on vector magnitude
def bfs(i, j, vis, mag, t, region):
    util = [-1, 0, 1]
    if mag[i][j] < t or vis[i][j] == True:
        return 0
    q = collections.deque()
    area = 0
    vis[i][j] = True
    q.append([i,j])
    while len(q) > 0:
        curX, curY = q.popleft()
        region[curX][curY] = 255
        area += 1
        for a in range(3):
            for b in range(3):
                x = curX + util[a]
                y = curY + util[b]
                if x >= 0 and y >= 0 and x < mag.shape[0] and y < mag.shape[1] and vis[x][y] != True:
                    vis[x][y] = True  
                    if mag[x][y] >= t:
                        q.append([x, y])
    return area

# to color different segmented objects
def color_it(img1,c):
    img=np.zeros((img1.shape[0],img1.shape[1]))
    for i in range(img1.shape[0]):
        for j in range(img1.shape[1]):
            if img1[i][j] in c:
                img[i][j]=255
    return img

# to count the area of components
def dfs(i,j,img,re,vis,c):
    if(i<0 or i>=img.shape[0] or j<0 or j>=img.shape[1] or vis[i][j]==1 or img[i][j]==0):
        return 0
    else:
        vis[i][j] = 1
        re[i][j] = c
        val = 1
        if img[i][j] != 0:
            val += dfs(i+1,j,img,re,vis,c)
            val += dfs(i-1,j,img,re,vis,c)
            val += dfs(i,j+1,img,re,vis,c)
            val += dfs(i,j-1,img,re,vis,c)
            val += dfs(i+1,j+1,img,re,vis,c)
            val += dfs(i-1,j-1,img,re,vis,c)
            val += dfs(i-1,j+1,img,re,vis,c)
            val += dfs(i+1,j-1,img,re,vis,c)
        return val

# moving object class for each moving object identified
# Stores flags to check the position of the object and the centroid
class movObj():
    def __init__(self, x, y):
        self.cx = x
        self.cy = y
        self.lin1 = False
        self.lin2 = False
        self.lout1 = False
        self.lout2 = False
        self.lastUpdate = 0

# to find the area
def count_obj(img,co=255):
    count = 1
    area = []
    re = np.zeros((img.shape[0],img.shape[1]))
    visit = np.zeros((img.shape[0],img.shape[1]))
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if visit[i][j]==0 and img[i][j]==co:
                temp=[]
                temp.append(dfs(i,j,img,re,visit,count))
                temp.append(count-1)
                area.append(temp)
                count += 1
    return area,re

# calculating centroid of image 
def centroid_bfs(img,r,c,col,vis):
    h,w = img.shape
    q = Queue()
    q.put((r,c))
    vis[r,c] = 1
    cent_x = 0
    cent_y = 0
    cnt = 0
    min_x = h+1
    min_y = w+1
    max_x = 0
    max_y = 0
    while not q.empty():
        r, c = q.get()
        min_x = min(min_x,r)
        min_y = min(min_y,c)
        max_x = max(max_x,r)
        max_y = max(max_y,c)
        cnt += 1
        cent_x += r
        cent_y += c
        if r-1>=0 and vis[r-1,c] == 0 and img[r-1,c]!=0:
            vis[r-1,c] = col
            q.put((r-1,c))
        if r+1<h and vis[r+1,c] == 0 and img[r+1,c]!=0:
            vis[r+1,c] = 1
            q.put((r+1,c))
        if c-1>=0 and vis[r,c-1] == 0 and img[r,c-1]!=0:
            vis[r,c-1] = 1
            q.put((r,c-1))
        if c+1<w and vis[r,c+1] == 0 and img[r,c+1]!=0:
            vis[r,c+1] = 1
            q.put((r,c+1))
            
    cent_x = cent_x//cnt
    cent_y = cent_y//cnt
    
    # bounding box co-ordinates are pushed in an array
    arr = [(min_x,min_y),(min_x,max_y),(max_x,min_y),(max_x,max_y)]
    
    return cent_x, cent_y, arr

def give_count():
    p = st.empty()
    # list of persons identified by algorithm
    listOfObjects = []
    final_in_count=0
    final_out_count=0
    in_count=0
    out_count=0
    in_person = 0
    out_person = 0

    # video obj for converting video to frames after 0.1 seconds
    vidObj = cv2.VideoCapture("./input_videos/" + str(video_number) + ".mp4")
    frame_count = vidObj.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = vidObj.get(cv2.CAP_PROP_FPS)
    FRAMES = int((frame_count/fps)*10)
    count = 0
    success = 1
    sec = 0
    someLineOne = 90
    someLineTwo = 150
    # st.write("Thresholds for counting people:")
    if not os.path.exists('./output_results'):
        os.makedirs('./output_results')

    if os.path.exists('./output_results/' + str(video_number) + ".txt"):
        os.remove('./output_results/' + str(video_number) + ".txt")

    while success:
        vidObj.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
        success, image = vidObj.read()
        # print("Reading a new frame: ", success)
        # if successfully got the frame
        if success == 1:
            if count == 0:
                first_frame = image 
                prev_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
            else:
                frame = image
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # motion estimation
                flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 1, 5, 2, 5, 1.1, None)
                mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
                prev_gray = gray.copy()

                # considering only vertical motion 
                vertical = mag.copy()
                for i in range(mag.shape[0]):
                    for j in range(mag.shape[1]):
                        vertical[i][j] = mag[i][j] * abs(np.sin(ang[i][j]))

                # calculating varying T (threshold for motion to be considered)
                ind = 0
                temp_array = [0]*(vertical.shape[0]*vertical.shape[1])
                for i in range(vertical.shape[0]):
                    for j in range(vertical.shape[1]):
                        temp_array[ind] = vertical[i][j]
                        ind += 1
                temp_array = np.array(temp_array)
                temp_array = np.sort(temp_array)[::-1]

                # top 5% motion values 
                percent = (5*mag.shape[0]*mag.shape[1])/100
                percent = int(percent)
                T = temp_array[percent-1]
                # if T is less than 2 we assumed that there is no considerate motion in that frame and we can neglect that frame
                if T < 2:
                    tempList = []
                    # remove objects that seem to have moved out of the frame
                    for obj in listOfObjects:
                        if obj.lastUpdate + 2  >= count:
                            tempList.append(obj)
                    listOfObjects = tempList.copy()
                    with open("./output_results/" + str(video_number) + ".txt", 'a') as file:
                        if in_person!=final_in_count:
                            final_in_count=in_person
                            st.write(f"""
                                ```
                                    Time = {round(count*0.1, 1)} In-person count changed {in_person}
                                ```
                            """)
                            # print("Time = " + str(round(count*0.1, 1)) + "  In-person count - " + str(in_person))
                        if out_person!=final_out_count:
                            final_out_count=out_person
                            st.write(f"""
                                ```
                                    Time = {round(count*0.1, 1)} Out-person count changed {out_person}
                                ```
                            """)
                            # print("Time = " + str(round(count*0.1, 1)) + "  Out-person count - " + str(out_person))
                        file.write("Time = " + str(round(count*0.1, 1)) + "  in-person count - " + str(in_person) + "    out-person count - " + str(out_person))
                        file.write('\n')
                    count += 1
                    sec += 0.1
                    continue

                # Calculating feature value M (differential matrix)
                dy, dx = np.gradient(gray)
                Ixx = dx**2
                Iyy = dy**2
                Ixy = dx*dy
                # R_score is the corner response value considering neighbourhood of 3x3
                R_score = np.array(gray.copy(),dtype=np.float64)
                for i in range(gray.shape[0]):
                    for j in range(gray.shape[1]):
                        sum_Ix = 0
                        sum_Iy = 0
                        sum_Ixy = 0
                        for k in range(-2,3):
                            for l in range(-2,3):
                                if i+k >= 0 and j+l >= 0 and i+k < gray.shape[0] and j+l < gray.shape[1]:
                                    sum_Ix += Ixx[i+k][j+l]
                                    sum_Iy += Iyy[i+k][j+l]
                                    sum_Ixy += Ixy[i+k][j+l]
                                else:
                                    sum_Ix += 0
                                    sum_Iy += 0
                                    sum_Ixy += 0
                        # determinant of Matrix M
                        det = sum_Ix*sum_Iy - sum_Ixy*sum_Ixy
                        # trace of matrix M
                        trace = sum_Ixy + sum_Ixy
                        r = det - 0.05*(trace**2)
                        R_score[i][j] = r 
                # converting R_score to 0-255
                min_val = np.min(R_score)
                R_score += (-1)*min_val
                max_val = np.max(R_score)
                R_score = (R_score/max_val)*255
                R_score = R_score.astype(int)
                
                # choosing top_features needed to be considered
                listOfFeatures = []
                listTemp = []
                for x in range(frame.shape[0]):
                    for y in range(frame.shape[1]):
                        listTemp.append([R_score[x][y], x, y])
                listTemp.sort()
                listTemp.reverse()
                # considering top total pixel/10 features for feature selection
                K = len(listTemp)//10
                for x in range(K):
                    listOfFeatures.append(listTemp[x])
                
                # region growing
                region = np.zeros((frame.shape[0], frame.shape[1]), dtype=int)
                vis = [[False for x in range(frame.shape[1])] for y in range(frame.shape[0])]
                for point in listOfFeatures:
                    if vis[point[1]][point[2]] == False:
                        area = bfs(point[1], point[2], vis, vertical, T, region)

                # component labelling
                img_gray = region.copy()

                # removing small dots using thresholding 
                area,re = count_obj(img_gray,255)
                thresh1 = 50
                ids=[]
                for i in area:
                    if i[0] > thresh1:
                        ids.append(i[1]+1)
                imgc = color_it(re,ids)
                imgc[imgc>0] = 255
                thresh2 = 5000

                # dilating using rectangular structuring element of 7x7 five times. 
                img_d=cv2.dilate(imgc,cv2.getStructuringElement(cv2.MORPH_RECT,(7,7)),iterations=5)

                # removing components that are not big enough to consider for counting
                area,re=count_obj(img_d,255)
                ids=[]
                for i in area:
                    if i[0] > thresh2:
                        ids.append(i[1]+1)
                imgc = color_it(re,ids)
                imgc[imgc>0] = 255
                thresh3 = 5000
                img_d=cv2.dilate(imgc,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9)),iterations=2)
                img_d=cv2.erode(img_d,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9)),iterations=3)
                
                # calculating centroid
                imgc = img_d.copy()
                centroid = []
                vis = np.zeros(imgc.shape)
                h, w= imgc.shape
                for i in range(h):
                    for j in range(w):
                        if imgc[i,j] == 255 and vis[i,j] == 0:
                            # the cent_x and cent_y has x,y coordinate of centroid and the array arr has
                            # the bounding box coordinate                
                            cent_x, cent_y, arr = centroid_bfs(imgc,i,j,1,vis)
                            centroid.append((cent_x,cent_y,arr))
                
                
                # counting algorithm based on bounding boxes and centroids to link the currently identified objects
                # with the ones identified in the previous frames
                for j in range(len(centroid)):
                    once = False

                    # x1, x2, y1, y2 form the bounding box
                    x1, y1 = centroid[j][2][0]
                    x1 -= 15
                    y1 -= 15
                    x2, y2 = centroid[j][2][3]
                    x2 += 15
                    y2 += 15 
                    for obj in listOfObjects:
                        # checking if previously identified objects lie within above bounding box
                        if obj.cx > x1 and obj.cx < x2 and obj.cy > y1 and obj.cy < y2 and once != True:
                            once = True
                            prevX = obj.cx
                            prevY = obj.cy

                            # update centroid of the object
                            obj.cx = centroid[j][0]
                            obj.cy = centroid[j][1]
                            obj.lastUpdate = count

                            # below set of conditions check whether the object crosses first line or second line
                            # alongwith their direction
                            if obj.lin1 == True and obj.cx >= someLineTwo and obj.lin2 == False:
                                in_person += 1
                                obj.lin2 = True
                            elif obj.lout2 == True and obj.cx <= someLineOne and obj.lout1 == False:
                                out_person += 1
                                obj.lout1 = True
                            elif obj.lin1 == False and obj.cx >= someLineOne and prevX <= someLineOne and obj.lin2 == False:
                                obj.lin1 = True
                            elif obj.lout2 == False and prevX >= someLineTwo and obj.cx <= someLineTwo and obj.lout1 == False:
                                obj.lout2 = True
                            break
                    if once == False:
                        # if the identified object is identified for the first time, then create a new object of movObj class
                        obj = movObj(centroid[j][0], centroid[j][1])
                        listOfObjects.append(obj)
                        obj.lastUpdate = count
                
                tempList = []
                # remove objects that seem to have moved out of the frame
                for obj in listOfObjects:
                    if obj.lastUpdate + 2  >= count:
                        tempList.append(obj)
                listOfObjects = tempList.copy()

                # printing the final count for the current frame
                with open("./output_results/" + str(video_number) + ".txt", 'a') as file:
                    if in_person!=final_in_count:
                            final_in_count=in_person
                            st.write(f"""
                                ```
                                    Time = {round(count*0.1, 1)} In-person count changed {in_person}
                                ```
                            """)
                            print("Time = " + str(round(count*0.1, 1)) + "  In-person count - " + str(in_person))
                    if out_person!=final_out_count:
                        final_out_count=out_person
                        st.write(f"""
                                ```
                                    Time = {round(count*0.1, 1)} Out-person count changed {out_person}
                                ```
                        """)
                        # print("Time = " + str(round(count*0.1, 1)) + "  Out-person count - " + str(out_person))
                    file.write("Time = " + str(round(count*0.1, 1)) + "  in-person count - " + str(in_person) + "    out-person count - " + str(out_person))
                    file.write('\n')
        p.write(f"Completed {count} of {FRAMES} frames")
        # st.write(f"### {count}")
        count += 1
        sec += 0.1
    p.write(f"Completed {FRAMES} of {FRAMES} frames")
    st.write(f"""Total In-person count is {in_person} and Out-person count is {out_person}""")
    return True

def no_page():
    '''
        404 page
    '''
    st.error("### Oops! 404")

def explore_page():
    '''
        Explore page
    '''
    st.write("""## Overview """)

def show_home_page():
    '''
        Home page
    '''
    st.write("## User Input")
    uploaded_file = st.file_uploader("Video", type=['mp4'], accept_multiple_files=False, key=None, help=None, on_change=None, args=None, kwargs=None)
    if uploaded_file is not None:
        with open("input_videos/1.mp4", 'wb') as f:
            f.write(uploaded_file.getbuffer())
        st.video("./input_videos/1.mp4")
    run = st.button("Count Number of People")
    if run and uploaded_file is not None:
        st.markdown("""---""")
        ss = st.empty()
        ss.write(f"### `STATUS : Counting`")
        
        # with st.spinner("Counting ..."):
        # st.write("### Counting ...")
        # if uploaded_file:
        #     st.write('## Count')
        # else:
        #     st.error("Error with the file")
        c=give_count()
        # c=True
        if c==True:
            ss.write(f"### `STATUS : Completed`")
            with open("./output_results/1.txt", 'r') as file:
                st.download_button("Download Complete log file",file, file_name="log.txt")

st.sidebar.header('Navigation')
page = st.sidebar.selectbox("Select the page you want to see", ["Home","Explore"])
st.sidebar.markdown("---")


st.title("People Counting System")
st.write("This app counts for Getting In/Out of a Bus Based on Video Processing")
if page == "Explore":
    explore_page()
elif page == "Home":
    show_home_page()
else:
    no_page()

