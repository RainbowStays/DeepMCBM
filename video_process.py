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

        # 每50帧一个单位
        if frame_count % 50 == 0:
            unit_folder_name = "unit" + f"{unit_count:05}"
            unit_folder_path = os.path.join(output_folder, unit_folder_name)
            os.makedirs(unit_folder_path, exist_ok=True)
            unit_count += 1
            train_frame_count = 0
            test_frame_count = 0

        # 划分前20帧和后30帧
        if train_frame_count < 20:
            sub_folder = "train"
            sub_frame_count = train_frame_count
            train_frame_count += 1
        else:
            sub_folder = "test"
            sub_frame_count = test_frame_count
            test_frame_count += 1

        # 保存图像
        image_name = f"frame{sub_frame_count:05}.jpg"
        output_path = os.path.join(unit_folder_path, sub_folder, image_name)
        cv2.imwrite(output_path, frame)

        frame_count += 1

    video_capture.release()


# 输入视频文件路径和输出文件夹路径
video_path = "input.mp4"
output_folder = "videooutput"
image_size = (640, 360)

# 处理视频并保存图像
save_frames(video_path, output_folder, image_size)