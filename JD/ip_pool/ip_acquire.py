from urllib import request
import requests
from bs4 import BeautifulSoup
from lxml import etree
import threading, socket, random
import json
import time
import threading

def get_ips(url):
	headers = {
				'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
				'Accept-Encoding':'gzip, deflate',
				'Accept-Language':'zh-CN,zh;q=0.8',
				'Cache-Control':'no-store',
				'Connection':'keep-alive',
				'Host':'www.xicidaili.com',
				'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
				}
	S = requests.Session()
	req = S.get(url=url, headers=headers)
	req.encoding = 'utf-8'
	html = req.text
	soup = BeautifulSoup(html, 'lxml')
	tr_soups = soup.find('table',id='ip_list').find_all('tr')
	del tr_soups[0]
	for tr_soup in tr_soups:
		protocol = tr_soup.find_all('td')[5].text
		ip = tr_soup.find_all('td')[1].text
		port = tr_soup.find_all('td')[2].text
		ip_single = {protocol.lower(): ip + ":" + port} #是一个字典?
		print(ip_single)
		lock.acquire()
		ip_list.append(ip_single)
		lock.release()
	# print('共有%d个ip' % len(ip_list))
	

if __name__ == '__main__':
	lock = threading.Lock()
	threads = []
	ip_list = []
	for i in range(1, 11):
		url = 'http://www.xicidaili.com/nn/' + str(i)
		thread = threading.Thread(target=get_ips, args=(url, ))
		threads.append(thread)
	for thread in threads:
		thread.start()
		time.sleep(1)
	for thread in threads:
		thread.join()
	print('共有%d个ip' % len(ip_list))
	with open('ip_pool.txt', 'w') as f:
		json.dump(ip_list, f)
