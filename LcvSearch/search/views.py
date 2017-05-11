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
            s.suggest()