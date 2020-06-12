#!/usr/bin/env python
# -*- coding: utf-8
import sys
import json
from itertools import chain

try:
    from JSONParser import JSONParser
except ImportError:
    from jsonparser import *

# reload(sys)
# sys.setdefaultencoding('utf-8')
# print sys.getdefaultencoding()
__date__ = "20150414"

json_ok = [
    ('{}', 1),
    ('{"":""}', 1),
    ('{"a":123}', 1),
    ('{"a":-123}', 1),
    ('{"a":1.23}', 1),
    ('{"a":1e1}', 1),
    ('{"a":true,"b":false}', 1),
    ('{"a":null}', 1),
    ('{"a":[]}', 1),
    ('{"a":{}}', 1),
    (' {"a:": 123}', 1),
    ('{ "a  " : 123}', 1),
    ('{ "a" : 123    	}', 1),
    ('{"true": "null"}', 1),
    ('{"":"\\t\\n"}', 1),
    ('{"\\"":"\\""}', 1),
]
json_ok2 = [
    ('{"a":' + '1' * 310 + '.0' + '}', 2),
    ('{"a":"abcde,:-+{}[]"}', 2),
    ('{"a": [1,2,"abc"]}', 2),
    ('{"d{": "}dd", "a":123}', 2),
    ('{"a": {"a": {"a": 123}}}', 2),
    ('{"a": {"a": {"a": [1,2,[3]]}}}', 2),
    ('{"a": "\\u7f51\\u6613CC\\"\'"}', 3),

    ('{"a":1e-1, "cc": -123.4}', 2),
    ('{ "{ab" : "}123", "\\\\a[": "]\\\\"}', 3),
]

json_ex = [
    # exceptions
    ('{"a":[}', 2),
    ('{"a":"}', 2),

    ('{"a":True}', 1),
    ('{"a":Null}', 1),
    ('{"a":foobar}', 2),
    ("{'a':1}", 3),
    ('{1:1}', 2),
    ('{true:1}', 2),
    ('{"a":{}', 2),
    ('{"a":-}', 1),
    ('{"a":[,]}', 2),
    ('{"a":.1}', 1),
    ('{"a":+123}', 2),
    ('{"a":"""}', 1),
    ('{"a":"\\"}', 1),
]

a1 = JSONParser()
a2 = JSONParser()
a3 = JSONParser()

total = 0
expect = 0
errors = []
for s, score in chain(json_ok, json_ex):
    expect += score
    try:
        dst = json.loads(s)
    except Exception:
        dst = Exception

    try:
        a1.loads(s)
        d1 = a1.dump_dict()
    except Exception as ex:
        d1 = ex

    if (dst is Exception and isinstance(d1, Exception)) or (dst == d1):
        total += score
    elif isinstance(d1, Exception):
        errors.append([s, 'ret ex:' + str(d1)])
    else:
        errors.append([s, json.dumps(d1)])

tmp_output_file = 'tmp_output_file.txt'
for s, score in json_ok2:
    expect += score
    try:
        dst = json.loads(s)
    except Exception as ex:
        print '%r' % s
        raise

    try:
        a1.loads(s)
        d1 = a1.dump_dict()
    except Exception as ex:
        errors.append([s, "ex:" + str(ex)])
        continue

    try:
        a2.load_dict(d1)
        a2.dump_file(tmp_output_file)
        a3.load_file(tmp_output_file)
        d3 = a3.dump_dict()
    except Exception as ex:
        errors.append([s, "ex:" + str(ex)])
        continue

    if d3 == dst:
        total += score
    else:
        errors.append([s, json.dumps(d3)])

# test load_dict()
a4 = JSONParser()
# dst = dict(a=1, b=(1,2), c=["a", -123.4], d={}, e=[], f=0, g=True, h=None)
dst = dict(a=1, b=[1, 2], c=["a", -123.4], d={}, e=[], f=0, g=True, h=None)
try:
    expect += 5
    a4.load_dict(dst)
    d4 = a4.dump_dict()
    if d4 == dst and d4 is not dst and d4['c'] is not dst['c']:
        total += 5
    else:
        errors.append(['load_dict: %s' % (json.dumps(dst)), json.dumps(d4)])
except Exception as ex:
    errors.append(['load_dict', 'ex:' + str(ex)])

# test __getitem__, __del__()
try:
    expect += 2
    if a4["a"] == 1:
        total += 2
except Exception as ex:
    errors.append(['get_item', "ex:" + str(ex)])

try:
    expect += 3
    del a4["a"]
    if "a" not in a4:
        total += 3
except Exception as ex:
    errors.append(['del', "ex:" + str(ex)])

# test update()
try:
    expect += 2
    src_dict = {"a": [1, 2]}
    a4.update(src_dict)
    assert a4["a"] == [1, 2] and a4["a"] is not src_dict["a"]
    total += 2
except Exception as ex:
    errors.append(['update', "ex:" + str(ex)])

# test time
import time

s = json.dumps({"a": 123456, "b": [{"a": "test", "b": True}], "c": "1" * 100})

start = time.time()
for i in range(1000):
    json.loads(s)
elapsed1 = time.time() - start

start = time.time()
for i in range(1000):
    a1 = JSONParser()
    try:
        a1.loads("{}")
    except Exception:
        pass
elapsed2 = time.time() - start

print "errors\n", json.dumps(errors, indent=2)
print "score: %s / %s = %s" % (total, expect, total * 100.0 / expect)
print "time: %s / %s = %s" % (elapsed2, elapsed1, elapsed2 / elapsed1)

raw_input("Input 'Enter' to quit")
