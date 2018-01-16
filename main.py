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

	sql.add_movie(movie)
