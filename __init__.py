from JSONDecoder import JSONDecoder
from JSONEncoder import JSONEncoder
from jsonparser import JSONParser

__all__ = [
    'JSONParser', 'loads',
    'load_dict', 'load_file',
    'dump_file', 'dump_dict', 'dumps','testjson'
]

run = JSONParser()


def loads(s):
    return run.loads()


def load_file(path):
    return run.load_file(path)


def load_dict(dic):
    return run.load_dict(dic)


def dumps():
    return run.dumps()


def dump_dict():
    return run.dump_dict()


def dump_file(path):
    return run.dump_file()
