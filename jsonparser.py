# -*- coding: utf-8
from JSONDecoder import JSONDecoder
from JSONEncoder import JSONEncoder
import codecs
import logConfig
import logging

logger = logging.getLogger(logConfig.logger_name + '.jsonParser')


class JSONParser(object):

    def __init__(self):
        self._data = {}
        self.jsonDecoder = JSONDecoder()
        self.jsonEncoder = JSONEncoder()

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data.__setitem__(key, value)

    def __delitem__(self, key):
        del self._data[key]

    def __contains__(self, item):
        return item in self._data

    def loads(self, s):
        """
        加载json串
        :param s: JSON string
        :return: None
        """
        if not isinstance(s, str) and not isinstance(s, unicode):
            logger.warning('用户输入类型有误：%s', type(str))
            raise TypeError('输入的必须是字符串')
        if len(s) <= 0:
            raise ValueError('No json obj can be load')
        self._data = self.jsonDecoder.decode(s)

    def dumps(self):
        """
        转化为json字符串
        :return: JSON string
        """
        content = self.jsonEncoder.encode(self._data)
        return content

    def load_file(self, path):
        """
        从文件中加载json串
        :param path:
        :return: None
        """
        with codecs.open(path, 'r', encoding='utf-8') as f:
            s = f.read()
            self.loads(s)

    def dump_file(self, path):
        """
        写入文件
        :param path:
        :return: None
        """
        with codecs.open(path, 'w+', encoding='utf-8') as f:
            f.write(self.dumps())

    def load_dict(self, input_dict):
        """
        从dict读取数据存入实例
        :param input_dict:
        :return: None
        """
        json_str = self.jsonEncoder.encode(input_dict)
        json_obj = self.jsonDecoder.decode(json_str)
        self._data = json_obj

    def dump_dict(self):
        """
        返回一个字典，包含实例的内容
        :return:
        """
        if not isinstance(self._data, dict):
            logger.warning('Self_data type is wrong :%s', type(self._data))
            raise TypeError('\tData type is not dict\t')
        json_str = self.jsonEncoder.encode(self._data)
        return self.jsonDecoder.decode(json_str)

    def update(self, others):
        """
        更新_data
        :param others:
        :return:
        """
        self.load_dict(others)
