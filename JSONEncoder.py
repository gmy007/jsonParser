# -*- coding: utf-8
from JsonException import JsonException
import logConfig
import logging

logger = logging.getLogger(logConfig.logger_name + '.jsonEncoder')
SPECIAL_VALUE = {
    True: 'true',
    False: 'false',
    None: 'null',
    float('Infinity'): 'Infinity',
    float('-Infinity'): '-Infinity',
    float('NaN'): 'NaN'
}


class JSONEncoder(object):

    def encode(self, data):
        if data is None:
            return "null"
        else:
            return self._ensure_encode_value(data)

    def _ensure_encode_value(self, data):
        type_data = type(data)
        if type_data is dict:
            return self._encode_dict(data)
        if type_data in (list, tuple):
            return self._encode_list(data)
        if type_data in (str, unicode):
            return self._encode_string(data)
        if type_data in (float, int):
            return self._encode_num(data)
        elif data in SPECIAL_VALUE:
            try:
                return SPECIAL_VALUE[data]
            except KeyError:
                logger.warning('\t特殊类型值错误: {}'.format(type_data))
                raise JsonException('\t特殊类型值错误\t')
        else:
            logger.warning('\t没有匹配到encode类型：{}'.format(type_data))
            raise JsonException('\t没有匹配到encode类型\t')

    @classmethod
    def _encode_num(cls, data):
        return str(data)

    def _encode_list(self, data):
        str_list = ['[']
        _append = str_list.append
        is_first = True
        for item in data:
            if not is_first:
                _append(', ')
            _append(self.encode(item))
            is_first = False
        _append(']')
        return ''.join(str_list)

    def _encode_dict(self, data):
        str_list = ['{']
        _append = str_list.append
        is_first = True
        for k, v in data.items():
            if not isinstance(k, (unicode, str)):
                logger.warning('\t键值必须是unicode或string类型：{}'.format(type(k)))
                raise JsonException('\t键值必须是unicode或string类型\t')
            if not is_first:
                _append(', ')
            _append(self._encode_string(k))
            _append(':')
            _append(self.encode(v))
            is_first = False
        _append('}')
        # print(str_list)
        return ''.join(str_list)

    @classmethod
    def _encode_string(cls, data):
        process_value = ""
        for ch in data:
            if ch == '"':
                process_value += "\\\""
            elif ch == '\'':
                process_value += "\\\'"
            elif ch == '\\':
                process_value += "\\\\"
            elif ch == '\n':
                process_value += "\\n"
            elif ch == '\t':
                process_value += "\\t"
            elif ch == '\r':
                process_value += "\\r"
            else:
                process_value += ch
        return '\"' + process_value + '\"'
