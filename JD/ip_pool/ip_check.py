from urllib import request
import requests
from bs4 import BeautifulSoup
from lxml import etree
import threading, socket, random
import time
import json
from ip_acquire import get_ips

'''
通过免费IP代理网站爬取IP，构建一个容量为100的代理IP池。
从代理IP池中随机选取IP，在使用IP之前，检查IP是否可用。
如果可用，使用该IP访问目标页面，如果不可用，舍弃该IP。
当代理IP池中IP的数量小于20的时候，更新整个代理IP池，
即重新从免费IP代理网站爬取IP，构建一个新的容量为100的代理IP池
def ip_test(ip):#需传入ip，不能在函数内部直接调动其他函数中定的参数！！

除此之外，我们也可以个创建一个User-Agent的列表，多罗列点。
也是跟代理IP一样，每次访问随机选取一个。这样在一定程度上，也能避免被服务器封杀。
'''
def ip_test(ip):
	# ip有效性验证
	socket.setdefaulttimeout(5) #设置全局超时时间
	url = 'https://www.baidu.com/'
	#创建proxyhandler
	proxy_support = request.ProxyHandler(ip)
	#创建opener
	opener = request.build_opener(proxy_support)
	#添加user_agent
	opener.addheaders = [
						('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'),
						('Host', 'www.jobbole.com'), 
						('Cookie','wordpress_logged_in_0efdf49af511fd88681529ef8c2e5fbf=super_super%7C1506509213%7CFhFz1N1oeutFfnhbza7zRcyQEk6faVTAxyiWVu2wLOy%7Ca033562741af2c0ebf9f98d97ee74cda70d51addf4e525ce34c32371dda1694f')
						] 
	#安装opener
	request.install_opener(opener)
	try:
		html = opener.open(url).read().decode('utf-8')
		print(ip, 'is ok')
		lock.acquire()
		ip_list_valid.append(ip)
		lock.release()
	except Exception as e:
		print(ip, e)

def check_ip(): # 不同函数的变量不能直接调用
	threads = []
	with open('ip_pool.txt', 'r') as f:
		ip_list = json.load(f)
	for i in range(len(ip_list)):
		thread = threading.Thread(target=ip_test, args=(ip_list[i],))
		threads.append(thread)
	for i in range(len(ip_list)):
		threads[i].start()
		time.sleep(0.2)
	for thread in threads:
		thread.join()

# 多线程比单线程还慢？！！？是不是写法不对？？
if __name__ == '__main__':
	# get_ips()
	start_time = time.time()
	ip_list_valid = []
	lock = threading.Lock()
	check_ip()
	print('%d ips are valid.' % len(ip_list_valid))
	end_time = time.time()
	print('多线程ip验证所花时间为：%s seconds' % (end_time-start_time))
	with open('ip_pool.txt', 'w') as f:
		json.dump(ip_list_valid, f)

# # 单线程
# start_time = time.time()
# ip_list_valid = []

# with open('ip_pool.txt', 'r') as f:
# 	ip_list = json.load(f)
# for i in range(len(ip_list)):
# 	ip_test(ip_list[i])
# print('%d ips are valid.' % len(ip_list_valid))
# end_time = time.time()
# print('单线程ip验证所花时间为：%s seconds' % (end_time-start_time))


