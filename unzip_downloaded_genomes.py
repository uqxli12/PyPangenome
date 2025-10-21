#a function for unzipping the ncbi genomes
import os
import zipfile
import shutil

def extract_zip_files(target_dir, source_dir):
    """
    在home文件夹创建target_dir命名的文件夹，将source_dir文件夹内的压缩文件解压到target_dir
    
    Args:
        target_dir: 目标文件夹名称
        source_dir: 源文件夹路径，包含需要解压的文件
    """
    # 获取home目录路径
    home_dir = os.path.expanduser('~')
    
    # 在home目录创建目标文件夹
    target_path = os.path.join(home_dir, target_dir)
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    
    # 遍历源文件夹中的所有文件
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        
        # 检查是否为压缩文件
        if filename.endswith(('.zip', '.ZIP')):
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    # 解压到目标文件夹
                    zip_ref.extractall(target_path)
                print(f"成功解压文件: {filename}")
            except Exception as e:
                print(f"解压文件 {filename} 时出错: {str(e)}")