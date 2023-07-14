import cv2
import os
from imaging_interview import preprocess_image_change_detection, compare_frames_change_detection
import argparse
from typing import List
from tqdm import tqdm

ap = argparse.ArgumentParser()
ap.add_argument("-p",
                type=str,
                required=True,
                help="Path to images")

FLAGS = ap.parse_args()

def imgs_dict_on_cam_id(cam_ids: List[str], img_list: List[str]) -> dict:
    """
    Create dictionary of images based on camera id. Helps in comparing images from same camera.
    :param cam_ids: List of camera ids
    :param img_list: Image list containing all image paths
    :return: Image dictionary
    """
    img_dict = {}
    for image_file in img_list:
        for cam_id in cam_ids:
            if cam_id in image_file:
                if cam_id not in img_dict:
                    img_dict[cam_id] = []
                img_dict[cam_id].append(image_file)

    return img_dict

def standardize_image(image, cam_id):
    """
    Standardize image size
    :param image: Image to be standardized
    :param cam_id: Camera id of the image
    :return: Standardized image
    """
    if cam_id == "c10":
        image = cv2.resize(image, (640, 480))
    else:
        # image = cv2.resize(image, (1920, 1080)) # Aspect ratio to be maintained
        image = cv2.resize(image, (640, 480)) # Smaller image size for faster processing and similar image detection
    return image

def remove_similar_images(args, threshhold):
    """
    Remove similar images from path
    :param path (str): Path containing images
    :param threshhold (float): Threshhold for image similarity
    :return: None
    """
    camera_ids = ["c10", "c20", "c21", "c23"]
    image_list = os.listdir(args)
    image_list = [os.path.join(args, image) for image in image_list]

    image_dict = imgs_dict_on_cam_id(camera_ids, image_list)

    for cam_id, image_list in image_dict.items():
        # # Compare frames
        for i in tqdm(range(1, len(image_list))):
            # TODO: Increase the speed by only comparing images within limited time frame
            prev_frame = cv2.imread(image_list[i])
            prev_file = image_list[i]

            prev_frame = standardize_image(prev_frame, cam_id)
            for j in range(i + 1, len(image_list)):
                next_frame = cv2.imread(image_list[j])
                next_file = image_list[j]

                if next_frame is not None and prev_frame is not None:
                    next_frame = standardize_image(next_frame, cam_id)
                    prev_frame_processed = preprocess_image_change_detection(prev_frame)
                    next_frame_processed = preprocess_image_change_detection(next_frame)
                    score, res_cnts, thresh = compare_frames_change_detection(prev_frame_processed, next_frame_processed, 1)

                # if score > threshhold:
                #     os.remove(image_list[j])
                # print("end")

    # REMOVED CODE BELOW, Implemented a faster version above
    # Compare frames
    # for i in range(0, len(image_list)):
    #     prev_frame = cv2.imread(image_list[i])
    #     prev_name = image_list[i].split(sep='\\')[-1]
    #     prev_cam_id = re.split(r'-|_', prev_name)[0]
    #
    #     if prev_cam_id == "c10":
    #         prev_frame = cv2.resize(prev_frame, (640, 480))
    #     else:
    #         prev_frame = cv2.resize(prev_frame, (1920, 1080))
    #
    #     for j in range(i + 1, len(image_list)):
    #         next_frame = cv2.imread(image_list[j])
    #         next_name = image_list[j].split(sep='\\')[-1]
    #         next_cam_id = re.split(r'-|_', next_name)[0]
    #
    #         if next_cam_id == "c10":
    #             next_frame = cv2.resize(next_frame, (640, 480))
    #         else:
    #             next_frame = cv2.resize(next_frame, (1920, 1080))
    #
    #         if prev_cam_id == next_cam_id:
    #             prev_frame_processed = preprocess_image_change_detection(prev_frame)
    #             next_frame_processed = preprocess_image_change_detection(next_frame)
    #             score, res_cnts, thresh = compare_frames_change_detection(prev_frame_processed, next_frame_processed, 1000)
    #
    #             print("end")

if __name__ == '__main__':
    remove_similar_images(FLAGS.p, 0.5)