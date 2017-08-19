#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests, threading, codecs, time
from lxml import etree


# 爬取IP
class GetIP(threading.Thread):
    def __init__(self, url, which):
        threading.Thread.__init__(self)
        self.daemon = True
        self.url = url
        self.which = which

    def get_ip(self):
        headers = {'Connection': 'keep-alive',
                   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
        try:
            response = requests.get(self.url, headers=headers, timeout=10)
            html = etree.HTML(response.text)
            print('[{}] {}'.format(response.status_code, self.url))
            if response.status_code == 200:
                # 对不同的网址进行爬取
                if self.which is 'xici':
                    for tr in html.xpath('//tr[contains(@class, *)]'):
                        allIP.append('{}:{}'.format(tr.xpath('./td/text()')[0],
                                                    tr.xpath('./td/text()')[1]))
                else:
                    for tr in html.xpath('//tbody/tr'):
                        allIP.append('{}:{}'.format(tr.xpath('./td[contains(@data-title, "IP")]/text()'),
                                                    tr.xpath('./td[contains(@data-title, "PORT")]/text()')))
        except Exception as e:
            print('[!]Request error: {}'.format(e))

    def run(self):
        self.get_ip()


# 验证IP可用性
class CheackIp(threading.Thread):
    def __init__(self, ip_list):
        threading.Thread.__init__(self)
        self.daemon = True
        self.ip_list = ip_list

    def check_ip(self):
        for ip in self.ip_list:
            proxy = {'http': ip, 'https': ip}
            try:
                response = requests.get('http://ip.chinaz.com/getip.aspx', proxies=proxy, timeout=5)
                if response.status_code == 200:
                    print('[ok] {}'.format(ip))
                    usefulIP.append(ip)
            except:
                pass

    def run(self):
        self.check_ip()


def run_spider_threads():
    nums = 5
    # 4页
    xici = ['http://www.xicidaili.com/nn/{}'.format(i) for i in range(1, nums)]
    kuai = ['http://www.kuaidaili.com/free/inha/{}/'.format(i) for i in range(1, nums)]
    threads = []
    for i in range(len(kuai)):
        threads.append(GetIP(xici[i], 'xici'))
        threads.append(GetIP(kuai[i], 'kuai'))
    for i in range(len(threads)):
        threads[i].start()
        # 快代理会ban访问太快的，只好等待2.5秒
        # 西刺会禁止同IP的多次爬取，所以一天不要爬太多次
        time.sleep(2.5)
    for i in range(len(threads)):
        threads[i].join()


def run_check_threads():
    print('[!]Total crawling %d ip' % len(allIP))
    x = int(len(allIP)/25)
    # 对IP切片，给不同的线程分发任务
    threads = [CheackIp(allIP[x*i:x*(i+1)]) for i in range(25)]
    for i in range(len(threads)):
        threads[i].start()
    print('[*]Start threads: {}'.format(threading.activeCount()))
    for i in range(len(threads)):
        threads[i].join()
    print('[*]End threads: {}'.format(threading.activeCount()))


def write():
    with codecs.open('ipool.txt', 'wb', encoding='utf-8') as f:
        for i in usefulIP:
            f.writelines(i + '\n')
    print('[!]These ip stored in ipool.txt')


if __name__ == '__main__':
    allIP = []
    run_spider_threads()
    usefulIP = []
    run_check_threads()
    write()
