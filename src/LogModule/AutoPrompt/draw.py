import matplotlib.pyplot as plt
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
                      whiskerprops={'linewidth':0.5,'color': 'black'},  # 将线条变细
                      capprops={'linewidth':0.5,'color': 'black'},  # 将线条变细
                      medianprops={'linewidth':0.5,'color': 'black'},  # 将线条变细
                      boxprops={'linewidth':0.5, 'edgecolor': 'black'})  # 将线条变细且边缘为黑色

    # 设置颜色
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)

    # 设置图表标题和坐标轴标签
    plt.title('指标箱体图')
    plt.xlabel('指标')
    plt.ylabel('值')

    # 显示网格
    plt.grid(True, linestyle='--', alpha=0.6)
    path = r'C:\code\src\python\autoQAG\result\plotBox.png'
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
    path = r'C:\code\src\python\autoQAG\result\plot.png'
    plt.savefig(path, dpi=300)


if __name__ == '__main__':
    data = [{'The process involves identifying key patterns in log messages, such as specific keywords or variables, '
             'and creating templates with placeholders for these elements. By matching log messages to these '
             'templates, language model assistants can accurately parse and interpret the information provided in the '
             'logs.': [0.8869047619047619, 0.883248730964467, 0.22023809523809523], 'The process of parsing log '
                                                                                    'messages into templates involves '
                                                                                    'identifying common patterns and '
                                                                                    'placeholders within the logs. By '
                                                                                    'analyzing the logs, '
                                                                                    'language model assistants can '
                                                                                    'create templates that capture '
                                                                                    'the essential information while '
                                                                                    'abstracting out specific values. '
                                                                                    'This approach helps improve the '
                                                                                    'accuracy of log template parsing '
                                                                                    'by generalizing the structure of '
                                                                                    'similar log messages.': [
        0.8511904761904762, 0.8762886597938144, 0.20833333333333334], 'The process involves identifying key patterns '
                                                                      'and placeholders in log messages, '
                                                                      'creating templates using those patterns and '
                                                                      'placeholders, and mapping the log message data '
                                                                      'to the placeholders in the templates for '
                                                                      'accurate parsing. This helps in extracting '
                                                                      'structured information from unstructured log '
                                                                      'data.': [0.8035714285714286, 0.81,
                                                                                0.20833333333333334], 'The process of '
                                                                                                      'log template '
                                                                                                      'parsing '
                                                                                                      'involves '
                                                                                                      'analyzing log '
                                                                                                      'messages to '
                                                                                                      'identify '
                                                                                                      'patterns and '
                                                                                                      'placeholders '
                                                                                                      'that can be '
                                                                                                      'generalized '
                                                                                                      'into a '
                                                                                                      'template '
                                                                                                      'format. By '
                                                                                                      'comparing log '
                                                                                                      'messages to '
                                                                                                      'existing '
                                                                                                      'templates and '
                                                                                                      'extracting '
                                                                                                      'common '
                                                                                                      'elements, '
                                                                                                      'language model '
                                                                                                      'assistants can '
                                                                                                      'improve the '
                                                                                                      'accuracy of '
                                                                                                      'parsing log '
                                                                                                      'messages and '
                                                                                                      'generating '
                                                                                                      'templates for '
                                                                                                      'future data '
                                                                                                      'processing '
                                                                                                      'tasks.': [
        0.8095238095238095, 0.8469387755102041, 0.16071428571428573], 'The process of parsing log templates involves '
                                                                      'identifying key patterns and placeholders in '
                                                                      'log messages to create a generalized template '
                                                                      'for easier parsing and analysis. By comparing '
                                                                      'log messages to existing templates, '
                                                                      'language model assistants can improve accuracy '
                                                                      'in extracting relevant information from logs. '
                                                                      'For example, in the given logs, patterns like '
                                                                      '"<START>registerCallback not in UI.<START>" '
                                                                      'and "<START>visible is system.message.count gt '
                                                                      '0<START>" can be transformed into templates '
                                                                      'like "<START>registerCallback not in '
                                                                      'UI.<START>" and "<START>visible is <*> gt '
                                                                      '<*><START>" respectively, allowing for '
                                                                      'consistent and efficient log parsing.': [
        0.7857142857142857, 0.8140703517587939, 0.21428571428571427]}, {'The process involves identifying key '
                                                                        'patterns in log messages, such as specific '
                                                                        'keywords or variables, and creating '
                                                                        'templates with placeholders for these '
                                                                        'elements. By matching log messages to these '
                                                                        'templates, language model assistants can '
                                                                        'accurately parse and interpret the '
                                                                        'information provided in the logs.': [
        0.9166666666666666, 0.9222797927461139, 0.22023809523809523], 'The process of parsing log templates involves '
                                                                      'identifying key patterns and placeholders in '
                                                                      'log messages to create a generalized template '
                                                                      'for easier parsing and analysis. By comparing '
                                                                      'log messages to existing templates, '
                                                                      'language model assistants can improve accuracy '
                                                                      'in extracting relevant information from logs. '
                                                                      'For example, in the given logs, patterns like '
                                                                      '"<START>registerCallback not in UI.<START>" '
                                                                      'and "<START>visible is system.message.count gt '
                                                                      '0<START>" can be transformed into templates '
                                                                      'like "<START>registerCallback not in '
                                                                      'UI.<START>" and "<START>visible is <*> gt '
                                                                      '<*><START>" respectively, allowing for '
                                                                      'consistent and efficient log parsing.': [
        0.8630952380952381, 0.8865979381443299, 0.20833333333333334], 'The process of parsing log messages into '
                                                                      'templates involves identifying common patterns '
                                                                      'and placeholders within the logs. By analyzing '
                                                                      'the logs, language model assistants can create '
                                                                      'templates that capture the essential '
                                                                      'information while abstracting out specific '
                                                                      'values. This approach helps improve the '
                                                                      'accuracy of log template parsing by '
                                                                      'generalizing the structure of similar log '
                                                                      'messages.': [0.8511904761904762,
                                                                                    0.8762886597938144,
                                                                                    0.20833333333333334],
                'The process of log template parsing involves analyzing log messages to identify patterns and placeholders '
                'that can be generalized into a template format. By comparing log messages to existing templates and '
                'extracting common elements, language model assistants can improve the accuracy of parsing log messages and '
                'generating templates for future data processing tasks.': [0.8333333333333334, 0.8762886597938144,
                                                                           0.16071428571428573], 'The process involves '
                                                                                                 'identifying key patterns '
                                                                                                 'and placeholders in log '
                                                                                                 'messages, '
                                                                                                 'creating templates using '
                                                                                                 'those patterns and '
                                                                                                 'placeholders, and mapping '
                                                                                                 'the log message data to the '
                                                                                                 'placeholders in the '
                                                                                                 'templates for accurate '
                                                                                                 'parsing. This helps in '
                                                                                                 'extracting structured '
                                                                                                 'information from '
                                                                                                 'unstructured log data.': [
            0.8035714285714286, 0.81, 0.20833333333333334]}, {'The process involves identifying key patterns in log '
                                                              'messages, such as specific keywords or variables, '
                                                              'and creating templates with placeholders for these '
                                                              'elements. By matching log messages to these templates, '
                                                              'language model assistants can accurately parse and '
                                                              'interpret the information provided in the logs.': [
        0.9166666666666666, 0.9222797927461139, 0.22023809523809523], 'The process of parsing log templates involves '
                                                                      'identifying key patterns and placeholders in '
                                                                      'log messages to create a generalized template '
                                                                      'for easier parsing and analysis. By comparing '
                                                                      'log messages to existing templates, '
                                                                      'language model assistants can improve accuracy '
                                                                      'in extracting relevant information from logs. '
                                                                      'For example, in the given logs, patterns like '
                                                                      '"<START>registerCallback not in UI.<START>" '
                                                                      'and "<START>visible is system.message.count gt '
                                                                      '0<START>" can be transformed into templates '
                                                                      'like "<START>registerCallback not in '
                                                                      'UI.<START>" and "<START>visible is <*> gt '
                                                                      '<*><START>" respectively, allowing for '
                                                                      'consistent and efficient log parsing.': [
        0.8630952380952381, 0.8865979381443299, 0.20833333333333334], 'The process of parsing log messages into '
                                                                      'templates involves identifying common patterns '
                                                                      'and placeholders within the logs. By analyzing '
                                                                      'the logs, language model assistants can create '
                                                                      'templates that capture the essential '
                                                                      'information while abstracting out specific '
                                                                      'values. This approach helps improve the '
                                                                      'accuracy of log template parsing by '
                                                                      'generalizing the structure of similar log '
                                                                      'messages.': [0.8511904761904762,
                                                                                    0.8762886597938144,
                                                                                    0.20833333333333334],
                'The process of log template parsing involves analyzing log messages to identify patterns and placeholders '
                'that can be generalized into a template format. By comparing log messages to existing templates and '
                'extracting common elements, language model assistants can improve the accuracy of parsing log messages and '
                'generating templates for future data processing tasks.': [0.8333333333333334, 0.8762886597938144,
                                                                           0.16071428571428573], 'The process involves '
                                                                                                 'identifying key patterns '
                                                                                                 'and placeholders in log '
                                                                                                 'messages, '
                                                                                                 'creating templates using '
                                                                                                 'those patterns and '
                                                                                                 'placeholders, and mapping '
                                                                                                 'the log message data to the '
                                                                                                 'placeholders in the '
                                                                                                 'templates for accurate '
                                                                                                 'parsing. This helps in '
                                                                                                 'extracting structured '
                                                                                                 'information from '
                                                                                                 'unstructured log data.': [
            0.8035714285714286, 0.81, 0.20833333333333334]}, {'The process involves identifying key patterns in log '
                                                              'messages, such as specific keywords or variables, '
                                                              'and creating templates with placeholders for these '
                                                              'elements. By matching log messages to these templates, '
                                                              'language model assistants can accurately parse and '
                                                              'interpret the information provided in the logs.': [
        0.9166666666666666, 0.9222797927461139, 0.22023809523809523], 'The process of parsing log templates involves '
                                                                      'identifying key patterns and placeholders in '
                                                                      'log messages to create a generalized template '
                                                                      'for easier parsing and analysis. By comparing '
                                                                      'log messages to existing templates, '
                                                                      'language model assistants can improve accuracy '
                                                                      'in extracting relevant information from logs. '
                                                                      'For example, in the given logs, patterns like '
                                                                      '"<START>registerCallback not in UI.<START>" '
                                                                      'and "<START>visible is system.message.count gt '
                                                                      '0<START>" can be transformed into templates '
                                                                      'like "<START>registerCallback not in '
                                                                      'UI.<START>" and "<START>visible is <*> gt '
                                                                      '<*><START>" respectively, allowing for '
                                                                      'consistent and efficient log parsing.': [
        0.8630952380952381, 0.8865979381443299, 0.20833333333333334], 'The process of parsing log messages into '
                                                                      'templates involves identifying common patterns '
                                                                      'and placeholders within the logs. By analyzing '
                                                                      'the logs, language model assistants can create '
                                                                      'templates that capture the essential '
                                                                      'information while abstracting out specific '
                                                                      'values. This approach helps improve the '
                                                                      'accuracy of log template parsing by '
                                                                      'generalizing the structure of similar log '
                                                                      'messages.': [0.8511904761904762,
                                                                                    0.8762886597938144,
                                                                                    0.20833333333333334],
                'The process of log template parsing involves analyzing log messages to identify patterns and placeholders '
                'that can be generalized into a template format. By comparing log messages to existing templates and '
                'extracting common elements, language model assistants can improve the accuracy of parsing log messages and '
                'generating templates for future data processing tasks.': [0.8333333333333334, 0.8762886597938144,
                                                                           0.16071428571428573], 'The process involves '
                                                                                                 'identifying key patterns '
                                                                                                 'and placeholders in log '
                                                                                                 'messages, '
                                                                                                 'creating templates using '
                                                                                                 'those patterns and '
                                                                                                 'placeholders, and mapping '
                                                                                                 'the log message data to the '
                                                                                                 'placeholders in the '
                                                                                                 'templates for accurate '
                                                                                                 'parsing. This helps in '
                                                                                                 'extracting structured '
                                                                                                 'information from '
                                                                                                 'unstructured log data.': [
            0.8035714285714286, 0.81, 0.20833333333333334]}, {'The process involves identifying key patterns in log '
                                                              'messages, such as specific keywords or variables, '
                                                              'and creating templates with placeholders for these '
                                                              'elements. By matching log messages to these templates, '
                                                              'language model assistants can accurately parse and '
                                                              'interpret the information provided in the logs.': [
        0.9166666666666666, 0.9222797927461139, 0.22023809523809523], 'The process of parsing log templates involves '
                                                                      'identifying key patterns and placeholders in '
                                                                      'log messages to create a generalized template '
                                                                      'for easier parsing and analysis. By comparing '
                                                                      'log messages to existing templates, '
                                                                      'language model assistants can improve accuracy '
                                                                      'in extracting relevant information from logs. '
                                                                      'For example, in the given logs, patterns like '
                                                                      '"<START>registerCallback not in UI.<START>" '
                                                                      'and "<START>visible is system.message.count gt '
                                                                      '0<START>" can be transformed into templates '
                                                                      'like "<START>registerCallback not in '
                                                                      'UI.<START>" and "<START>visible is <*> gt '
                                                                      '<*><START>" respectively, allowing for '
                                                                      'consistent and efficient log parsing.': [
        0.8630952380952381, 0.8865979381443299, 0.20833333333333334], 'The process of parsing log messages into '
                                                                      'templates involves identifying common patterns '
                                                                      'and placeholders within the logs. By analyzing '
                                                                      'the logs, language model assistants can create '
                                                                      'templates that capture the essential '
                                                                      'information while abstracting out specific '
                                                                      'values. This approach helps improve the '
                                                                      'accuracy of log template parsing by '
                                                                      'generalizing the structure of similar log '
                                                                      'messages.': [0.8511904761904762,
                                                                                    0.8762886597938144,
                                                                                    0.20833333333333334],
                'The process of log template parsing involves analyzing log messages to identify patterns and placeholders '
                'that can be generalized into a template format. By comparing log messages to existing templates and '
                'extracting common elements, language model assistants can improve the accuracy of parsing log messages and '
                'generating templates for future data processing tasks.': [0.8333333333333334, 0.8762886597938144,
                                                                           0.16071428571428573],
                'The process of log template '
                'parsing involves analyzing '
                'log messages to identify '
                'patterns and placeholders '
                'that can be generalized '
                'into a template format. By '
                'comparing log messages to '
                'existing templates and '
                'extracting common elements, '
                'language model assistants '
                'can enhance the precision '
                'of parsing log messages and '
                'creating templates for '
                'future data processing '
                'tasks.': [
                    0.8333333333333334, 0.8585858585858586, 0.16666666666666666]},
            {'The process involves identifying key '
             'patterns in log messages, '
             'such as specific keywords or variables, '
             'and creating templates with placeholders '
             'for these elements. By matching log '
             'messages to these templates, '
             'language model assistants can accurately '
             'parse and interpret the information '
             'provided in the logs.': [
                0.9166666666666666, 0.9222797927461139, 0.22023809523809523],
                'The process of parsing log templates involves '
                'identifying key patterns and placeholders in '
                'log messages to create a generalized template '
                'for easier parsing and analysis. By comparing '
                'log messages to existing templates, '
                'language model assistants can improve accuracy '
                'in extracting relevant information from logs. '
                'For example, in the given logs, patterns like '
                '"<START>registerCallback not in UI.<START>" '
                'and "<START>visible is system.message.count gt '
                '0<START>" can be transformed into templates '
                'like "<START>registerCallback not in '
                'UI.<START>" and "<START>visible is <*> gt '
                '<*><START>" respectively, allowing for '
                'consistent and efficient log parsing.': [
                    0.8630952380952381, 0.8865979381443299, 0.20833333333333334],
                'The process of log template parsing involves '
                'analyzing log messages to identify patterns '
                'and placeholders that can be generalized into '
                'a template format. By comparing log messages '
                'to existing templates and extracting common '
                'elements, language model assistants can '
                'enhance the precision of parsing log messages '
                'and creating templates for future data '
                'processing tasks.': [0.8809523809523809,
                                      0.9072164948453607,
                                      0.16071428571428573],
                'The process of parsing log messages into templates involves identifying common patterns and placeholders '
                'within the logs. By analyzing the logs, language model assistants can create templates that capture the '
                'essential information while abstracting out specific values. This approach helps improve the accuracy of log '
                'template parsing by generalizing the structure of similar log messages.': [0.8511904761904762,
                                                                                            0.8762886597938144,
                                                                                            0.20833333333333334],
                'The process of log template parsing involves analyzing log messages to identify patterns and placeholders '
                'that can be generalized into a template format. By comparing log messages to existing templates and '
                'extracting common elements, language model assistants can improve the accuracy of parsing log messages and '
                'generating templates for future data processing tasks.': [0.8333333333333334, 0.8762886597938144,
                                                                           0.16071428571428573]}]

    draw_plotBox(data)
    draw_plot_with_keys(data)
