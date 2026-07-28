import os
from urllib.parse import urlparse
# this file loads the db connection details from database.ini


def load_config(filename='database.ini', section='postgresql'):
    url = os.environ['DATABASE_URL']
    parsed = urlparse(url)
    return {
        "host": parsed.hostname,
        "port": parsed.port,
        "dbname": parsed.path[1:],   # strip the leading slash
        "user": parsed.username,
        "password": parsed.password,
    }


if __name__ == '__main__':
    config = load_config()
    print(config)
