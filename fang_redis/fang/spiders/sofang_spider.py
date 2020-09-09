import scrapy
from lxml import etree
import re
from fang.items import NewHouseItem, OldHouseItem

from scrapy_redis.spiders import RedisSpider

class SofangSpiderSpider(RedisSpider):
    name = 'sofang_spider'
    allowed_domains = ['fang.com']
    # start_urls = ['http://www.fang.com/SoufunFamily.html']
    redis_key = "fang:start_url"
    def parse(self, response):
        """主解析爬虫"""
        # 获取tr元素列表
        html = etree.HTML(response.text)
        tr_list = html.xpath('//*[@id="senfe"]//tr')
        # print(tr_list)
        # 获取所有城市以及所属的省份
        prov_out = ""
        for tr in tr_list:
            provs = tr.xpath('./td//strong/text()')
            # 当获取到strong标签并且标签内容存在
            if provs and provs[0].strip():
                prov_out = provs[0]
            # 获取城市
            if prov_out != "其它":
                a_list = tr.xpath('./td[3]//a')
                for a in a_list:
                    city = a.xpath('./text()')[0]
                    url = a.xpath('@href')[0]
                    # 构造新房的链接
                    url_new = url+"house/s"
                    url_new = url_new.replace(".",".newhouse.",1)
                    # 构造旧房的链接
                    url_old = url.replace(".",'.esf.',1)
                    print(url_old)
                    # print(prov_out,city, url_new, url_old)

                    yield scrapy.Request(url=url_new, callback=self.parse_new,
                                         meta={'info':(prov_out, city)})

                    yield scrapy.Request(url=url_old, callback=self.parse_old,
                                         meta={'info': (prov_out, city)})


    def parse_new(self, response):
        """新房链接爬虫"""
        province,city = response.meta.get('info')
        html = etree.HTML(response.text)
        li_list = html.xpath('//div[@id="newhouse_loupai_list"]//li')
        # print(li_list)
        for li in li_list:
            detail = li.xpath('.//div[@class="nlc_details"]')
            if detail:
                # 名字
                name = detail[0].xpath(".//div[@class='nlcd_name']/a/text()")[0].strip()
                url = detail[0].xpath(".//div[@class='nlcd_name']/a/@href")[0]
                # 房间
                rooms = detail[0].xpath('.//div[@class="house_type clearfix"]//text()')
                rooms = "".join(rooms)
                rooms = "".join(rooms.split())
                # 判断rooms是否含有居平米等关键字
                if rooms.find("居") != -1 and rooms.find("平米") != -1:
                    room = rooms.split("－")[0]
                    area = rooms.split("－")[1]
                else:
                    room = rooms
                    area = rooms
                # 价格
                price = detail[0].xpath('.//div[@class="nhouse_price"]//text()')
                price = "".join(price)
                price = "".join(price.split())
                # 详细地址
                address = detail[0].xpath(".//div[@class='address']/a/@title")[0]
                # print(type(rooms))
                # district
                district = detail[0].xpath(".//div[@class='address']/a//text()")
                district = "".join("".join(district).split()).split("]")[0]+"]"
                #status
                status = detail[0].xpath(".//div[@class='fangyuan']//text()")
                status = "".join(status).split()
                type = "/".join(status[1:-1])
                status = status[0]
                newhouse_item = {}
                newhouse_item['new'] = NewHouseItem(province=province, city= city, name=name,
                             price=price,rooms = room,area=area,address=address,
                             district=district,status=status,type=type,url=url)
                yield newhouse_item
        next_url = html.xpath('//div[@class="page"]//a[@class="next"]/@href')
        if next_url :
            print("当前url",response.url)
            print("要返回的url:",next_url[0])
            if next_url[0].find("http") == -1:
                base_url = response.url.split("/house")[0]
                next_url = base_url+next_url[0]
            else:
                print("不包含http的链接",next_url)

            print(next_url)
            yield scrapy.Request(url=next_url, callback=self.parse_new, meta={'info': (province, city)})


    def parse_old(self,response):
        """旧房链接爬虫"""
        province, city = response.meta.get('info')
        html = etree.HTML(response.text)
        print("当前url:", response.url)
        dl_list = html.xpath('//div[@class="shop_list shop_list_4"]/dl')
        if dl_list:
            for dl in dl_list:

                # name
                name = dl.xpath('.//h4[@class="clearfix"]//text()')
                name = "".join("".join(name).split())
                # room
                rooms = dl.xpath(".//p[@class='tel_shop']//text()")
                rooms = "".join("".join(rooms).split())
                room = rooms.split("|")[0]
                # are
                area = rooms.split("|")[1]
                # floor
                floor = rooms.split("|")[2]
                # orient
                orient = rooms.split("|")[3]
                # data
                data = rooms.split("|")[4]
                # owner
                owner = rooms.split("|")[5]
                # address
                address = dl.xpath(".//p[@class='add_shop']//text()")
                address = "".join(address).split()
                # location
                location = address[0]
                address = address[1]
                # price
                price = dl.xpath(".//dd[@class='price_right']//text()")
                price = "".join(price).split()
                average_price = price[1]
                price = price[0]
                item = {}
                item['old'] = OldHouseItem(province=province, city=city,name=name, room=room, area= area, floor=floor,
                                    orient=orient, data=data, owner=owner, address=address,
                                    location=location, price=price, average_price=average_price)
                yield item

        next_url = html.xpath("//div[@class='page_box']//p")
        print(next_url)
        if next_url:
            next_url = next_url[0].xpath("./a/@href")
            print("获取到了下一页的url",next_url)
            base_url = response.url.replace('com/','com')
            next_url = base_url+next_url[0]
            print("下一页的url:", next_url)
            yield scrapy.Request(url=next_url,  callback=self.parse_old, meta={'info': (province, city)})



