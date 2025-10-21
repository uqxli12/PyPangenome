import matplotlib.pyplot as plt
import seaborn as sns
from Bio import Phylo
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')

def generate_roary_plots(tree_file, spreadsheet_file, labels=False, format='png', skipped_columns=14):
    sns.set_style('white')  # 调用name_of_your_newick_tree_file.tree，gene_presence_absence.csv

    # 读取新ick树文件
    t = Phylo.read(tree_file, 'newick')

    # 计算最大距离
    mdist = max([t.distance(t.root, x) for x in t.get_terminals()])

    # 读取基因存在/不存在的表格文件
    roary = pd.read_csv(spreadsheet_file, low_memory=False)
    roary.set_index('Gene', inplace=True)
    roary.drop(list(roary.columns[:skipped_columns-1]), axis=1, inplace=True)

    # 替换数据
    roary.replace('.{2,100}', 1, regex=True, inplace=True)
    roary.replace(np.nan, 0, regex=True, inplace=True)

    # 按基因数量降序排序
    idx = roary.sum(axis=1).sort_values(ascending=False).index
    roary_sorted = roary.loc[idx]

    # 绘制直方图
    plt.figure(figsize=(7, 5))
    plt.hist(roary.sum(axis=1), bins=roary.shape[1], histtype="stepfilled", alpha=.7, color='#4b5cc4')
    plt.xlabel('No. of genomes')
    plt.ylabel('No. of genes')
    sns.despine(left=True, bottom=True)
    
    # 添加横轴和竖轴线
    plt.axhline(y=0, color='black', linewidth=0.5)
    plt.axvline(x=0, color='black', linewidth=0.5)
    
    plt.savefig(f'pangenome_frequency.{format}', dpi=300)
    plt.clf()

    # 转置矩阵并绘制热图
    roary_sorted = roary_sorted[[x.name for x in t.get_terminals()]]

    with sns.axes_style('whitegrid'):
        fig = plt.figure(figsize=(17, 10))

        ax1 = plt.subplot2grid((1, 40), (0, 10), colspan=30)
        a = ax1.matshow(roary_sorted.T, cmap=plt.cm.Blues, vmin=0, vmax=1, aspect='auto', interpolation='none')
        ax1.set_yticks([])
        ax1.set_xticks([])
        ax1.axis('off')

        ax = fig.add_subplot(1, 2, 1)
        try:
            ax = plt.subplot2grid((1, 40), (0, 0), colspan=10, facecolor='white')
        except AttributeError:
            ax = plt.subplot2grid((1, 40), (0, 0), colspan=10, axisbg='white')

        fig.subplots_adjust(wspace=0, hspace=0)

        ax1.set_title(f'Roary matrix ({roary.shape[0]} gene clusters)')

        if labels:
            fsize = 12 - 0.1 * roary.shape[1]
            if fsize < 7:
                fsize = 7
            with plt.rc_context({'font.size': fsize}):
                Phylo.draw(t, axes=ax, show_confidence=False, label_func=lambda x: str(x)[:10], xticks=([],), yticks=([],), ylabel=('',), xlabel=('',), xlim=(-mdist * 0.1, mdist + mdist * 0.45 - mdist * 0.001 * roary.shape[1]), axis=('off',), title=('Tree (%d strains)' % roary.shape[1],), do_show=False)
        else:
            Phylo.draw(t, axes=ax, show_confidence=False, label_func=lambda x: None, xticks=([],), yticks=([],), ylabel=('',), xlabel=('',), xlim=(-mdist * 0.1, mdist + mdist * 0.1), axis=('off',), title=('Tree (%d strains)' % roary.shape[1],), do_show=False)
        plt.savefig(f'pangenome_matrix.{format}', dpi=300)
        plt.clf()

    # 绘制饼图
    plt.figure(figsize=(10, 10))

    core = roary[(roary.sum(axis=1) >= roary.shape[1] * 0.99) & (roary.sum(axis=1) <= roary.shape[1])].shape[0]
    softcore = roary[(roary.sum(axis=1) >= roary.shape[1] * 0.95) & (roary.sum(axis=1) < roary.shape[1] * 0.99)].shape[0]
    shell = roary[(roary.sum(axis=1) >= roary.shape[1] * 0.15) & (roary.sum(axis=1) < roary.shape[1] * 0.95)].shape[0]
    cloud = roary[roary.sum(axis=1) < roary.shape[1] * 0.15].shape[0]

    total = roary.shape[0]

    # 自定义autopct函数，保留整数部分
    def my_autopct(pct):
        val = int(round(pct * total / 100.0))
        return f'{val}'

    # 使用Cell出版社色系
    cell_colors = ['#815476', '#FF4c00', '#40de5a', '#eedeb0']

    a = plt.pie([core, softcore, shell, cloud],
                labels=[
                    f'core ({roary.shape[1] * .99:.2f} <= strains <= {roary.shape[1]:.2f})',
                    f'soft-core ({roary.shape[1] * .95:.2f} <= strains < {roary.shape[1] * .99:.2f})',
                    f'shell ({roary.shape[1] * .15:.2f} <= strains < {roary.shape[1] * .95:.2f})',
                    f'cloud (strains < {roary.shape[1] * .15:.2f})'
                ],
                explode=[0.1, 0.05, 0.02, 0], radius=0.9,
                colors=cell_colors,
                autopct=my_autopct)
    plt.savefig(f'pangenome_pie.{format}', dpi=300)
    plt.clf()

# example: generate_roary_plots("/home/xiaofang/Acidithiobacillus_roary_1735133370/accessory_binary_genes.fa.newick", "/home/xiaofang/Acidithiobacillus_roary_1735133370/gene_presence_absence.csv")