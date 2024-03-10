import os

from logparser.Drain import LogParser
from src.QaMaker.configLoad import load_config


def logParse(fileName:str):
    input_dir = f'../../data/loghub-master/{fileName}'
    output_dir = f'../../data/loghub-master/{fileName}/Test'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    settings = load_config("PARSE_SETTING")
    log_file = settings[fileName]["log_file"]
    parser = LogParser(
        settings[fileName]["log_format"],
        indir=input_dir,
        outdir=output_dir,
        depth=settings[fileName]["depth"],
        st=settings[fileName]["st"],
        rex=settings[fileName]["regex"]
    )
    parser.parse(log_file)


if __name__ == '__main__':
    logParse("Apache")
