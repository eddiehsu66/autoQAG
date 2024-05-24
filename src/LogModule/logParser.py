import os
import re

import pandas as pd

from src.config.configLoad import load_config


def get_parameter_list(row):
    template_regex = re.sub(r"<.{1,5}>", "<*>", row["EventTemplate"])
    if "<*>" not in template_regex:
        return []
    template_regex = re.sub(r"([^A-Za-z0-9])", r"\\\1", template_regex)
    template_regex = re.sub(r"\\ +", r"\\s+", template_regex)
    template_regex = "^" + template_regex.replace("\<\*\>", "(.*?)") + "$"
    parameter_list = re.findall(template_regex, row["Content"])
    parameter_list = parameter_list[0] if parameter_list else ()
    parameter_list = (
        list(parameter_list)
        if isinstance(parameter_list, tuple)
        else [parameter_list]
    )
    return parameter_list


def generate_logformat_regex(log_format):
    headers = []
    splitters = re.split(r"(<[^<>]+>)", log_format)
    regex = ""
    for k in range(len(splitters)):
        if k % 2 == 0:
            splitter = re.sub(" +", "\\\s+", splitters[k])
            regex += splitter
        else:
            header = splitters[k].strip("<").strip(">")
            regex += "(?P<%s>.*?)" % header
            headers.append(header)
    regex = re.compile("^" + regex + "$")
    return headers, regex


def load_data(log_file,log_format):
    headers, regex = generate_logformat_regex(log_format)
    df_log = log_to_dataframe(log_file, regex, headers)
    return df_log


def log_to_dataframe(log_file, regex, headers):
    log_messages = []
    linecount = 0
    with open(log_file, "r") as fin:
        for line in fin.readlines():
            try:
                match = regex.search(line.strip())
                message = [match.group(header) for header in headers]
                log_messages.append(message)
                linecount += 1
            except Exception as e:
                print("[Warning] Skip line: " + line)
    logdf = pd.DataFrame(log_messages, columns=headers)
    logdf.insert(0, "LineId", None)
    logdf["LineId"] = [i + 1 for i in range(linecount)]
    print("Total lines: ", len(logdf))
    return logdf


def log_parser(category: str,uuid:str):
    log_file_path = f'../../cache/logs/{uuid}/Test.log'
    output_file_path = f'../../cache/logs/{uuid}/Test_parsed.csv'
    log_format = load_config('PARSE_SETTING')[category]['log_format']
    if not os.path.exists(output_file_path):
        return load_data(log_file_path,log_format).to_csv(output_file_path, index=False)


if __name__ == '__main__':
    output_file_path = '../../cache/logs/8F5B632B-B127-5294-DB7F-277AD406D193/Test_parsed.csv'
    log_parser('Test','a782d2f2-bbf8-420b-90f6-52758b113528')
