# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonLinesItemExporter

class FangPipeline:
    def __init__(self):
        self.fp_new = open("new.json", 'bw')
        self.exporter_new = JsonLinesItemExporter(self.fp_new, ensure_ascii=False, encoding='utf-8')
        self.fp_old = open('old.json', 'bw')
        self.exporter_old = JsonLinesItemExporter(self.fp_old, ensure_ascii=False, encoding='utf-8')

    def process_item(self, item, spider):
        old_item = item.get('old')
        new_item = item.get('new')
        if new_item:
            self.exporter_new.export_item(item)
        if old_item:
            self.exporter_old.export_item(item)
        return item

    def close_spider(self, spider):
        self.fp_new.close()
        self.fp_old.close()
