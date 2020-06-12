# -*- coding: utf-8
import unittest, json, time
from jsonparser import *

parser = JSONParser()
testJson1 = '{"status":"0000","message":"success","data":{"title":{"id":"001","name":"白菜"},"content":[{"id":"001","value":"你好白菜"},{"id":"002","value":"你好萝卜"}]}}'
testJson2 = '{"animal":"cat","color":"orange"}'
testJson3 = '{"eggCartoon":["egg","egg","egg","egg","egg","egg","egg",null,"egg",null,"egg"]}'
testJson4 = '{"\u5468\u661f\u661f":1}'
testJson5 = '''{
    "_id": "5ee0ce5390a827f4c83b24cf",
    "index": 0,
    "guid": "563d3881-cddc-40bf-ae3a-eb59f41d097d",
    "isActive": false,
    "balance": "$2,032.77",
    "picture": "http://placehold.it/32x32",
    "age": 40,
    "eyeColor": "green",
    "name": "Watts Carson",
    "gender": "male",
    "company": "BOINK",
    "email": "wattscarson@boink.com",
    "phone": "+1 (955) 591-2078",
    "address": "450 Ryerson Street, Grimsley, Pennsylvania, 3384",
    "about": "Sit qui mollit anim nisi ut Lorem esse cillum. Ullamco nisi aliquip non ullamco nulla culpa qui amet enim deserunt. Irure consectetur ad nisi do laborum sint deserunt amet enim esse enim fugiat in exercitation.\r\n",
    "registered": "2018-05-30T09:49:36 -08:00",
    "latitude": 53.007168,
    "longitude": 71.469448,
    "tags": [
      "mollit",
      "eu",
      "enim",
      "est",
      "cupidatat",
      "laborum",
      "ad"
    ],
    "friends": [
      {
        "id": 0,
        "name": "Krista Olson"
      },
      {
        "id": 1,
        "name": "Parks Diaz"
      },
      {
        "id": 2,
        "name": "Le Avila"
      }
    ],
    "greeting": "Hello, Watts Carson! You have 8 unread messages.",
    "favoriteFruit": "strawberry"
  }'''
testJson6 = """{
   "min_position": 7,
   "has_more_items": false,
   "items_html": "Car",
   "new_latent_count": 2,
   "data": {
      "length": 26,
      "text": "QQE2.com"
   },
   "numericalArray": [
      28,
      32,
      26,
      33,
      23
   ],
   "StringArray": [
      "Oxygen",
      "Nitrogen",
      "Nitrogen",
      "Oxygen"
   ],
   "multipleTypesArray": true,
   "objArray": [
      {
         "class": "middle",
         "age": 1
      },
      {
         "class": "upper",
         "age": 4
      },
      {
         "class": "middle",
         "age": 2
      },
      {
         "class": "upper",
         "age": 5
      },
      {
         "class": "upper",
         "age": 3
      }
   ]
}"""

tester1 = '{"a":[]}'  # ok
tester2 = '{"":"\\t\\n"}'  # ok
tester3 = '{"\\"":"\\""}'  # ok
tester4 = '{"a":{}'
# ok_2
tester5 = '{"a":' + '1' * 310 + '.0' + '}'
tester6 = '{"a": "\\u7f51\\u6613CC\\"\'"}'
tester7 = '{ "{ab" : "}123", "\\\\a[": "]\\\\"}'
path = 'd://' + time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime()) + '.txt'


class Jsonparser_test(unittest.TestCase):

    def test_json1(self):
        parser.loads(testJson1.decode('utf-8'))
        rt = json.loads(testJson1.decode('utf-8'))
        self.assertEqual(json.dumps(rt), parser.dumps())

    # def setUp(self):
    #     print 'This is test start Method:setUP'
    #
    # def tearDown(self):
    #     print 'This is test end Method: tearDown'

    def test_json2(self):
        '''
        :return: ok
        '''
        parser.loads(testJson2)
        self.assertEqual(json.loads(testJson2), parser.dump_dict())

    def test_json5(self):
        '''
        python内置json模块异常。。。
        :return: failed
        '''
        parser.loads(testJson5)
        print testJson5[0:225]
        self.assertEqual(json.loads(testJson5), parser.dump_dict())

    def test_json6(self):
        parser.loads(testJson5)
        print testJson5[0:225]
        self.assertEqual(json.loads(testJson5), parser.dump_dict())

    def test_load_file(self):
        parser.loads(testJson5)
        parser.dump_file(path)
        test_parser = JSONParser()
        test_parser.load_file(path)
        # self.assertEqual(parser.dumps(),test_parser.dumps())
        self.assertEqual(parser.dump_dict(), test_parser.dump_dict())  # OK

    def test_jsontester1(self):
        #print json.loads('{"a": "\\u7f51\\u6613CC\\"\'"}')

        parser.loads('{"a": "\\u7f51\\u6613CC\\"\'"}')
        #parser.loads('{ "{ab" : "}123", "\\\\a[": "]\\\\"}')
        # content = parser.dumps()
        parser.dump_file('test_for_0612.txt')
        t_parser=JSONParser()
        t_parser.load_file('test_for_0612.txt')
        self.assertEqual(t_parser.dump_dict(),parser.dump_dict())
        # print parser.dump_dict()
        # self.assertEqual(json.loads(tester4),parser.dump_dict())
