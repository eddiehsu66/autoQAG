import concurrent
import csv
import sys
import os

import pandas as pd

sys.path.append('src/QaMaker')
from src.QaMaker.qaServer import QaServer
from src.QaMaker.configLoad import find_nearest_dir


def process_row(row, csv_writer):
    content = row[1]

    qaBot = QaServer().genQaBot()
    qap = qaBot.getQuestAnsPair(content)

    row.append(qap[0])
    row.append(qap[1])

    csv_writer.writerow(row)


def log2QA(filename: str):
    base = find_nearest_dir('data')
    input_file_path = os.path.join(base, rf'loghub-master\{filename}\{filename}_2k.merged_file.csv')
    output_file_path =os.path.join(base, rf'loghub-master\{filename}\{filename}_2k.qa_file.csv')

    with open(input_file_path, 'r') as csv_input, open(output_file_path, 'w', newline='',encoding='utf-8') as csv_output:
        csv_reader = csv.reader(csv_input)
        csv_writer = csv.writer(csv_output)

        header = next(csv_reader)
        header.append('question')
        header.append('answer')
        csv_writer.writerow(header)

        # Use ThreadPoolExecutor for parallel processing
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            # Process each row in parallel
            futures = [executor.submit(process_row, row, csv_writer) for row in csv_reader]

            # Wait for all threads to finish
            concurrent.futures.wait(futures)

    df = pd.read_csv(output_file_path)
    df.sort_values(by='LineId', ascending=True, inplace=True)
    df.to_csv(output_file_path, index=False)
    print("done,result at", output_file_path)


if __name__ == '__main__':
    log2QA('Test')
