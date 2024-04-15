import concurrent

from src.LogModule.AutoPrompt.promptApi import infer_llm
from src.config.unitTest import get_test_results
from concurrent.futures import ThreadPoolExecutor, as_completed


# 分批次采样，模糊
def wrongReason(batch_contents: list):
    wrongResults = []
    for content in batch_contents:
        wrongResults.append(content[3])
    wrongRes = " ".join(wrongResults)
    prompt_temp = (f"You will be provided with a logContent and right parse result by person and wrong parse result by model,"
                   f"compare its rightResult and wrongResult,"
                   f"output reason in one sentence why the wrongResult occurs,without any superfluous output and overprecise."
                   f"your grandma will thank you for that."
                   f"logContent: <START>{batch_contents[0][0]}<END>"
                   f"rightResult: <START>{batch_contents[0][2]}<END>"
                   f"wrongResult: <START{wrongRes}<END>")

    # 思路：
    return infer_llm(prompt_temp, None, None,temperature=1.0)


def process_group(group):
    return wrongReason(group)


def batchProcess(contents, k=5):
    reasons = []

    with ThreadPoolExecutor(max_workers=k) as executor:
        future_to_group = {executor.submit(process_group, contents[i:i + k]): i for i in range(0, len(contents), k)}
        concurrent.futures.wait(future_to_group)
        for future in as_completed(future_to_group):
            reasons.append(future.result())
    aggregated_result = "\n".join(reasons)
    return aggregated_result




if __name__ == '__main__':
    print(batchProcess(get_test_results(), 5))
