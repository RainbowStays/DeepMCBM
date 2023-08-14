import cv2
import os
from datetime import datetime

def save_frames(video_path, output_folder, image_size):
    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    # 打开视频文件
    video_capture = cv2.VideoCapture(video_path)

    if not video_capture.isOpened():
        print("Failed to open")
        exit()

    frame_count = 0
    unit_count = 0
    train_frame_count = 0
    test_frame_count = 0

    while True:
        success, frame = video_capture.read()

        if not success:
            break

        # 调整图像尺寸
        frame = cv2.resize(frame, image_size)

        # 60帧一个单位
        if frame_count % 60 == 0:
            unit_name = "unit" + f"{unit_count:05}"
            train_folder_name = os.path.join(output_folder, unit_name + "_train")
            os.makedirs(train_folder_name, exist_ok=True)
            sub_folder = "frames"
            train_save_path = os.path.join(train_folder_name, sub_folder)
            os.makedirs(train_save_path, exist_ok=True)
            test_folder_name = os.path.join(output_folder, unit_name + "_test")
            os.makedirs(train_folder_name, exist_ok=True)
            sub_folder = "frames"
            test_save_path = os.path.join(test_folder_name, sub_folder)
            os.makedirs(test_save_path, exist_ok=True)
            unit_count += 1
            train_frame_count = 0
            test_frame_count = 0

        # 划分前30帧和后30帧
        if train_frame_count < 30:
            output_path_parent = train_save_path
            sub_frame_count = train_frame_count
            train_frame_count += 1
        else:
            output_path_parent = test_save_path
            sub_frame_count = test_frame_count
            test_frame_count += 1

        # 保存图像
        image_name = f"frame{sub_frame_count:05}.jpg"
        output_path = os.path.join(output_path_parent, image_name)
        cv2.imwrite(output_path, frame)

        frame_count += 1

    video_capture.release()


# 输入视频文件路径和输出文件夹路径
video_path = "input.mp4"
output_folder = "input"
image_size = (640, 360)

# 处理视频并保存图像
save_frames(video_path, output_folder, image_size)