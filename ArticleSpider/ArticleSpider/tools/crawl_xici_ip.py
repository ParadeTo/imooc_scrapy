# -*- coding: utf-8 -*-
import requests
import MySQLdb
from scrapy.selector import Selector

conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123456", db="scrapy", charset="utf8")
cursor = conn.cursor()

def crawl_ips():
    # 爬取西刺的免费ip代理
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36"
    }

    for i in range(1642, 0, -1):

        re = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)

        selector = Selector(text=re.text)
        all_trs = selector.css("#ip_list tr")

        ip_list = []
        for tr in all_trs[1:]: # 不要表头
            speed_str = tr.css(".bar::attr(title)").extract()[0]
            if speed_str:
                speed = float(speed_str.split("秒")[0])

            # all_texts = tr.css("td::text").extract()
            #
            # ip = all_texts[0]
            # port = all_texts[1]
            # proxy_type = all_texts[5]

            ip = tr.css("td:nth-of-type(2)::text").extract()[0]
            port = tr.css("td:nth-of-type(3)::text").extract()[0]
            proxy_type = tr.css("td:nth-of-type(6)::text").extract()[0].strip();

            if proxy_type.lower().find("http") == -1:
                continue

            ip_list.append((ip, port, speed, proxy_type))

        for ip_info in ip_list:
            cursor.execute(
                """
                    INSERT INTO
                      proxy_ip(ip, port, speed, proxy_type)
                    VALUES
                      (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                      port=VALUES(port), speed=VALUES(speed), proxy_type=VALUES(proxy_type)
                """
            , (ip_info[0], ip_info[1], ip_info[2], ip_info[3]))

            conn.commit()

class GetIP(object):
    def check_ip(self, ip, port):
        # 判断ip是否可用
        http_url = "http://www.baidu.com"
        proxy_url = "http://{0}:{1}".format(ip, port)
        try:
            proxy_dict = {
                "http": proxy_url
            }
            response = requests.get(http_url, timeout=2, proxies=proxy_dict)
        except Exception as e:
            print ("invalid ip and port")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print ("effective ip")
                return True
            else:
                print ("invalid ip and port")
                self.delete_ip(ip)
                return False

    def delete_ip(self, ip):
        delete_sql = """
            DELETE FROM
              proxy_ip
            WHERE
              ip='{0}'
        """.format(ip)

        cursor.execute(delete_sql)
        conn.commit()
        return True

    def get_random_ip(self):
        # 从数据库中随机获取一个可用ip
        random_sql = """
            SELECT ip, port
            FROM proxy_ip
            WHERE proxy_type
            NOT LIKE "%HTTPS%"
            ORDER BY RAND()
            LIMIT 1
        """

        result = cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]

            judge_re = self.check_ip(ip, port)
            if judge_re:
                return "http://{0}:{1}".format(ip, port)
            else:
                return self.get_random_ip()

            # if self.check_ip(ip, port):
            #     return (ip, port)
            # else:
            #     return False

if __name__ == "__main__":
    get_ip = GetIP()
    while True:
        result = get_ip.get_random_ip()
        if result:
            print (result)
            break
