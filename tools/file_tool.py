import os
import shutil


def copy_files(source_dir, destination_dir):
    shutil.copy2(source_dir, destination_dir)


# # 调用函数复制文件夹 A 中的所有文件到文件夹 B
# copy_files("path/to/folderA", "path/to/folderB")


def copy_tree(source_dir, destination_dir):
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)
    shutil.copytree(source_dir, destination_dir)


source = "/Users/gxm/workspace/editorclient/client/DigiPlayer/Builds/WebGL"
destionation = "/Users/gxm/workspace/tq-editor/src/assets/unity"
copy_tree(source, destionation)
