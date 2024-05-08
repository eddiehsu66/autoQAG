import pm4py
import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.objects.petri_net.exporter.variants import pnml as pnml_exporter
from pm4py.visualization.process_tree import visualizer as pt_visualizer


def alphaMiner():
    path = r'C:\code\src\python\autoQAG\data\loghub-master\Test\Test_2k.log_structured.xes'
    netPath = r'C:\code\src\python\autoQAG\data\loghub-master\Test\Test_2k.pn_net.pnml'
    petriPath = r'C:\code\src\python\autoQAG\data\loghub-master\Test\Test_2k.pn_net.svg'

    treeSvgPath = r'C:\code\src\python\autoQAG\data\loghub-master\Test\Test_2k.process_tree.svg'
    log = xes_importer.apply(path)
    # 使用Alpha Miner算法进行流程挖掘
    # net代表发现的过程模型，initial_marking代表Petri网的初始标记，final_marking代表Petri网的最终标记。
    net, initial_marking, final_marking = heuristics_miner.apply(log)

    pnml_exporter.export_net(net, initial_marking, netPath, final_marking)

    # 可视化挖掘到的Petri网
    pm4py.save_vis_petri_net(net, initial_marking, final_marking, petriPath, format="svg")

    # tree = pm4py.discover_process_tree_inductive(log)
    #
    # pm4py.save_vis_process_tree(tree, treeSvgPath, format="svg")


if __name__ == '__main__':
    alphaMiner()
