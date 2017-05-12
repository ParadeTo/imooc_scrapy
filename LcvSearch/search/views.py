import json
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from search.models import ArticleType


class SearchSuggest(View):
    def get(self, request):
        key_words = request.GET.get('s', '')
        re_datas = []
        if key_words:
            s = ArticleType.search()
            s = s.suggest('my_suggest', key_words, completion={
                "field": "suggest",
                "fuzzy": {
                    "fuzziness": 2
                },
                "size": 10
            })
            suggestions = s.execute_suggest()
            if hasattr(suggestions, "my_suggest"):
                for match in suggestions.my_suggest[0].options:
                    source = match._source
                    re_datas.append(source["title"])

        return HttpResponse(json.dumps(re_datas), content_type="application/json")




# s = ArticleType.search()
# s = s.suggest('my_suggest', '水平', completion={
#     "field": "suggest",
#     "fuzzy": {
#         "fuzziness": 1
#     },
#     "size": 10
# })
# suggestions = s.execute_suggest()
# for match in suggestions['my_suggest'][0].options:
#     pass