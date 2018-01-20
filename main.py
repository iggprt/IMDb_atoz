import imdblib
import csv
import crawler
import sql

f = open ("./Testing/WATCHLIST.csv", "r")

csvreader = csv.reader(f)

sql.create_tables()

for row in csvreader:
	source = crawler.get_source(row[0])
	movie = imdblib.Title(source)

	print (movie.title)
	#print (movie.budget)
	print (movie.actors)

	for item in movie.actors:
		act_source = crawler.get_source('http://www.imdb.com/name/' + item[1] + '/')
		actor = imdblib.Actor(act_source)
		print (actor.name) 
		print (actor.birthDate)
		print (actor.death)
		print (actor.birthPlace)
		print (actor.jobs)
		print (actor.oscars)
		print ('\n')
	print ('\n_________________________________________________')

	#sql.add_movie(movie)
