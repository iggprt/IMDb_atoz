 
"""Library containing the two classes"""



from bs4 import BeautifulSoup
import requests
import re
import time

def strip_ID(link):
	pattern = re.compile(r'((tt|nm)[0-9]{7})')
	matches = pattern.findall(link)
	if matches != []:
		return matches[0][0]
	else:
		return "__ID_Error__"


class Title():

	def __init__(self, source):
		self.source = source
		self.soup = BeautifulSoup ( source, "lxml" )


	@property
	def title(self):   #todo - do something about the tv movies
		
		matches = self.soup.find_all('meta', property='og:title')
		if matches != []:
			return matches[0].get('content')[:-7]
		else:
			return "__NameError__"

	@property
	def movieID(self):
		matches = self.soup.find_all('div', class_="ribbonize" )
		if matches != []:
			return matches[0].get('data-tconst')
		else:
			return "__ID_Error__"

	@property
	def titleYear(self):

		matches = self.soup.find_all('span', id='titleYear')

		if matches != []:
			return int(matches[0].text[1:-1])
		else:
			return "__YearError__"


	@property
	def genre(self):

		matches = self.soup.find_all('span', itemprop='genre')

		if matches != []:
			for i in range(len(matches)):
				matches[i] = matches[i].text
			return matches
		else:
			return "__GenreError__"

	@property
	def contentRating(self):
		""" There is a problem with that. It doesn't work for Scarface and some other movies"""


		matches = self.soup.find_all('meta', itemprop='contentRating')
		#matches = self.soup.find_all('span', itemprop='contentRating')

		if matches != []:
			return matches[0].get('content')
		else:
			#pattern = re.compile(r'contentRating">(.+)<')
			#pattern = re.compile(r'g">(.+)</span')
			#pattern = re.compile(r'content="(.+)">')
			#matches = pattern.findall(self.source)
			return "__RatedError__" + self.title# + str(matches) + str(len(matches))


	@property
	def ratingValue(self):

		matches = self.soup.find_all('span', itemprop='ratingValue')
		match = float(matches[0].text.replace(".",""))/10

		if matches != []:
			return match
		else:
			return "__ratingValueError__ "+self.name

	@property
	def ratingCount(self):

		matches = self.soup.find_all('span', itemprop='ratingCount')
		match = int(matches[0].text.replace(",",""))

		if matches != []:
			return match
		else:
			return "__ReviewsError__ "+self.name


	@property
	def runtime(self):

		matches = self.soup.find_all('time', itemprop = 'duration')
		match = int(matches[0].get('datetime')[2:-1])

		if matches != []:
			return match
		else:
			return "__runtimeError__ "+self.name


	@property
	def storyline(self):

		matches = self.soup.find_all('div', itemprop = 'description')

		if matches != []:
			return matches[0].text.strip()
		else:
			return "__StoryLineError__"


	@property
	def originalTitle(self):

		matches = self.soup.find_all('div', class_ = 'originalTitle')

		if matches != []:
			if matches[0].text[:-17] != self.title:
				return matches[0].text[:-17]
			return None
		else:
			return None


	@property
	def budget(self):

		pattern = re.compile(r'Budget:<\/h4>(.+)')
		pattern = re.compile(r'Budget:(.+)')

		match = pattern.findall(self.source)
		if match != []:
			match[0] = re.sub(' ','',match[0]) 
		else:
			return 0

		return match[0][5:]


	@property
	def directors(self):

		start = self.source.find('"inline">Director')
		fin = self.source.find('"inline">Writer')
		section = self.source[start: fin]

		soup_sect = BeautifulSoup(section, 'lxml')

		matches = soup_sect.find_all('a', itemprop = 'url')
		matches = [[match.text, strip_ID(match.get('href'))] for match in matches]

		if matches != []:
			return matches
		else:
			return "__DirectorError__"


	@property
	def writers(self):

		start = self.source.find('"inline">Writer')
		fin = self.source.find('"inline">Star')
		section = self.source[start: fin]

		soup_sect = BeautifulSoup(section, 'lxml')

		matches = soup_sect.find_all('a', itemprop = 'url')
		matches = [[match.text, strip_ID(match.get('href'))] for match in matches]

		if matches != []:
			return matches
		else:
			return "__WriterError__"


	@property
	def actors(self):

		start = self.source.find('class="cast_list"')
		fin = self.source.find('See full cast</a>')
		section = self.source[start: fin]

		soup_sect = BeautifulSoup(section, 'lxml')

		matches = soup_sect.find_all('a', itemprop = 'url')
		matches = [[match.text[:-1], strip_ID(match.get('href'))] for match in matches]

		if matches != []:
			return matches
		else:
			return "__ActorError__"


	@property
	def oscars(self):
		matches = self.soup.find_all('span', itemprop = 'awards')
		string = re.sub(r'[\n\s]+','',matches[0].text)
		pattern = re.compile(r'Won(\d+)(Oscar|oscar)')
		match = pattern.findall(string)
		if match != []:
			return match[0][0]
		else:
			return 0


	@property
	def metascore(self):
		matches = self.soup.find_all('div', class_ = 'metacriticScore score_favorable titleReviewBarSubItem')
		
		if matches != []:
			return int(matches[0].text[1:-1])
		else:
			return -1 
		

	@property
	def productionCo(self):
		pass




class Actor():
	"""docstring for ClassName"""

	def __init__(self, source):

		self.source = source
		self.soup = BeautifulSoup ( self.source,"lxml" )

		#self.biosource = requesets.get(link+'bio/')
		#self.biosoup = BeautifulSoup (self.biosource, 'lxml')

	@property
	def name(self):

		name = self.soup.find_all('span', itemprop = 'name')[0].text

		return  name

	@property
	def birthDate(self):

		birth = self.soup.find_all('time', itemprop ='birthDate')
		if birth == []:
			return 'n/a'
		else :
			return birth[0].get('datetime')
		return birth

	@property
	def birthPlace(self):

		birthplace = self.soup.find_all('div', id = 'name-born-info')
		if birthplace == []:
			return 'n/a'
		else:
			birthplace = birthplace[0].find_all('a')
			if len(birthplace) < 3:
				birthplace = birthplace[0].text
				birthplace = birthplace.strip().split(', ')
			else:
				birthplace = birthplace[2].text
				birthplace = birthplace.strip().split(', ')
		

		return birthplace

	@property
	def jobs(self):
		jobs = self.soup.find_all('span', itemprop = 'jobTitle')
		jobs = [job.text.strip() for job in jobs]

		return jobs 


	@property
	def death(self):
		death = self.soup.find_all('time', itemprop ='deathDate')
		if death == []:
			death = 'n/a'
		else:
			death = death[0].get('datetime')

		return death

	@property
	def oscars(self):
		oscars = self.soup.find_all('span', itemprop = 'awards')
		if oscars == []:
			return 0
		else:
			oscars = oscars[0].text
		oscars = re.sub(r'(\n| )','',oscars)
		pattern = re.compile(r'Won([0-9])+Oscar')
		oscars = pattern.findall(oscars)
		if oscars == []:
			oscars = 0
		else:
			oscars = int(oscars[0])

		return oscars
