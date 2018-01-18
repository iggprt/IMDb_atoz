
import os
from bs4 import BeautifulSoup
import re

files = os.listdir('./actors')
pages = [ BeautifulSoup( open('./actors/'+file, 'r').read(),'html.parser') for file in files ]



a = []
for page in pages:

	name = page.find_all('span', itemprop = 'name')[0].text
	
	birth = page.find_all('time', itemprop ='birthDate')[0].get('datetime')
	
	birthplace = page.find_all('div', id = 'name-born-info')[0].find_all('a')[2].text
	birthplace = birthplace.strip().split(', ')
	
	jobs = page.find_all('span', itemprop = 'jobTitle')
	jobs = [job.text.strip() for job in jobs]
	
	#height = page.find_all('div', id = 'details-height' )[0].text.strip("\u02dd")
	
	death = page.find_all('time', itemprop ='deathDate')
	if death == []:
		death = 'n/a'
	else:
		death = death[0].get('datetime')
	
	oscars = page.find_all('span', itemprop = 'awards')[0].text
	oscars = re.sub(r'(\n| )','',oscars)
	pattern = re.compile(r'Won([0-9])+Oscar')
	oscars = pattern.findall(oscars)
	if oscars == []:
		oscars = 0
	else:
		oscars = int(oscars[0])
		
	
	print name
	#print birth
	#print birthplace
	#print jobs
	#print death
	print oscars
	print '\n'


