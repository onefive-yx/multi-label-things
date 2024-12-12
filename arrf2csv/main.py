import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
from pathlib import Path


def process_xml(filename):
    """处理XML文件获取标签"""
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        # 使用列表推导式替代循环
        labels = [child.attrib['name'] for child in root if child.tag.endswith('label')]
        return labels
    except Exception as e:
        print(f"Error processing XML file: {e}")
        return []


def process_arff(filename, labels):
    """处理ARFF文件获取属性和标签数据"""
    try:
        # 一次性读取文件内容
        with open(filename, 'r') as fp:
            lines = fp.readlines()

        # 处理属性
        attributes = []
        data_start = 0
        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith('@attribute '):
                attr_name = line.split()[1]
                attributes.append(attr_name)
            elif line.startswith('@data'):
                data_start = i + 1
                break

        # 移除标签属性
        attributes = attributes[:-len(labels)]

        # 处理数据
        total_cols = len(attributes) + len(labels)
        rows = []

        for line in lines[data_start:]:
            line = line.strip()
            if not line:
                continue

            if line.startswith('{'):
                # 稀疏格式处理
                row = np.zeros(total_cols)
                elements = line.strip('{}').split(', ')
                for element in elements:
                    if element:
                        idx, val = element.split()
                        row[int(idx)] = float(val)
            else:
                # 密集格式处理
                row = np.array(line.split(','), dtype=float)

            rows.append(row)

        # 使用numpy的高效操作
        data_array = np.array(rows)

        # 创建DataFrame
        attributes_df = pd.DataFrame(data_array[:, :len(attributes)], columns=attributes)
        labels_df = pd.DataFrame(data_array[:, -len(labels):], columns=labels)

        return attributes_df, labels_df

    except Exception as e:
        print(f"Error processing ARFF file: {e}")
        return None, None


def main():
    """主函数"""
    try:
        # 使用pathlib处理路径
        base_path = Path('./arts')
        label_xml = base_path / 'Arts1.xml'
        arff_file = base_path / 'Arts1.arff'
        name = 'Arts'

        # 处理文件
        labels = process_xml(label_xml)
        if not labels:
            raise ValueError("No labels found in XML file")

        att_df, lab_df = process_arff(arff_file, labels)
        if att_df is None or lab_df is None:
            raise ValueError("Error processing ARFF file")

        # 保存结果
        att_df.to_csv(base_path / f'{name}-attributes.csv', index=False)
        lab_df.to_csv(base_path / f'{name}-labels.csv', index=False)

        print("Processing completed successfully!")

    except Exception as e:
        print(f"Error in main process: {e}")


if __name__ == '__main__':
    main()