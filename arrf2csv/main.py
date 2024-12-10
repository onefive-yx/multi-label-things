import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd

def process_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    labels = []
    for child in root:
        print(child.tag[-5:])
        if child.tag[-5:] == 'label':
            labels.append(child.attrib['name'])
    print(labels)
    return labels


def process_arff(filename, labels):

    with open(filename, 'r') as fp:
        file_content = fp.readlines()

    # 处理表头
    attributes = []
    attribute_prefix_len = len('@attribute ')
    for line in file_content:
        if line.startswith('@attribute '):
            line_array = line[attribute_prefix_len:].split()
            col_name = line_array[0]
            attributes.append(col_name)
    attributes = attributes[: -1*len(labels)]
    print(attributes)

    rows = []
    data_idx = 0
    for line in file_content:
        if line.startswith('@data'):
            break
        data_idx = data_idx + 1

    for line in file_content[data_idx+1:]:
        if line.startswith('{'):
            line = line.replace('{', '').replace('}', '')
        line = line.strip()
        row = line.split(',')
        rows.append(row)

    rows = np.array(rows)
    attributes_df = pd.DataFrame(rows[:, :-1*len(labels)], columns=attributes)
    labels_df = pd.DataFrame(rows[:, -1*len(labels):], columns=labels)
    return attributes_df, labels_df

# 用于转化arff文件转化为csv文件
# 保证多标签数据集要有arff文件和xml文件
# arff文件存储属性,标签,数据
# xml文件存储标签,用于在arff文件中识别标签
if __name__ == '__main__':
    # xml文件路径
    label_xml = './nuswide-cVLADplus/nus-wide-full-cVLADplus.xml'
    # arff文件路径
    arff = './nuswide-cVLADplus/nus-wide-full-cVLADplus-test.arff'
    # 数据集名
    name = 'nuswide-cVLADplus'
    # 获取标签列表
    labels = process_xml(label_xml)
    # 获取属性集和标签集
    att_df, lab_df = process_arff(arff, labels)

    # 分布写入csv文件,便于Python/Matlab实验使用
    att_df.to_csv('./nuswide-cVLADplus/nus-wide-full-cVLADplus-test-attributes.csv', index=False)
    lab_df.to_csv('./nuswide-cVLADplus/nus-wide-full-cVLADplus-test-labels.csv', index=False)