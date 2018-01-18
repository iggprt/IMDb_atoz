
import os
from bs4 import BeautifulSoup
import re
import HTMLParser

files = os.listdir('./htmls')
pages = [ BeautifulSoup( open('./htmls/'+file, 'r').read(),'html.parser') for file in files ]


matches = []

for page in pages:
	
	page = page.text
	
	pattern = re.compile(r'Budget:<\/h4>(.+)')
	pattern = re.compile(r'Budget:(.+)')

	match = pattern.findall(page)
	match[0] = re.sub(' ','',match[0])
	
	print match
	
	

	


