import subprocess
import os

# 定义要运行的.py文件路径
file_path = "src/DeepMCBM.py"

# 从第0单元开始
unit = 0
unit_name = ""

while True:
    # train first
    if unit > 1:
        break

    unit_name = f"unit{unit:05}_train"
    if not os.path.exists(os.join("input", unit_name)):
        break
    arguments = ["--dir " + unit_name]
    subprocess.run(["python", file_path] + arguments)

    # test then
    unit_name = f"unit{unit:05}_test"
    if not os.path.exists(os.join("input", unit_name)):
        break
    arguments = ["--dir " + unit_name, "--no_train_BMN", "--no_train_STN"]
    subprocess.run(["python", file_path] + arguments)

    unit += 1
