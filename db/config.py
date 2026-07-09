from configparser import ConfigParser
from pathlib import Path
# this file loads the db connection details from database.ini


def load_config(filename='database.ini', section='postgresql'):
    filepath = Path(__file__).resolve().parent / filename
    parser = ConfigParser()
    parser.read(filepath)

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return config


if __name__ == '__main__':
    config = load_config()
    print(config)
