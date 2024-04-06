import os

from logparser.Drain import LogParser
from src.config.configLoad import load_config,find_nearest_dir


def logParse(fileName:str):
    base = find_nearest_dir('data')
    dirName = os.path.join(base,rf'loghub-master\{fileName}')
    settings = load_config("PARSE_SETTING")
    log_file = settings[fileName]["log_file"]
    parser = LogParser(
        settings[fileName]["log_format"],
        indir=dirName,
        outdir=dirName,
        depth=settings[fileName]["depth"],
        st=settings[fileName]["st"],
        rex=settings[fileName]["regex"]
    )
    parser.parse(log_file)


if __name__ == '__main__':
    logParse("Test")
