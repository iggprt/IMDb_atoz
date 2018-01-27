import imdblib
import csv
import crawler
import sql

f = open ("./Testing/WATCHLIST.csv", "r")
g = open ("./Testing/actors.csv", "r")

csvreader = csv.reader(f)
csvreader_g = csv.reader(g)

sql.create_tables()


#print (sql.find_actor('3'))
"""
for row in csvreader_g:
	source = crawler.get_source(row[0])
	actor = imdblib.Actor(source)

	print (actor.name)
"""

for row in csvreader:
	if sql.movie_exists(imdblib.strip_ID(row[0])) == 0:
		source = crawler.get_source(row[0])
		movie = imdblib.Title(source)

		print (movie.title)
		sql.add_movie(movie)

