import subprocess
import os

# 定义要运行的.py文件路径
file_path = "src/DeepMCBM.py"

# 从第40单元开始
unit = 40

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

    # delete checkpoints
    to_delete = [train_name + "_my_run_BMN_best.ckpt", train_name + "_my_run_BMN_last.ckpt", train_name + "_my_run_STN_best.ckpt", train_name + "_my_run_STN_last.ckpt"]
    try:
        for file_name in to_delete:
            os.remove(os.path.join("checkpoints", file_name))
            print(f"文件 {file_name} 已成功删除")
    except OSError as error:
        print(f"无法删除文件：{error}")

    unit += 1
