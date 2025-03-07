import os
import zipfile
from pathlib import Path


def advanced_batch_unzip(input_folder, output_folder=None, extract_to_subfolder=True):
    # 将输入参数统一转为 Path 对象
    input_folder = Path(input_folder)
    if output_folder is None:
        output_folder = input_folder
    else:
        output_folder = Path(output_folder)

    # 创建输出目录（如果 extract_to_subfolder 为 False）
    if not extract_to_subfolder and not output_folder.exists():
        output_folder.mkdir(parents=True)

    print(list(input_folder.glob('*.zip')))

    for zip_file in input_folder.glob('*.zip'):
        try:
            # 解压文件名（不带 .zip 后缀）
            zip_name = zip_file.stem
            if extract_to_subfolder:
                # 解压到独立子目录
                target_dir = output_folder / zip_name
                target_dir.mkdir(exist_ok=True)
                with zipfile.ZipFile(zip_file, 'r') as z:
                    z.extractall(target_dir)
                print(f"✅ {zip_file} → {target_dir}")
            else:
                # 解压到统一目录
                with zipfile.ZipFile(zip_file, 'r') as z:
                    z.extractall(output_folder)
                print(f"✅ {zip_file} → {output_folder}")
        except Exception as e:
            print(f"⚠️ {zip_file} 解压失败：{e}")


if __name__ == "__main__":
    # 使用示例（保持路径字符串格式，避免空格问题）
    input_folder_path = Path(os.path.abspath("../datasets/mld/Stratified-train-test/"))
    output_folder_path = Path(os.path.abspath("../datasets/mld/Stratified-train-test-unzip/"))

    advanced_batch_unzip(
        input_folder=input_folder_path,
        output_folder=output_folder_path,
        extract_to_subfolder=True
    )