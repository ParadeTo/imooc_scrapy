# -*- coding: utf-8 -*-

import re


line = 'xxx出生于2001年6月'
# line = 'xxx出生于2001/6/1'
# line = 'xxx出生于2001-6-1'
# line = 'xxx出生于2001-06-01'
# line = 'xxx出生于2001-06'


regex_str = ".*出生于(\d{4}[年/-]\d{1,2}[月/-]?(\d{1,2}|$))"
match_obj = re.match(regex_str, line)
print match_obj
if match_obj:
    print match_obj.group(1)
