import scrapy  
import bs4
import re
import json
import requests
from ..items import XiechengItem


class XiechengSpider(scrapy.Spider):
    name = 'xiecheng'
    allowed_domains = ['www.ctrip.com','you.ctrip.com','gs.ctrip.com']
    start_urls = []
    for page in range(1,1993):      #测试：2页即可，实际需要（1,1993）
        url = 'https://you.ctrip.com/travels/japan100041/t3-p'+str(page)+'.html'
        start_urls.append(url)

    def parse(self, response):
        bs = bs4.BeautifulSoup(response.text, 'html.parser')
        url_list = bs.find('div',class_='journalslist cf')
        url = url_list.find_all('a',class_='journal-item cf')
        for u in url:
            note_link = u['href']
            url = 'https://you.ctrip.com{id}'
            real_url = url.format(id=note_link)
            yield scrapy.Request(real_url, callback=self.parse_note)

    def parse_note(self, response):
        bs = bs4.BeautifulSoup(response.text, 'html.parser')
        bs1 = bs.decode('utf-8')
        
        # 取出该函数的根网址
        # 匹配根网址中的两个参数
        # 带参数请求url并json
        # 从json中匹配liked、views和comments
        url_running = re.findall(r'you/travels/(.*?)/(.*?).html',bs1)[0]
        url_left = url_running[0]
        url_right = url_running[1]
        #游记链接
        link = 'https://gs.ctrip.com/html5/you/travels/{}/{}.html'.format(url_left,url_right)
        #游记链接
        url_here = 'https://you.ctrip.com/TravelSite/Home/GetBusinessData'
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'}
        params = {
            'random': '0.06257961784435673',
            'arList[0].RetCode': '0',
            'arList[0].Html': url_right,
            'arList[1].RetCode': '1',
            'arList[1].Html': url_right,
            'arList[2].RetCode': '2',
            'arList[2].Html': url_right,
            'arList[3].RetCode': '3',
            'arList[3].Html': url_left
            }
        res_url = requests.get(url_here,headers=headers,params=params)
        json_res = res_url.json()
        json_str = json.dumps(json_res)  #把字典转换成字符串
        liked_re = re.findall('LikeCount(.*?),',json_str)   #[1][3:]
        liked_len = len(liked_re)
        if liked_len==int(0):
            liked = 'N'
        else:
            liked = liked_re[liked_len-1][3:]
        views = re.findall('VisitCount(.*?),',json_str)[0][3:]
        comments = re.findall('CommentCount(.*?),',json_str)[0][3:]
        print(liked,comments,views)

        res_link = requests.get(link,headers=headers,params=params)
        web_2 = bs4.BeautifulSoup(res_link.text,'html.parser')
        #note_time\user\user_gender
        note_time = web_2.find('div',class_='count date')
        note_time = note_time.text
        if note_time:
            note_time = str(note_time)
        else:
            note_time = 'N'
        print(note_time)
        
        user = web_2.find('div',class_='author user_header_no_card')
        user = user.text
        if user:
            user = str(user)
        else:
            user = 'N'
        print(user) 

        user_link = bs.find('a',class_='user_img')['href']
        if user_link:
            user_link = str(user_link)
            print(user_link)
        else:
            print('fuck you')
        data = {'id':'2803978',
        'status':'0'}
        user_url = 'https://you.ctrip.com{id}'
        gender_url = user_url.format(id=user_link)
        gender_res = requests.post(gender_url,data=data)
        web_3 = bs4.BeautifulSoup(gender_res.text,'html.parser')
        user_gender = web_3.find('span',class_='J_gender')
        user_gender = user_gender.find('i')['title']
        if user_gender:
            user_gender = str(user_gender[0])
        else:
            user_gender = 'N'
        print(user_gender)
        # res_link = requests.get(link,headers=headers)


        #title游记题目
        title_1 = web_2.find('div',class_='title')
        title = title_1.text.strip()
        # title_re = re.findall('-.*?】',title_1)
        # title = title_1.strip(str(title_re))
        print(title)
   
        #days\travel_time\per_capital_spending\with_whom\plays
        days = re.findall('天数：(.*?)天',bs1)
        # days = bs2.find('div',class_='out_days').text
        if days:
            days = str(days[0])
        else:
            days = 'N'
        print(days)
        travel_time = re.findall('时间：(.*?)月',bs1)
        # travel_time = bs2.find('div',class_='start_date').text
        if travel_time:
            travel_time = str(travel_time[0])
        else:
            travel_time = 'N'
        print(travel_time)
        per_capital_spending = re.findall('人均：(.*?)元',bs1)
        # per_capital_spending = bs2.find('div',class_='aver_cost').text.strip()
        if per_capital_spending:
            per_capital_spending = str(per_capital_spending[0])
        else:
            per_capital_spending = 'N'
        print(per_capital_spending)
        with_whom = re.findall('和谁：(.*?)</span>',bs1,re.S)
        # with_whom = bs2.find('div',class_='whom_with').text.strip()
        if with_whom:
            with_whom = str(with_whom[0]).strip()
        else:
            with_whom = 'N'
        print(with_whom)
        plays = re.findall('玩法：(.*?)</span>', bs1, re.S)
        if plays:
            plays = str(plays[0]).strip()
        else:
            plays = 'N'
        print(plays)

        # content = 'N'
        # # content_ = []
        # # content_div = web_2.find('div',class_='travels_detail').find_all('p')
        # # for con_p in content_div:
        # #     if con_p:
        # #         con_p = con_p.text.strip()
        # #         content_.append(con_p)
        # #     else:
        # #         continue

        # # content = "".join(content_)


        # #解决openpyxl.utils.exceptions.IllegalCharacterError报错问题
        # ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
        # content = ILLEGAL_CHARACTERS_RE.sub(r'', content)
        #解决openpyxl.utils.exceptions.IllegalCharacterError报错问题

        item = XiechengItem()
        #实例化XiechengItem这个类
        item['note_time'] = note_time
        item['title'] = title
        item['user'] = user
        item['days'] = days
        item['travel_time'] = travel_time
        item['per_capital_spending'] = per_capital_spending
        item['with_whom'] = with_whom
        item['plays'] = plays
        item['liked'] = liked
        item['comments'] = comments
        item['views'] = views
        # item['content'] = content
        item['link'] = link
        item['user_gender'] = user_gender
        yield item
            # 用yield语句把item传递给引擎
