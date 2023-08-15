import subprocess
import os

# 定义要运行的.py文件路径
file_path = "src/DeepMCBM.py"

# 从第0单元开始
unit = 0

while True:
    # train first
    train_name = f"unit{unit:05}_train"
    if not os.path.exists(os.path.join("input", train_name)):
        break
    arguments = ["--dir", train_name]
    subprocess.run(["python", file_path] + arguments)

    # test then
    test_name = f"unit{unit:05}_test"
    if not os.path.exists(os.path.join("input", test_name)):
        break
    arguments = ["--dir", test_name, "--no_train_BMN", "--no_train_STN", "--BMN_ckpt", train_name + "_my_run_BMN_best.ckpt"]
    subprocess.run(["python", file_path] + arguments)

    unit += 1
