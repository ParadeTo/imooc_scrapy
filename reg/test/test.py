# -*- coding: utf-8 -*-

import re

line = "boooooooobby123"

def match_res(reg, str):
    match_obj = re.match(regex_str, line)
    if match_obj:
        print(match_obj.group(1))

# ? 匹配尽可能短
regex_str = ".*?(b.*?b).*"
match_res(regex_str, line)

# + 至少一次
line = "boooooooobby123"
regex_str = ".*(b.+b).*"
match_res(regex_str, line)

# |
line = "bobby123"
regex_str = "(bobby|bobby123)"
match_res(regex_str, line)

# group
line = "bobby123"
regex_str = "((bobby|bobby)123)"
match_obj = re.match(regex_str, line)
if match_obj:
    print(match_obj.group(1)) # 外层
    print(match_obj.group(2)) # 内层

# []里面的任何一个,且没有特殊含义，中括号里面的.*就是简单的字符
line = "1861111254644444"
#regex_str = "(1[48357][0-9]{9})"
regex_str = "1[48357]\d{9}"
match_obj = re.match(regex_str, line)
print(match_obj)

# \s \S   \w=[A-Za-z0-9_] \W
line = "你__好"
regex_str = "(你\w*好)"
match_res(regex_str, line)