# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import openpyxl

class XiechengPipeline(object):
    def __init__(self):
        #初始化函数 当类实例化时这个方法会自启动
            self.wb =openpyxl.Workbook()
            #创建工作薄
            self.ws = self.wb.active
            #定位活动表
            self.ws.append(['游记链接','游记时间','标题', '用户', '用户性别','天数（天）', '时间（月）','人均开销（元）','和谁一起','玩法','喜欢数','评论数','浏览数'])#'游记内容'
            #用append函数往表格添加表头

    def process_item(self, item, spider):
    #process_item是默认的处理item的方法，就像parse是默认处理response的方法
        line = [item['link'], item['note_time'], item['title'], item['user'],item['user_gender'], item['days'], item['travel_time'], item['per_capital_spending'], item['with_whom'], item['plays'], item['liked'], item['comments'], item['views']]#item['content']
        #把公司名称、职位名称、工作地点和招聘要求都写成列表的形式，赋值给line
        self.ws.append(line)
        #用append函数把公司名称、职位名称、工作地点和招聘要求的数据都添加进表格
        return item
        #将item丢回给引擎，如果后面还有这个item需要经过的itempipeline，引擎会自己调度

    def close_spider(self, spider):
    #close_spider是当爬虫结束运行时，这个方法就会执行
        self.wb.save('./Travel_Notes_JP0718.xlsx')
        #保存文件
        self.wb.close()
        #关闭文件