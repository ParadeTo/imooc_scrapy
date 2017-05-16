import json
import math
import redis

from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from search.models import ArticleType
from elasticsearch import Elasticsearch

client = Elasticsearch(hosts=["127.0.0.1"])
redis_cli = redis.StrictRedis(host="localhost")

class IndexView(View):
    def get(self, request):
        topn_search = redis_cli.zrevrangebyscore("search_keywords_set", "+inf", "-inf", start=0, num=5)
        return render(request, "index.html", {
            "topn_search": topn_search
        })

class SearchSuggest(View):
    def get(self, request):
        key_words = request.GET.get('s', '')
        s_type = request.GET.get('s_type', 'article')

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


class SearchView(View):
    def get(self, request):
        key_words = request.GET.get("q", "")

        # 搜索关键词加1
        redis_cli.zincrby("search_keywords_set", key_words)

        # 排序，倒序
        topn_search = redis_cli.zrevrangebyscore("search_keywords_set", "+inf", "-inf", start=0, num=5)

        page = request.GET.get("p", "1")
        try:
            page = int(page)
        except:
            page = 1

        jobbole_count = redis_cli.get("jobbole_count")
        start_time = datetime.now()

        response = client.search(
            index = "jobbole",
            body = {
                "query": {
                    "multi_match": {
                        "query": key_words,
                        "fields": ["tags", "title", "content"]
                    }
                },
                "from": 10 * (page - 1),
                "size": 10,
                "highlight": {
                    "pre_tags": ['<span class="keyWord">'],
                    "post_tags": ['</span>'],
                    "fields": {
                        "title": {},
                        "content": {}
                    }
                }
            }
        )
        end_time = datetime.now()
        last_seconds = (end_time - start_time).total_seconds()

        total_nums = response["hits"]["total"]
        page_nums = math.ceil(total_nums / 10.0)

        hit_list = []
        for hit in response["hits"]["hits"]:
            hit_dict = {}
            if "title" in hit["highlight"]:
                # hit_dict["title"] = hit["highlight"]["title"][0] if isinstance(hit["highlight"]["title"], list) else hit["highlight"]["title"]
                hit_dict["title"] = "".join(hit["highlight"]["title"])
            else:
                hit_dict["title"] = hit["_source"]["title"]

            if "content" in hit["highlight"]:
                # hit_dict["content"] = hit["highlight"]["content"][0][:500] if isinstance(hit["highlight"]["content"], list) else hit["highlight"]["content"][:500]
                hit_dict["content"] = ("".join(hit["highlight"]["content"]))[:500]
            else:
                hit_dict["content"] = hit["_source"]["content"][:500]

            hit_dict["create_date"] = hit["_source"]["create_date"]
            hit_dict["url"] = hit["_source"]["url"]
            hit_dict["score"] = hit["_score"]

            hit_list.append(hit_dict)

        return render(request, "result.html", {
            "topn_search": topn_search,
            "jobbole_count": jobbole_count,
            "total_nums": total_nums,
            "page_nums": page_nums,
            "last_seconds": last_seconds,
            "page": page,
            "all_hits": hit_list,
            "key_words": key_words
        })


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