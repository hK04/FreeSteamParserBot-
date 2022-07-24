import requests
import sqlite3 
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent

def get_html():
	# add an user agent
	# add url
	url = 'https://freesteam.ru/'
	# get a html
	r = requests.get(url)
	return r.text


def pars_html(html):
	# open html in re and seek for key
	soup = bs(html, "lxml")
	answer = []
	urls = []
	img_srcs = []
	texts = []
	ans = soup.find_all('a',rel="bookmark");
	i = 0;
	for j in ans:
		if i%3 ==0:
			answer.append(j.text)
			urls.append(j.get('href'))
		i += 1;
	ans = soup.find_all(class_='attachment-banner-small-image size-banner-small-image wp-post-image');
	for j in ans:
		img_srcs.append(j.get('src'))
	ans = soup.find_all('p')
	for j in ans:
		texts.append(j.text) 
	texts = texts[1::]
	return answer[::-1],urls[::-1],img_srcs[::-1],texts[::-1]

def db_work(answer,urls,img_srcs,texts):
	conn = sqlite3.connect('results.db')
	cursor = conn.execute("SELECT MAX(ID) FROM RESULTS")
	for i in cursor:
		x=i;
		break
	if x[0]==None:
		x = 0;
	else:
		x = x[0] + 1
	print(x)
	for i in range(len(answer)):
		conn.execute(
				"INSERT INTO RESULTS (ID, _TEXT_, _LINK_, _IMG_)\
				VALUES({0},'{1}','{2}','{3}')".format(i+x,answer[i],urls[i],img_srcs[i])
				)
		conn.commit()
	conn.close()	

def get_p():
	html = get_html()
	answer, urls, img_srcs, texts  = pars_html(html)
	print(len(answer))
	print(len(urls))
	print(len(img_srcs))
	print(len(texts))
	db_work(answer, urls, img_srcs, texts)

get_p()