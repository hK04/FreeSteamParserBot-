import requests
from bs4 import BeautifulSoup as bs
	
class Parser():
	def __init__(self):
		self.url = 'https://freesteam.ru/'
	def update_html(self):
		html = requests.get(self.url)
		return html.text
	def pars_html(self,html):
		soup = bs(self.update_html(), "lxml")
		ans = soup.find('a',rel="bookmark")
		ur_l = ans.get('href')
		ans = ans.text
		img_src = soup.find(class_='attachment-banner-small-image size-banner-small-image wp-post-image').get('src');
		tex_t = soup.find('p').find_next('p').text
		return ans,ur_l,img_src,tex_t
	def check(self,URL):
		try:
			with open('last_check.txt', 'r') as t:
				link = t.read() 
		except:
			link = ''
		if link != URL:
			with open('last_check.txt', 'w') as t:
				t.write(URL)
			return(True)
		else:
			return(False)
	def update_and_check(self):
		html = self.update_html()
		a,u,i,t = self.pars_html(html)
		if self.check(u):
			return(True,a,u,i,t)
		else:
			return(False,'','','','')
