# cv_kopernikus

This repository contains the code for cleaning Image data using Computer vision techniques. The rmv_similar_img.py was implemented by me and the other code imaging_interview.py is an intellectual property of Kopernikus Automotive GmbH.

## Running the Python file: 
1. Clone the repository cv_kopernikus.
2. Download the dataset into the repository file.
3. Create a virtual environment having packages OpenCV, imutils installed.
4. Run the file imaging_dataset.py as below

   `python rmv_similar_img.py -p path_to_images`

## Q & A:
##### 1. What did you learn after looking on our dataset?
A. The image dataset is recorded in parking garages. They are recording from different cameras "c10", "c20", "c21" and "c23". As there are not a lot of moving cars or people in the parking area frequently, there are a lot of static images which are redundant.

##### 2. How does your program work?
A. The program has two main functionalities:
i) Access all images according to the camera id and compare only those images from respective cameras in pairs so as to remove the duplicate images.
ii) Preprocessing the image pairs and comparing those frames to detect the changes.

##### 3. What values did you decide to use input parameters and how did you find these values?
A. There are two input parameters to the function `remove_similar_images()`. One is the path to the dataset and the other is the threshold value. The values were chosen by running multiple experimental trials.

`threshold`: Those images which were similar, have a 'score' from the `compare_frames_change_detection()` function to be zero. And some in the range of 100-500.  Images that were completely apart had a 'score' of a few thousand.
`camera_ids`: Camera ids for which the images are to be compared. If not given, all the cameras are considered.
`min_contour_area`: Those many numbers of pixel groups were considered to detect a change.

##### 4. What you would suggest to implement to improve the data collection of unique cases in the future?
A. A good solution would be to record those scenes when there is movement detected between two frames. Algorithms like optical flow and object tracking could be used.

##### 5. Any comments about your solution?
A. It is observed that there are not a lot of duplicates in cameras "c20" and "c23" and hence comparison consumed a lot of time. Instead, deep learning methods could be used to extract features from the images and compare them. Errors due to manual tuning like thresholding could be avoided as features would be separable in higher dimensional space.


Thank you *Kopernikus Automotive GmbH* team for this opportunity to present myself.


##### After commit changes (after sending mail):
1. Added input parameters `camera_ids` and `min_contour_area`.
2. Tested with Gaussian blur having kernels 3 & 5. Filtered 487 images instead of 377 as before.
