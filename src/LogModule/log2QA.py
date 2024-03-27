import concurrent
import csv
import sys
import os

import pandas as pd
from tqdm import tqdm

sys.path.append('src/QaMaker')
from src.QaMaker.qaServer import QaServer
from src.QaMaker.configLoad import find_nearest_dir
from src.processMining.makePrompt import makePrompt


def process_row(row, csv_writer, originFilePath: str):
    prompt = makePrompt(originFilePath, row[7], row[11], row[12])
    qaBot = QaServer(prompt).genQaBot()
    qap = qaBot.getQuestAnsPair(row[7])
    row.append(prompt)
    row.append(qap[0])
    row.append(qap[1])
    csv_writer.writerow(row)


def log2QA(filename: str):
    base = find_nearest_dir('data')
    input_file_path = os.path.join(base, rf'loghub-master\{filename}\{filename}_2k.process_add.csv')
    origin_file_path = os.path.join(base, rf'loghub-master\{filename}\{filename}_2k.log_structured.csv')
    output_file_path = os.path.join(base, rf'loghub-master\{filename}\{filename}_2k.qa_file.csv')

    with open(input_file_path, 'r') as csv_input, open(output_file_path, 'w', newline='',
                                                       encoding='utf-8') as csv_output:
        csv_reader = csv.reader(csv_input)
        csv_writer = csv.writer(csv_output)

        header = next(csv_reader)
        header.append('prompt')
        header.append('question')
        header.append('answer')
        csv_writer.writerow(header)

        with tqdm(total=17) as progress_bar:
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                # Process each row in parallel
                futures = [executor.submit(process_row, row, csv_writer, origin_file_path) for row in csv_reader]

                # Wait for all threads to finish
                concurrent.futures.wait(futures)
                for future in concurrent.futures.as_completed(futures):
                    progress_bar.update(1)

    df = pd.read_csv(output_file_path)
    df.sort_values(by='LineId', ascending=True, inplace=True)
    df.to_csv(output_file_path, index=False)
    print("done,result at", output_file_path)


if __name__ == '__main__':
    log2QA('Test')
