__author__ = "xumeng"
__date__ = "2018/11/17 13:28"
'''
爬取并分析熊猫Tv主播热度排名
'''
from urllib import request
import re


class Spider():

    url = 'https://www.panda.tv/cate/pubg?pdt=1.24.s1.19.viu4jaqhfv'
    root_pattern = '<div class="video-info">([\w\W]*?)</div>'
    name_pattern = '</i>([\w\W]*?)</span>'
    num_pattern = '<span class="video-number">([\w\W]*?)</span>'

    def __fetch_content(self):
        r = request.urlopen(Spider.url)
        html = r.read()
        html = str(html,encoding='utf-8')
        return html

    def __analysis(self,html):
        ress = re.findall(Spider.root_pattern,html)
        relists = []
        for res in ress:
            result_name = re.findall(Spider.name_pattern,res)
            name = result_name[0].strip()
            result_num = re.findall(Spider.num_pattern,res)
            dic = {'name': name,'number':result_num}
            relists.append(dic)
        return relists

    def __refine(self,relists):
        l = lambda relist: {
            "name": relist["name"],
            "number": relist["number"][0]
        }
        return map(l, relists)

    def __sort_seed(self,relist):
        r = re.findall('\d*',relist["number"])
        number = int(r[0])
        if "万" in relist["number"]:
            number *= 10000
        return number


    def __my_sort(self,relists):
        return sorted(relists, key=self.__sort_seed,reverse=True)

    def __print_result(self,relists):
        count = 0
        for relist in relists:
            number = str(relist["number"])
            count+= 1
            print("第"+str(count)+"名:"+relist["name"]+"*******"+number+"人观看")

    def go(self):

        html = self.__fetch_content()
        relists = self.__analysis(html)
        relists = list(self.__refine(relists))
        relists = self.__my_sort(relists)
        self.__print_result(relists)


spider = Spider()
spider.go()