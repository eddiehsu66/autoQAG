import pandas as pd

from src.config.configLoad import load_config


def parse_relation(relation: str):
    relation = relation.split('/')
    return relation[-1]


def get_train_dataSet():
    path = f"C:/code/src/python/autoQAG/data/ipre_data/train/train.csv"
    data = pd.read_csv(path, header=None)
    return data


def get_test_dataSet():
    path = f"C:/code/src/python/autoQAG/data/ipre_data/test/test.csv"
    data = pd.read_csv(path, header=None)
    return data



if __name__ == '__main__':
    # print(get_train_dataSet())
    print(parse_relation("外公"))
