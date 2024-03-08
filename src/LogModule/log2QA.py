import concurrent
import csv
import sys

sys.path.append('src/QaMaker')
from src.QaMaker.qaServer import QaServer


def process_row(row, csv_writer):
    content = row[1]

    qaBot = QaServer().genQaBot()
    qap = qaBot.getQuestAnsPair(content)

    row.append(qap[0])
    row.append(qap[1])

    csv_writer.writerow(row)


def log2QA(filename: str):
    input_file_path = f'../../data/loghub-master/{filename}/{filename}_2k.merged_file.csv'
    output_file_path = f'../../data/loghub-master/{filename}/{filename}_2k.qa_file.csv'

    with open(input_file_path, 'r') as csv_input, open(output_file_path, 'w', newline='') as csv_output:
        csv_reader = csv.reader(csv_input)
        csv_writer = csv.writer(csv_output)

        header = next(csv_reader)
        header.append('问题')
        header.append('答案')
        csv_writer.writerow(header)

        # Use ThreadPoolExecutor for parallel processing
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            # Process each row in parallel
            futures = [executor.submit(process_row, row, csv_writer) for row in csv_reader]

            # Wait for all threads to finish
            concurrent.futures.wait(futures)

    print("处理完成，结果保存在", output_file_path)


if __name__ == '__main__':
    log2QA('Android')
