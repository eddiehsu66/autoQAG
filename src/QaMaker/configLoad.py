import yaml

file_path = '../config/config.yaml'


def load_config(config_name):
    with open(file_path, 'r') as file:
        config_data = yaml.safe_load(file)
    return config_data[config_name]


if __name__ == '__main__':
    print(load_config("OPENAI_API_KEY"))
