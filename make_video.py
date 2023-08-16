import os
from skimage import io, transform, img_as_ubyte, img_as_float
from skimage.exposure import rescale_intensity
import numpy as np
import ffmpeg

# 从第0单元开始
unit = 10
id = 600

video_folder_path = f".\\final_video"
frame_path = os.path.join(video_folder_path, "frames")

def process(folder_name):
    global video_folder_path, frame_path, id

    orig_path = f".\\input\\{folder_name}\\frames"
    mask_path = f".\\output\\{folder_name}\\my_run\\MSE"

    if os.path.exists(orig_path) and os.path.exists(mask_path):
        if not os.path.exists(video_folder_path):
            os.makedirs(video_folder_path, exist_ok = True)
            os.makedirs(frame_path, exist_ok = True)
        orig_files = os.listdir(orig_path)
        mask_files = os.listdir(mask_path)

        for i in range(len(orig_files)):
            image_orig = io.imread(os.path.join(orig_path, orig_files[i]))
            image_mask_low_size = io.imread(os.path.join(mask_path, mask_files[i]))

            image_mask = transform.resize(image_mask_low_size, (image_orig.shape[0], image_orig.shape[1], 4), mode = 'symmetric')
            mask_float = img_as_float(image_mask)
            normalized_mask = rescale_intensity(mask_float, in_range='image', out_range=(0, 1))
            image_mask = img_as_ubyte(normalized_mask)

            image_res = np.zeros_like(image_orig)
                                            
            for row in range(image_orig.shape[0] - 1):
                for col in range(image_orig.shape[1]):
                    mask_intensity = image_mask[row][col][0]
                    if mask_intensity > 0:
                        intensity = int((image_orig[row][col][0] + image_orig[row][col][1] + image_orig[row][col][2])/3.0)
                        greyed_pixel = [intensity, intensity, intensity]
                        orig_pixel = image_orig[row][col]
                        if mask_intensity > 5:
                            image_res[row][col] = greyed_pixel
                        else:
                            r0 = int(greyed_pixel[0]*(mask_intensity/5) + orig_pixel[0]*(1-mask_intensity/5))
                            r1 = int(greyed_pixel[1]*(mask_intensity/5) + orig_pixel[1]*(1-mask_intensity/5))
                            r2 = int(greyed_pixel[2]*(mask_intensity/5) + orig_pixel[2]*(1-mask_intensity/5))
                            image_res[row][col] = [r0,r1,r2]
                    else:
                        image_res[row][col] = image_orig[row][col]
            image_save_path = os.path.join(frame_path, f"frame_{id}.jpg")
            io.imsave(image_save_path, image_res)
            id += 1

        print(f"Finish {folder_name} creation")
        return True

    else:
        return False

while True:
    # train first
    folder_name = f"unit{unit:05}_train"

    if not process(folder_name):
        break

    # test then
    folder_name = f"unit{unit:05}_test"

    if not process(folder_name):
        break

    unit += 1
    if unit == 12:
        break


video_name = f'final.mp4'
res_path = os.path.join(video_folder_path, video_name)

frame_rate = 10
codec = 'h264'

input_stream = (
    ffmpeg.input(os.path.join(frame_path, 'frame_%d.jpg'), framerate=frame_rate)  # 输入图像序列文件名模板
        .filter('fps', fps=frame_rate, round='up')  # 设定帧率
        .output(res_path, pix_fmt='yuv420p', vcodec='libx264')  # 输出文件名和编码设置
)

# 运行编码任务
ffmpeg.run(input_stream)