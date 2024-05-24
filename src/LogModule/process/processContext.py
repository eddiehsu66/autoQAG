import csv
import os

from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
import pm4py
import pandas as pd
from pm4py.objects.log.importer.xes import importer as xes_importer

from src.LogModule.process.processMining import csv2xes


def find_successor_events(petri_net, target_transition_name):
    # 查找目标转移对象
    target_transition = None
    for transition in petri_net.transitions:
        if transition.name == target_transition_name:
            target_transition = transition
            break

    if not target_transition:
        return []  # 如果没有找到目标转移，返回空列表

    output_places = [arc.target for arc in target_transition.out_arcs]

    # 找到这些库所的输出转移，即后继事件
    successor_transitions = set()
    for place in output_places:
        for arc in place.out_arcs:
            successor_transitions.add(arc.target)

    # 返回后继事件的名称列表
    return [t.name for t in successor_transitions]


def find_predecessor_events(petri_net, target_transition_name):
    # 查找目标转移对象
    target_transition = None
    for transition in petri_net.transitions:
        if transition.name == target_transition_name:
            target_transition = transition
            break

    if not target_transition:
        return []  # 如果没有找到目标转移，返回空列表

    # 找到目标转移的输入库所
    input_places = [arc.source for arc in target_transition.in_arcs]

    # 找到这些库所的输入转移，即前继事件
    predecessor_transitions = set()
    for place in input_places:
        for arc in place.in_arcs:
            predecessor_transitions.add(arc.source)

    # 返回前继事件的名称列表
    return [t.name for t in predecessor_transitions]


# def process_row(row, petri_net, csv_writer):
#     content = row[9]
#
#     row.append(find_predecessor_events(petri_net, content))
#     row.append(find_successor_events(petri_net, content))
#
#     csv_writer.writerow(row)


def add2csv(petri_net, fromPath: str, toPath: str):
    with open(fromPath, 'r') as csv_input, open(toPath, 'w', newline='', encoding='utf-8') as csv_output:
        csv_reader = csv.reader(csv_input)
        csv_writer = csv.writer(csv_output)
        header = next(csv_reader)
        header.append('predecessor')
        header.append('successor')
        csv_writer.writerow(header)

        for row in csv_reader:
            process_row(row, petri_net, csv_writer)


def process_row(row, petri_net):
    # 这里需要根据具体的逻辑来处理每一行数据
    # 假设我们有一些逻辑来确定predecessor和successor
    content = row['EventTemplate']
    row['predecessor'] = find_predecessor_events(petri_net, content)
    row['successor'] = find_successor_events(petri_net, content)
    return row


def process_context(UUID):
    xes_path = f'../../../cache/logs/{UUID}/Test_mining.xes'
    log_path = f'../../../cache/logs/{UUID}/Test_template.csv'
    if not os.path.exists(xes_path):
        df = pd.read_csv(log_path)
        csv2xes(df, xes_path)
    process_path = f'../../../cache/logs/{UUID}/Test_process.csv'
    log = xes_importer.apply(xes_path)
    net, initial_marking, final_marking = heuristics_miner.apply(log)

    df = pd.read_csv(log_path, encoding='utf-8')
    df['predecessor'] = None
    df['successor'] = None
    df = df.apply(lambda row: process_row(row, net), axis=1)
    df.to_csv(process_path, index=False, encoding='utf-8')


if __name__ == '__main__':
    process_context('51ac8ff1-314d-4899-9218-bd1f3b5cafcc')
