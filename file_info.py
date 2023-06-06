import os
import json

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = f"{BASE_PATH}/data.bin"
SIZE_UNITS = ['Bytes', 'KB', 'MB', 'GB']


def set(file_path, write=True):
    file_path = file_path.replace('~/', os.environ["HOME"]+'/')
    file_path = file_path.replace('./', f"{BASE_PATH}/")
    print("serving : "+file_path)
    file_path = os.path.abspath(file_path)
    with open(DATA_PATH, 'wb') as f:
        f.write(file_path.encode('utf-8'))


def get(default=False):
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'rb') as f:
            file_path = f.read().decode('utf-8')
        if not os.path.exists(file_path):
            return default
        if os.path.isdir(file_path):
            data = [
                {
                    "path": os.path.join(file_path, i),
                    "name": i,
                    "size": size(file_path=os.path.join(file_path, i))
                }
                for i in os.listdir(file_path)
            ]
        else:
            data = [
                {
                    "path": file_path,
                    "name": os.path.basename(file_path),
                    "size": size(os.path.getsize(file_path))
                }
            ]
        return data
    return default


def size(file_path):
    size = 0
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
    if size <= 0:
        return 0, SIZE_UNITS[0]
    unit = 0
    while size > 999 and unit < len(SIZE_UNITS)-1:
        size = round(size/1024, 2)
        unit += 1
    return size, SIZE_UNITS[unit]


def name(file_path):
    return file_path.split('/')[-1]
