import csv
import json

def convert_csv_to_json(input_file, output_file):
    with open(input_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        with open(output_file, 'w') as jsonfile:
            for row in reader:
                query = row['Content']
                answer = row['EventTemplate']
                json_data = {"query": query, "answer": answer}
                json.dump(json_data, jsonfile)
                jsonfile.write('\n')

# 使用示例
if __name__ == '__main__':
    convert_csv_to_json(r'C:\code\src\python\autoQAG\data\loghub-master\HPC\HPC_2k.log_32sampled.csv', '32shot.json')
