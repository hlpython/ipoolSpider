#!/usr/bin/python3
# coding=utf-8
import requests
import threading
import codecs
import json
import time
from lxml import etree


class GetIP(threading.Thread):
    def __init__(self, url, which):
        threading.Thread.__init__(self)
        self.url = url
        self.which = which

    def get_ip(self):
        time.sleep(1)
        headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }
        response = requests.get(self.url, headers=headers, timeout=5)
        response.encoding = 'utf-8'
        html = etree.HTML(response.text)
        print(self.url + ' ' + str(response.status_code))
        x = []
        if self.which is 'xici':
            for tr in html.xpath('//tr[contains(@class, *)]'):
                x.append({'ip': tr.xpath('./td/text()')[0],
                          'port': tr.xpath('./td/text()')[1],
                          'anonymity': tr.xpath('./td/text()')[4],
                          'type': tr.xpath('./td/text()')[5]})
            values['xici'] = x

        else:
            for tr in html.xpath('//tbody/tr'):
                x.append({'ip': tr.xpath('./td[contains(@data-title, "IP")]/text()')[0],
                          'port': tr.xpath('./td[contains(@data-title, "PORT")]/text()')[0],
                          'anonymity': tr.xpath('./td[contains(@data-title, "匿名度")]/text()')[0],
                          'type': tr.xpath('./td[contains(@data-title, "类型")]/text()')[0]})
            values['kuai'] = x

    def run(self):
        if threadLock.acquire():
            self.get_ip()
            threadLock.release()


def write_json():
    file = codecs.open('ipool.json', 'wb', encoding='utf-8')
    line = json.dumps(values, ensure_ascii=False)
    file.write(line)
    file.close()


def run_threads():
    for i in range(1, 4):
        xici.append('http://www.xicidaili.com/nn/%d' % i)
        kuai.append('http://www.kuaidaili.com/free/inha/%d/' % i)
    for i in range(len(kuai)):
        threads.append(GetIP(xici[i], 'xici'))
        threads.append(GetIP(kuai[i], 'kuai'))
    for i in range(len(threads)):
        threads[i].start()
    print('[*]Start active threads: %s' % threading.activeCount())
    for i in range(len(threads)):
        threads[i].join()
    print('[*]End active threads: %s' % threading.activeCount())


if __name__ == '__main__':
    xici = []
    kuai = []
    values = {}
    threads = []
    threadLock = threading.Lock()
    run_threads()
    write_json()
