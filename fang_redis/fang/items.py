# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class NewHouseItem(scrapy.Item):
    """新房item类"""
    # 省份
    province = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 住宅名字
    name = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 几居室
    rooms = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 详细地址
    address =scrapy.Field()
    # 行政区县城
    district = scrapy.Field()
    # 是否在售
    status = scrapy.Field()
    # 住宅类型
    type = scrapy.Field()
    # 详情页面的url
    url = scrapy.Field()

class OldHouseItem(scrapy.Item):
    """二手房item类"""
    # 省份
    province =scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 名称
    name = scrapy.Field()
    # 房间
    room = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 层数
    floor = scrapy.Field()
    # 朝向
    orient = scrapy.Field()
    # 建成日期
    data = scrapy.Field()
    # owner
    owner =scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 位置
    location = scrapy.Field()
    # price
    price = scrapy.Field()
    # average_price
    average_price = scrapy.Field()



