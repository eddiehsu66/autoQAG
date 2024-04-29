from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score


def get_topK_prompt_accuracy(results, k):
    # 创建一个字典来存储每个prompt的正确预测次数和总预测次数
    prompt_stats = {}

    # 遍历结果列表
    for result in results:
        prompt = result[3]
        # 检查预测是否正确
        is_correct = judge_equal(result[4], result[5])

        if prompt not in prompt_stats:
            prompt_stats[prompt] = {'correct': 0, 'total': 0}

        # 更新统计数据
        prompt_stats[prompt]['total'] += 1
        if is_correct:
            prompt_stats[prompt]['correct'] += 1

    # 计算每个prompt的准确率
    prompt_accuracy = {prompt: stats['correct'] / stats['total'] for prompt, stats in prompt_stats.items()}

    # 对prompt按准确率进行排序并获取前k个
    sorted_prompts = sorted(prompt_accuracy.items(), key=lambda x: x[1], reverse=True)
    top_k_prompts = sorted_prompts[:k]
    top_k_prompts_dict = dict(top_k_prompts)

    return top_k_prompts_dict


def judge_equal(model_res, real_res):
    model_res = model_res.replace(" ", "")
    real_res = real_res.replace(" ", "")
    return model_res == real_res


from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def calculate_multiclass_metrics_sklearn(results):
    # 创建一个字典来存储每个prompt的统计数据
    prompt_stats = {}

    # 初始化prompt统计字典
    for result in results:
        _, _, _, prompt, _, _ = result
        if prompt not in prompt_stats:
            prompt_stats[prompt] = {'y_true': [], 'y_pred': []}

    # 收集每个prompt的真实标签和预测标签
    for result in results:
        _, _, _, prompt, model_res, real_res = result
        prompt_stats[prompt]['y_true'].append(model_res)
        prompt_stats[prompt]['y_pred'].append(real_res)

    # 计算每个prompt的指标
    metrics = {}
    for prompt, data in prompt_stats.items():
        y_true = data['y_true']
        y_pred = data['y_pred']
        precision = precision_score(y_true, y_pred, average='macro')
        recall = recall_score(y_true, y_pred, average='macro')
        f1 = f1_score(y_true, y_pred, average='macro')

        metrics[prompt] = {'precision': precision, 'recall': recall, 'f1': f1}

    return metrics




if __name__ == '__main__':
    # results = [
    #     ["entityA", "entityB", "context", "prompt1", "real_res1", "real_res1"],
    #     ["entityA", "entityB", "context", "prompt2", "real_res2", "real_res2"],
    #     ["entityA", "entityB", "context", "prompt1", "model_res1", "real_res1"],
    #     ["entityA", "entityB", "context", "prompt3", "model_res3", "real_res3"],
    #     ["entityA", "entityB", "context", "prompt2", "model_res2", "real_res2"],
    #     ["entityA", "entityB", "context", "prompt3", "real_res3", "real_res3"],
    #     ["entityA", "entityB", "context", "prompt1", "real_res1", "real_res1"],
    #     ["entityA", "entityB", "context", "prompt2", "model_res2", "real_res2"],
    #     ["entityA", "entityB", "context", "prompt3", "real_res3", "real_res3"],
    # ]
    #
    # top_k_prompt = get_topK_prompt_accuracy(results, 5)
    # print(top_k_prompt)
    read_list = []
    with open(r"C:\code\src\python\autoQAG\result\ipre_testResult.txt", "r", encoding='utf-8') as file:
        file_content = file.read()
        # 将读取的字符串转换回列表
        read_list = eval(file_content)
    top_k_prompt = calculate_multiclass_metrics_sklearn(read_list)
    print(top_k_prompt)