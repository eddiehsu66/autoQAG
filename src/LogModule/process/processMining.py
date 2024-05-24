import os

import pandas as pd
import pm4py
from pm4py import discover_bpmn_inductive
from pm4py.algo.filtering.log.paths import paths_filter
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.bpmn.exporter import exporter as bpmn_exporter
from pm4py.objects.conversion.log import converter as log_converter

from src.config.redisKit import redisInit

DEFAULT_SEP = '<SEP>'


def csv2xes(df, toPath: str):
    # 从CSV文件中导入数据框
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S.%f')
    dataframe = pm4py.format_dataframe(df, case_id='Component', activity_key='EventTemplate',
                                       timestamp_key='Time', timest_format='%H:%M:%S.%f')
    event_log = pm4py.convert_to_event_log(dataframe)
    pm4py.write_xes(event_log, toPath)


def use_heuristics_miner(log_path, xes_path, bpmn_path, process_path,UUID):
    df = pd.read_csv(log_path)
    csv2xes(df, xes_path)
    log = xes_importer.apply(xes_path)
    # net, initial_marking, final_marking = heuristics_miner.apply(log)
    paths = get_paths_from_log(log)
    sorted_paths = paths_filter.get_sorted_paths_list(paths)
    client = redisInit()
    log_all_path = []
    for path in sorted_paths:
        log_template_path = path[0].split(DEFAULT_SEP)
        sub_all_path = []
        for sub_log_template in log_template_path:
            log_content_path = ','.join(client.smembers('LogTemplate:' + UUID + ':' + sub_log_template))
            sub_all_path.append(log_content_path)
        log_all_path.append(','.join(sub_all_path))
    pd.Series(log_all_path).to_csv(process_path, index=False, header=False)
    bpmn_graph = discover_bpmn_inductive(log)
    bpmn_exporter.apply(bpmn_graph, bpmn_path)


def get_paths_from_log(log, attribute_key="concept:name"):
    log = log_converter.apply(log, variant=log_converter.Variants.TO_EVENT_LOG)

    paths = {}
    for trace in log:
        for i in range(0, len(trace) - 1):
            if attribute_key in trace[i] and attribute_key in trace[i + 1]:
                path = trace[i][attribute_key] + DEFAULT_SEP + trace[i + 1][attribute_key]
                if path not in paths:
                    paths[path] = 0
                paths[path] = paths[path] + 1
    return paths


def process_mining(UUID: str):
    log_path = f'../../cache/logs/{UUID}/Test_template.csv'
    xes_path = f'../../cache/logs/{UUID}/Test_mining.xes'
    bpmn_path = f'../../cache/logs/{UUID}/Test_visual.bpmn'
    process_path = f'../../cache/logs/{UUID}/process_set.csv'
    if not os.path.exists(bpmn_path):
        use_heuristics_miner(log_path, xes_path, bpmn_path,process_path, UUID)


if __name__ == '__main__':
    process_mining('def865f9-571e-4011-aa9c-70a77e979ed6')
