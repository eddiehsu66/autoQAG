import re


def tidy(input_string):
    # 使用 replace 替换空格和换行符为空字符串
    cleaned_string = input_string.replace(" ", "").replace("\n", "")
    return cleaned_string


def extractQA(input_string):
    # 定义问题和答案的正则表达式模式
    question_pattern = r"问题：(.+?)(?:\n|$)"
    answer_pattern = r"答案：(.+?)(?:\n|$)"

    # 使用正则表达式匹配问题和答案
    question_match = re.search(question_pattern, input_string)
    answer_match = re.search(answer_pattern, input_string)
    # 检查匹配结果
    if question_match and answer_match:
        question = question_match.group(1).strip()
        answer = answer_match.group(1).strip()
        return question, answer
    else:
        return None,None

if __name__ == "__main__":
    print(extractQA("问题：谁在 2024 年 3 月 7 日上午 10:15:30 登录成功？\n答案：用户123。"))