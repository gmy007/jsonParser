# -*- coding: utf-8
import re
import string
from JsonException import JsonException
import logConfig
import logging

logger = logging.getLogger(logConfig.logger_name + '.jsonDecoder')
NUMBER_RE = re.compile(
    r'(-?(?:0|[1-9]\d*))(\.\d+)?([eE][-+]?\d+)?',
    (re.VERBOSE | re.MULTILINE | re.DOTALL))
match_number = NUMBER_RE.match
BACKSLASH = {
    '"': '"', '\\': '\\', '/': '/',
    'b': '\b', 'f': '\f', 'n': '\n', 'r': '\r', 't': '\t', '\'': '\''
}
hexdigits = string.hexdigits


class JSONDecoder(object):
    # 空白区域
    _white_space = ['\r', '\n', '\t', ' ']

    def __init__(self):
        self._str = None  # 输入json串
        self._idx = 0  # 当前遍历下标
        self._cur = None  # 当前遍历字符

    def decode(self, s):
        """
        解码json串
        :param s: json串
        :return: object
        """
        self._cur = s[0]
        self._idx = 0
        self._str = s
        self._skip_white_space()
        ret = self._parse_obj()
        return ret

    def _has_next(self):
        """
         判断是否还有下个字符等待扫描
        :return:None
        """
        return self._idx + 1 < len(self._str)

    def _next(self, step=1):
        """
        移动当前位置
        :param step:扫描步长
        """
        if self._idx + step < len(self._str):
            self._idx += step
            self._cur = self._str[self._idx]
        else:
            logger.warning('无法访问下一个字符')
            raise JsonException('\tjson数据有误，无法扫描下一字符\t')

    def _skip_white_space(self):
        """
        跳过空白字符
        """
        while self._cur in self._white_space and self._has_next():
            self._next()

    def _parse_obj(self):
        """
        解码json对象
        :return: obj
        """
        data = {}
        if self._cur != '{':
            logger.warning('未扫描到合理对象 %s', self._cur)
            raise JsonException('\t未扫描到合理对象\t')
        if not self._has_next():
            logger.warning('Method: _parse_obj：非法的object')
            raise JsonException('\t非法的object\t')
        self._next()
        # 对象为空值
        if self._cur == '}':
            return {}

        while True:
            # 每次遍历获取一个对象
            self._skip_white_space()
            if self._cur != '"':
                logger.warning('对象键值必须为string类型 %s ', self._cur)
                raise JsonException('\t对象类的键值必须为string类型\t')
            # 得到key值
            key = self._parse_string()
            self._skip_white_space()
            if not self._has_next():
                logger.warning('\t没有匹配value值\t')
                raise JsonException('\t没有匹配value值\t')
            if self._cur == ':':
                self._next()
            self._skip_white_space()
            # 确定value的类型并返回
            value = self._ensure_value_type()
            data[key] = value
            self._skip_white_space()
            if self._cur == '}':
                break
            elif self._cur == ',' and self._has_next():
                self._next()
            else:
                logger.warning('json 数据异常')
                raise JsonException('\tjson 数据异常\t')
        return data

    def _parse_string(self):
        if self._cur == '"':
            self._next()
        ret = []
        while self._has_next():
            if self._cur == '"':
                self._next()
                return ''.join(ret)
            elif self._cur == '\\':
                self._next()
                if self._cur == 'u':
                    ret.append(self._decode_chinese())
                    self._next()
                else:
                    try:
                        char = BACKSLASH[self._cur]
                        ret.append(char)
                        self._next()
                    except KeyError:
                        logger.warning('错误的转义符')
                        raise JsonException('\t错误的转义字符\t')
            else:
                ret.append(self._cur)
                self._next()
        logger.warning('string类型没有后引号')
        raise JsonException('\tstring类型没有后引号\t')

    def _decode_chinese(self):
        unicode_char = '\u'
        for i in range(4):
            self._next()
            ch = self._cur
            if ch not in hexdigits:
                logger.warning("Invalid hex char : %s" % ch)
                raise JsonException("Invalid hex char : %s" % ch)
            unicode_char += ch
        return unicode_char.decode("raw_unicode_escape")

    def _ensure_value_type(self):
        if self._cur == '"':
            return self._parse_string()
        elif self._cur == '{':
            value = self._parse_obj()
            self._next()
            return value
        elif self._cur == 'n':
            return self._parse_null()
        elif self._cur == 't' or self._cur == 'f':
            return self._parse_boolean()
        elif self._cur == '[':
            return self._parse_list()
        elif self._cur == '-' or (str(self._cur)).isdigit():
            (number, step) = self._parse_num()
            self._next(step)
            return number
        elif self._cur in ('I', 'i', 'n', 'N'):
            return self._parse_num()
        else:
            logger.warning('没有匹配到value类型: %s', self._cur)
            raise JsonException('\t没有匹配到value类型: {}'.format(self._cur))

    def _parse_null(self):
        if self._str.startswith('null', self._idx):
            self._next(4)
            return None
        else:
            logger.warning('不是合法的null值 %s', self._str[self._idx, self._idx + 4])
            raise JsonException('\t不是合法的null值\t')

    def _parse_boolean(self):
        if self._str.startswith('true', self._idx):
            self._next(4)
            return True
        elif self._str.startswith('false', self._idx):
            self._next(5)
            return False
        else:
            logger.warning('非法的boolean值 %s', self._cur)
            raise JsonException('\t非法的boolean值 {}'.format(self._cur))

    def _parse_list(self):
        if self._cur == '[':
            self._next()
        if not self._has_next():
            logger.warning('扫描的list对象没有下个字符')
            raise JsonException('\t扫描的list对象没有下个字符\t')
        if self._cur == ']':
            self._next()
            return []
        value = []
        while 1:
            self._skip_white_space()
            value.append(self._ensure_value_type())
            self._skip_white_space()
            if self._cur == ',':
                self._next()
            elif self._cur == ']':
                self._next()
                return value

    def _parse_num(self):
        self._skip_white_space()
        m = match_number(self._str[self._idx:], 0)
        if m is not None:
            integer, frac, exp = m.groups()
            if frac or exp:
                res = float(integer + (frac or '') + (exp or ''))
            else:
                res = int(integer)
            return res, m.end()
        elif self._cur == 'N' and self._str[self._idx:self._idx + 3] == 'NaN':
            self._next(3)
            return float('NaN')
        elif self._cur == 'I' and self._str[self._idx:self._idx + 8] == 'Infinity':
            self._next(8)
            return float('Infinity')
        elif self._cur == '-':
            if self._str[self._idx:self._idx + 9] == '-Infinity':
                self._next(9)
                return float('-Infinity')
            elif self._str[self._idx:self._idx + 4] == '-inf':
                self._next(4)
                return float('-Infinity')
        elif self._cur == 'i' and self._str[self._idx:self._idx + 3] == 'inf':
            self._next(3)
            return float('Infinity')
        else:
            raise StopIteration
