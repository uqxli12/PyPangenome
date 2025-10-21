import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn3, venn3_circles

def plot_venn_diagram(file1, file2, file3, color_scheme='cell'):
    """
    绘制三个数据集的维恩图，并可以选择不同的色系。

    :param file1: 第一个数据集的CSV文件路径
    :param file2: 第二个数据集的CSV文件路径
    :param file3: 第三个数据集的CSV文件路径
    :param color_scheme: 色系选项，可选值为'cell'或'nature'
    """

    # 读取CSV文件中的gene_name列
    data_set_1 = set(pd.read_csv(file1)['Gene'])
    data_set_2 = set(pd.read_csv(file2)['Gene'])
    data_set_3 = set(pd.read_csv(file3)['Gene'])

    # 获取文件名并去掉后缀
    dataset1_name = file1.split('/')[-1].split('.')[0]
    dataset2_name = file2.split('/')[-1].split('.')[0]
    dataset3_name = file3.split('/')[-1].split('.')[0]

    # 定义标签
    labels = {'100': '', '010': '', '001': '',
              '110': '', '101': '', '011': '',
              '111': ''}

    # 创建维恩图
    venn = venn3([data_set_1, data_set_2, data_set_3], set_labels=(dataset1_name, dataset2_name, dataset3_name))

    # 设置颜色
    if color_scheme == 'cell':
        colors = {
            '100': 'skyblue',
            '010': 'lightgreen',
            '001': 'salmon',
            '110': 'lightsteelblue',
            '101': 'palegreen',
            '011': 'lightcoral',
            '111': 'lightgray'
        }
    elif color_scheme == 'nature':
        colors = {
            '100': 'mediumseagreen',
            '010': 'cornflowerblue',
            '001': 'tomato',
            '110': 'darkcyan',
            '101': 'darkgreen',
            '011': 'firebrick',
            '111': 'dimgray'
        }
    else:
        raise ValueError("Invalid color scheme. Choose either 'cell' or 'nature'.")

    for key, color in colors.items():
        if venn.get_patch_by_id(key):
            venn.get_patch_by_id(key).set_color(color)

    # 计算每个交集的大小
    subsets = (len(data_set_1 - (data_set_2 | data_set_3)),
               len(data_set_2 - (data_set_1 | data_set_3)),
               len(data_set_3 - (data_set_1 | data_set_2)),
               len(data_set_1 & data_set_2 - data_set_3),
               len(data_set_1 & data_set_3 - data_set_2),
               len(data_set_2 & data_set_3 - data_set_1),
               len(data_set_1 & data_set_2 & data_set_3))

    # 添加交集的元素个数
    for i, size in enumerate(subsets):
        if venn.get_label_by_id('100') and i == 0:
            venn.get_label_by_id('100').set_text(size)
            venn.get_label_by_id('100').set_fontsize(12)  # 增加字号
            venn.get_label_by_id('100').set_weight('bold')  # 加粗
        elif venn.get_label_by_id('010') and i == 1:
            venn.get_label_by_id('010').set_text(size)
            venn.get_label_by_id('010').set_fontsize(12)  # 增加字号
            venn.get_label_by_id('010').set_weight('bold')  # 加粗
        elif venn.get_label_by_id('001') and i == 2:
            venn.get_label_by_id('001').set_text(size)
            venn.get_label_by_id('001').set_fontsize(12)  # 增加字号
            venn.get_label_by_id('001').set_weight('bold')  # 加粗
        elif venn.get_label_by_id('110') and i == 3:
            venn.get_label_by_id('110').set_text(size)
            venn.get_label_by_id('110').set_fontsize(12)  # 增加字号
            venn.get_label_by_id('110').set_weight('bold')  # 加粗
        elif venn.get_label_by_id('101') and i == 4:
            venn.get_label_by_id('101').set_text(size)
            venn.get_label_by_id('101').set_fontsize(12)  # 增加字号
            venn.get_label_by_id('101').set_weight('bold')  # 加粗
        elif venn.get_label_by_id('011') and i == 5:
            venn.get_label_by_id('011').set_text(size)
            venn.get_label_by_id('011').set_fontsize(12)  # 增加字号
            venn.get_label_by_id('011').set_weight('bold')  # 加粗
        elif venn.get_label_by_id('111') and i == 6:
            venn.get_label_by_id('111').set_text(size)
            venn.get_label_by_id('111').set_fontsize(12)  # 增加字号
            venn.get_label_by_id('111').set_weight('bold')  # 加粗

    # 打印交集的具体元素
    intersection_12 = data_set_1.intersection(data_set_2)
    intersection_13 = data_set_1.intersection(data_set_3)
    intersection_23 = data_set_2.intersection(data_set_3)
    intersection_all = data_set_1.intersection(data_set_2).intersection(data_set_3)

    print(f"数据集1和数据集2的交集元素为: {intersection_12}")
    print(f"数据集1和数据集3的交集元素为: {intersection_13}")
    print(f"数据集2和数据集3的交集元素为: {intersection_23}")
    print(f"三个数据集的交集元素为: {intersection_all}")

    # 显示图表
    plt.title("Overlap of Three Datasets")
    plt.show()

# 示例调用
# plot_venn_diagram('dataset1.csv', 'dataset2.csv', 'dataset3.csv', color_scheme='cell')
# plot_venn_diagram('dataset1.csv', 'dataset2.csv', 'dataset3.csv', color_scheme='nature')

