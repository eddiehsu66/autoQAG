import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
import numpy as np

# 设置matplotlib的字体为支持中文的字体，例如：微软雅黑
matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
matplotlib.rcParams['font.size'] = 10
# 解决负号'-'显示为方块的问题
matplotlib.rcParams['axes.unicode_minus'] = False


def draw_plotBox(data):
    ga_values = []
    fga_values = []
    pa_values = []

    # 从data中提取每个指标的所有值
    for record in data:
        for values in record.values():
            ga_values.append(values[0])
            fga_values.append(values[1])
            pa_values.append(values[2])

    # 准备绘制箱体图的数据
    data_to_plot = [ga_values, fga_values, pa_values]

    # 创建一个图形实例
    plt.figure(figsize=(10, 6))

    # 自定义颜色，调整为浅绿色、浅黄色和浅蓝色
    colors = ['#90EE90', '#FFFFE0', '#ADD8E6']

    # 绘制箱体图
    box = plt.boxplot(data_to_plot, patch_artist=True, labels=['GA', 'FGA', 'PA'], showmeans=False,
                      showfliers=False,
                      whiskerprops={'linewidth': 0.5, 'color': 'black'},  # 将线条变细
                      capprops={'linewidth': 0.5, 'color': 'black'},  # 将线条变细
                      medianprops={'linewidth': 0.5, 'color': 'black'},  # 将线条变细
                      boxprops={'linewidth': 0.5, 'edgecolor': 'black'})  # 将线条变细且边缘为黑色

    # 设置颜色
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)

    # 设置图表标题和坐标轴标签
    plt.title('指标箱体图')
    plt.xlabel('指标')
    plt.ylabel('值')

    # 显示网格
    plt.grid(True, linestyle='--', alpha=0.6)
    path = 'C:/code/src/python/autoQAG/result/plotBox.png'
    plt.savefig(path, dpi=300)


def draw_plot_with_keys(data):
    max_pa, min_pa, avg_pa = [], [], []
    max_ga, min_ga, avg_ga = [], [], []
    max_fga, min_fga, avg_fga = [], [], []

    for i in data:
        # 初始化临时列表来存储每个指标的所有值，以便计算平均值
        temp_ga, temp_fga, temp_pa = [], [], []

        for j in i.values():
            temp_ga.append(j[0])
            temp_fga.append(j[1])
            temp_pa.append(j[2])

        # 计算最大值、最小值和平均值
        max_ga.append(max(temp_ga))
        min_ga.append(min(temp_ga))
        avg_ga.append(sum(temp_ga) / len(temp_ga))

        max_fga.append(max(temp_fga))
        min_fga.append(min(temp_fga))
        avg_fga.append(sum(temp_fga) / len(temp_fga))

        max_pa.append(max(temp_pa))
        min_pa.append(min(temp_pa))
        avg_pa.append(sum(temp_pa) / len(temp_pa))

    # 绘图
    x_indexes = range(len(data))
    plt.figure(figsize=(12, 8))

    # 绘制最大值曲线
    plt.plot(x_indexes, max_pa, color='red', label='Max PA')
    plt.plot(x_indexes, max_ga, color='green', label='Max GA')
    plt.plot(x_indexes, max_fga, color='blue', label='Max FGA')

    # 绘制最小值曲线
    plt.plot(x_indexes, min_pa, color='red', label='Min PA', linestyle=':')
    plt.plot(x_indexes, min_ga, color='green', label='Min GA', linestyle=':')
    plt.plot(x_indexes, min_fga, color='blue', label='Min FGA', linestyle=':')

    # 绘制平均值曲线
    plt.plot(x_indexes, avg_pa, color='red', label='Avg PA', linestyle='--')
    plt.plot(x_indexes, avg_ga, color='green', label='Avg GA', linestyle='--')
    plt.plot(x_indexes, avg_fga, color='blue', label='Avg FGA', linestyle='--')

    # 设置图表标题和坐标轴标签
    plt.title('指标分析')
    plt.xlabel('迭代次数')
    plt.ylabel('值')

    # 显示图例和网格
    plt.legend()
    plt.grid(True)
    path = 'C:/code/src/python/autoQAG/result/plot.png'
    plt.savefig(path, dpi=300)


def show_train_boxplot(data):

    categories = ['NLGLAP', 'NLGLAP(w/o)梯度生成', 'k=3', 'NLGLAP(w/o)梯度更新']
    indicators = ['GA', 'FGA', 'PA']

    # 创建一个图形实例
    fig, ax = plt.subplots(figsize=(10, 6))

    # 位置和宽度设置
    pos = np.array(range(len(categories)))  # 每个类别的基础位置
    width = 0.2  # 箱体图的宽度
    colors = ['#90EE90', '#FFFFE0', '#ADD8E6']

    # 绘制箱体图
    for i, category in enumerate(data):
        ga_values = []
        fga_values = []
        pa_values = []
        for j, indicator_values in enumerate(category):
            ga_values.append(indicator_values[0])
            fga_values.append(indicator_values[1])
            pa_values.append(indicator_values[2])
        for j, values in enumerate([ga_values, fga_values, pa_values]):
            if values:  # 确保指标值列表不为空
                box = plt.boxplot(values, positions=[pos[i] + j * width], widths=width, patch_artist=True,
                                  showmeans=False, showfliers=False,
                                  whiskerprops={'linewidth': 0.5, 'color': 'black'},
                                  capprops={'linewidth': 0.5, 'color': 'black'},
                                  medianprops={'linewidth': 0.5, 'color': 'black'},
                                  boxprops={'linewidth': 0.5, 'edgecolor': 'black',
                                            'facecolor': colors[j % len(colors)]})
                plt.setp(box['medians'], color='black')

    # 设置图例和x轴标签
    legend_patches = [mpatches.Patch(color=color, label=indicator) for indicator, color in zip(indicators, colors)]
    plt.legend(handles=legend_patches, loc='upper right')
    ax.set_xticks(pos + width)
    ax.set_xticklabels(categories)

    # plt.title('参数分析')
    # plt.xlabel('实验组')
    label = '评价指标'
    vertical_label = '\n'.join(label)  # 将每个字符分开并加入换行符
    plt.ylabel(vertical_label,rotation=0)

    # plt.show()
    plt.grid(True, linestyle='--', alpha=0.6)
    path = 'C:/code/src/python/autoQAG/result/trainPlotBox.png'
    plt.savefig(path, dpi=300)

def show3Line(data):
    # 提取每个指标的数据
    ga = [row[0] for row in data]
    fga = [row[1] for row in data]
    pa = [row[2] for row in data]

    # 创建折线图
    plt.figure(figsize=(10, 6))

    # 绘制每个指标的折线
    plt.plot(ga, label='GA')
    plt.plot(fga, label='FGA')
    plt.plot(pa, label='PA')

    # 添加图例
    plt.legend()

    # 添加标题和坐标轴标签
    plt.title('GA, FGA, PA 统计图')
    plt.title('指标分析')
    plt.xlabel('迭代次数')
    plt.ylabel('指标')
    # 显示图表
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()
if __name__ == '__main__':

    # data = [
    #     [
    #         [0.857734806629834,0.782222222222222,0.734806629834254],
    #         [0.87292817679558,0.784140969162995,0.722375690607734],
    #         [0.888121546961326,0.8,0.708563535911602],
    #         [0.837016574585635,0.773333333333333,0.722375690607734],
    #         [0.888121546961326,0.820276497695852,0.703038674033149]
    #     ],
    #     [
    #      [0.6546961325966851, 0.5234375, 0.6726519337016574],
    #      [0.6464088397790055, 0.5333333333333333, 0.6850828729281768],
    #      [0.68646408839779, 0.5853658536585367, 0.6823204419889503],
    #      [0.6795580110497238, 0.5853658536585367, 0.7085635359116023],
    #      [0.6408839779005525, 0.532258064516129, 0.7306629834254144]
    #     ],
    #     [
    #      [0.5089903181189488, 0.47805555555555564, 0.6196403872752421],
    #      [0.4903314917127072, 0.46426116838487976, 0.5994475138121547],
    #      [0.47513812154696133, 0.4416370106761566, 0.6049723756906077],
    #      [0.40331491712707185, 0.41851851851851853, 0.6298342541436464],
    #      [0.5041436464088398, 0.4870967741935484, 0.6243093922651933]
    #     ],
    #     [
    #         [0.5704419889502762, 0.5, 0.6519337016574586],
    #         [0.6823204419889503, 0.5680000000000001, 0.7113259668508287],
    #         [0.6878453038674033, 0.5568627450980392, 0.6560773480662984],
    #         [0.6201657458563536, 0.5138339920948617, 0.7223756906077348],
    #         [0.7044198895027625, 0.584, 0.7058011049723757]
    #     ]
    #
    # ]
    # temp = {'Based on the given examples, the process of log template parsing involves identifying key elements within a log message, such as specific strings or variable values, and converting them into a standardized template format. This can help increase the accuracy of log parsing by allowing language model assistants to recognize common patterns and structures in log messages, making it easier to extract relevant information for analysis or troubleshooting.': [0.5089903181189488, 0.36805555555555564, 0.6196403872752421], 'The process of log template parsing involves identifying common patterns in log messages and creating a template based on those patterns. For example, in the given logs, a template was created to match the error recovery message which includes block ID, pipeline information, and datanode details. Another template was created for a message regarding maximum task failures per node. By using these templates, other language model assistants can accurately parse and categorize similar log messages.': [0.4903314917127072, 0.36426116838487976, 0.5994475138121547], 'Reason for wrongResult: The model incorrectly generated additional irrelevant log entries and did not accurately parse the log content provided.\nReason for wrongResult: The model failed to properly parse and identify the specific class and event being registered in the logContent.\nReason for wrongResult: The model is attempting to parse specific fields and values from the log message without considering the overall context or structure of the log message.\nReason for wrongResult: The model repeated the same log message multiple times and included irrelevant information about starting socket readers.\nReason for wrongResult: WrongResult occurs because the model incorrectly inserted placeholders and repeated sentences throughout the logContent.\nReason for wrongResult: The model mistakenly included irrelevant information from other log messages in the output.\nReason for wrongResult: The model failed to properly parse the log content and instead generated unrelated log messages and file paths.\nReason for wrongResult: The model mistakenly tried to parse specific thread names, job IDs, and task IDs as placeholders instead of recognizing the general log message pattern.\nReason for wrongResult: The model failed to correctly parse the values for memory (8192) and vCores (32) in the logContent, resulting in placeholder characters <*> being displayed.': [0.47513812154696133, 0.3416370106761566, 0.6049723756906077], 'Log parsing involves identifying patterns within log messages and creating templates that can be used to classify and organize future log entries. By examining the structure and content of logs, language model assistants can create templates to accurately capture key information such as errors, events, or application identifiers. For example, in the given log messages, the template <START>Created MRAppMaster for application appattempt_<*> can be used to match similar log entries containing information about the creation of MRAppMasters for different application attempts. By using templates derived from example log messages, language model assistants can improve the accuracy of log parsing and provide more precise and relevant assistance to users.': [0.40331491712707185, 0.31851851851851853, 0.6298342541436464], 'Extract one log template, substitute variable tokens in the log as <*> between <START> and <END> tags.': [0.5041436464088398, 0.3870967741935484, 0.6243093922651933]}
    #
    # res = []
    # for value in temp.values():
    #     res.append(value)
    # print(res)
    data = [
        [0.76,0.73,0.67],
        [0.79,0.74,0.71],
        [0.845,0.83,0.73],
        [0.88,0.815,0.73],
        [0.87,0.82,0.728],
        [0.9,0.83,0.76]
    ]
    # show_train_boxplot(data)
    show3Line(data)