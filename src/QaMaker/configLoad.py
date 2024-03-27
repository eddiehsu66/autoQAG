import yaml
import os


def load_config(config_name: str):
    src_dir = find_nearest_dir('src')
    file_path = os.path.join(src_dir, r'config/config.yaml')
    with open(file_path, 'r',encoding='utf-8') as file:
        config_data = yaml.safe_load(file)
    return config_data[config_name]


def find_nearest_dir(dirName:str):
    current_dir = os.getcwd()
    while current_dir != '/':
        src_dir = os.path.join(current_dir, dirName)
        if os.path.isdir(src_dir):
            return os.path.abspath(src_dir)
        current_dir = os.path.dirname(current_dir)

    return None


if __name__ == '__main__':
    print(load_config("OPENAI_API_KEY"))
