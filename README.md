# jsonParser
# 自定义json解析器

### 基于Python 2.7封装实现一个可重用的Json解析类，具体要求为:
 - 该类能读取JSON格式的数据，并以Python字典的方式读写数据；
 - 给定一个Python字典，可以更新类中数据，并以JSON格式输出；
 - 遵循JSON格式定义确保相同的同构数据源彼此转换后数据仍然一致；
 - 支持将数据以JSON格式存储到文件并加载回来使用；
 - 只允许使用Python string、unittest和logging模块，不允许使用eval、其他标准模块及任何第三方开发库；
  -独立完成此作业，不要参考任何现成代码。模块需要附带测试代码及一份简短的模块使用说明；使用git记录代码提交历史，使用unittest编写测试用例。

### 基本要求：
将文件名为jsonparser.py或包名为jsonparser的Python代码，连同测试代码和文档一起打包作为邮件附件提交。

jsonparser模块中包函一个类名为JsonParser的类，可以使用from jsonparser import JsonParser来导入该类。JsonParser类包含_data属性表示实例中保持的JSON Object内容，另外还包含以下方法：
- loads(self, s) 读取JSON格式数据，输入s为一个JSON字符串，无返回值。若遇到JSON格式错误的应该抛出异常。为简便考虑，JSON的最外层假定只为Object；
- dumps(self) 将实例中的内容转成JSON格式返回；
- load_file(self, f) 从文件中读取JSON格式数据，f为文件路径，异常处理同1，文件操作失败抛出异常；
- dump_file(self, f) 将实例中的内容以JSON格式存入文件，文件若存在则覆盖，文件操作失败抛出异常；
- load_dict(self, d) 从dict中读取数据，存入实例中，若遇到不是字符串的key则忽略；
- dump_dict(self) 返回一个字典，包含实例中的内容。
- JsonParser类支持用[]进行赋值、读写数据的操作，类似字典。
- JsonParser类包含方法update(self, d)用字典d更新实例中的数据，类似于字典的update。
***
### 注意：
 做5和6的操作时，实例==不要==直接引用输入参数d，也不要返回实例中_data字典的==任何引用。==
 返回值中所有字符串（包括key和value）转化为Python中的unicode类型字符串（因为JSON支持\uxxxx表示），特别注意转义符的转化。

***
>JSON格式：
http://json.org/json-zh.html
