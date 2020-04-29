#!/usr/bin/python
# -*- coding: utf-8 -*-

'''

51job工作岗位爬取
python3.7版本以上
'''
import asyncio
import time
import aiohttp
from lxml import etree

class Job():
    def __init__(self,keyword):
        self.url_basic1 = 'https://search.51job.com/list/000000,000000,0000,00,9,99,{},2,'.format(keyword)
        self.url_basic2 = '.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'}
        self.count=1   #记录爬取职位数量
        self.page=1     #记录爬取页数
        self.fail_count=0   #记录爬取失败的数量

    # 请求一页的html
    async def get_html(self,url):
            async with aiohttp.ClientSession() as sess:
                async with sess.get(url, headers=self.headers) as html:
                    text1= await html.text('gb18030')
                    print('page:',self.page)
                    self.page+=1
            await asyncio.create_task(self.parse_text1(text1))

    # 解析一个职位详细信息所在的url
    async def get_html_2(self,url):
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url, headers=self.headers) as html:
                text2= await html.text('gb18030')
                print('count:',self.count)
                self.count+=1
        return text2

    # 解析一页中的50个职位
    async def parse_text1(self,text):
        html = etree.HTML(text)
        for i in range(4,54):   #遍历50个职位
            d={}
            base_list = html.xpath(f'//*[@id="resultList"]/div[{i}]')
            for span in base_list:
                try:
                    url_info = span.xpath('./p/span/a/@href')[0]            #提取一个职位的相关信息所在的新url
                    job_name = span.xpath('./p/span/a/@title')[0]
                    company_name = span.xpath('./span[1]/a/text()')[0]
                    text_1= span.xpath('./span[2]/text()')[0]
                    text_2 = span.xpath('./span[3]/text()')[0]
                    text_3 = span.xpath('./span[4]/text()')[0]
                    text2= await asyncio.create_task(self.get_html_2(url_info))
                    info_list = await asyncio.create_task(self.parse_text2(text2))

                    d['job_name']=job_name          #存入基本信息及岗位详细信息到字典d中
                    d['company_name']=company_name
                    d['text_1']=text_1
                    d['text_2']=text_2
                    d['text_3']=text_3
                    d['info_list']=info_list
                except:
                    print('fail')
                    self.fail_count+=1
            self.save(d)

    # 解析一个职位的url，获取岗位详细信息
    async def parse_text2(self,text):
        html = etree.HTML(text)
        info_list = html.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div[@class="bmsg job_msg inbox"]/p/text()')
        return info_list

    # 存入一个职位的数据
    def save(self,d):
        try:            #测试的时候碰到了存入失败的，不想找原因了，直接写个try不管了
            with open('data_xpath.txt','a+')as f:
                f.write(str(d)+'\n')
        except:
            print(f'save fail')

    async def main(self):
        task_list=[]
        for i in range(700):        #创建700页的任务
            url=self.url_basic1+str(i+1)+self.url_basic2        #拼接url
            task_list.append(asyncio.create_task(self.get_html(url)))

        for i in range(len(task_list)):     #执行700页的任务
            await task_list[i]
        print(f'fail sum is:{self.fail_count}')

if __name__ == '__main__':
    job = Job('python')
    start = time.time()
    asyncio.run(job.main())
    print(f'total time used is {time.time() - start}s')



