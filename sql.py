import sqlite3
import imdblib

conn = sqlite3.connect('IMDb.db')
conn.text_factory = str
c = conn.cursor()

def create_tables():

	c.execute("""CREATE TABLE IF NOT EXISTS movie_tab (movie_id primary key, name, year integer, runtime integer, genre, content_rating, 
		rating real, storyline, original_title, budget, directors, writers, actors, metascore integer, oscars integer)""")
	c.execute("""CREATE TABLE IF NOT EXISTS actors_tab (actor_id primary key, name, 
		birthdate, deathdate, birthplace, jobs, oscars integer, films_played integer, films_directed integer, films_written integer, films integer)""")		
	c.execute("""CREATE TABLE IF NOT EXISTS genres_movie_tab (bind_id integer primary key AUTOINCREMENT, movie_id, genre)""")
	c.execute("""CREATE TABLE IF NOT EXISTS actors_movie_tab (bind_id integer primary key autoincrement, movie_id, actor_id)""")
	c.execute("""CREATE TABLE IF NOT EXISTS directors_movie_tab (bind_id integer primary key autoincrement, movie_id, director_id)""")
	c.execute("""CREATE TABLE IF NOT EXISTS writers_movie_tab (bind_id integer primary key autoincrement, movie_id, writer_id)""")

def actor_exists(id_act):
	c.execute("""SELECT name
		FROM actors_tab
		WHERE actor_id = :id""",{
		'id': id_act})
	result = c.fetchall()

	if result == []:
		return -1
	else:
		return 1

def films_dir(id_act):
	c.execute("""SELECT films_directed 
		FROM actors_tab
		WHERE actor_id = :id""",{
		'id': id_act})
	result = c.fetchall()
	if result == []:
		return -1 
	else:
		return result[0][0]


def films_act(id_act):
	c.execute("""SELECT films_played
		FROM actors_tab
		WHERE actor_id = :id""",{
		'id': id_act})
	result = c.fetchall()
	if result == []:
		return -1 
	else:
		return result[0][0]


def films_writ(id_act):
	c.execute("""SELECT films_written
		FROM actors_tab
		WHERE actor_id = :id""",{
		'id': id_act})
	result = c.fetchall()
	if result == []:
		return -1 
	else:
		return result[0][0]


def add_movie(movie):
	c.execute("""INSERT INTO  movie_tab(movie_id, 
		name, year, runtime, genre, content_rating, rating, storyline, original_title, budget, directors, writers, actors, metascore, oscars) 
		VALUES(:id, :name, :year, :runtime, :genre, :content, :rating, :storyline, :orig, :budget, :dir, :writ, :act, :meta, :osc)""",{
		'id': movie.movieID,
		'name': movie.title,
		'year': movie.titleYear,
		'runtime': movie.runtime,
		'genre': imdblib.display_list(movie.genre),
		'content':movie.contentRating,
		'rating': movie.ratingValue,
		'storyline': movie.storyline,
		'orig': movie.originalTitle,
		'budget': movie.budget,
		'dir': imdblib.display_matrice(movie.directors),
		'writ': imdblib.display_matrice(movie.writers),
		'act': imdblib.display_matrice(movie.actors),
		'meta': movie.metascore,
		'osc': movie.oscars})

	actors = movie.actors

	for actor in actors:
		c.execute("""INSERT INTO actors_movie_tab (actor_id, movie_id) values(:a_id, :m_id)""",{
			'a_id':actor[1],
			'm_id':movie.movieID})

	if actor_exists(actor[1])
		c.execute("""INSERT INTO actors_tab( name, birthdate, deathdate, birthplace, jobs, )""")

	genres = movie.genre

	for genre in genres:
		c.execute("""insert into genre_movie_tab (genre, movie_id) values(:genre, :m_id)""",{
			'genre':genre,
			'm_id':movie.movieID})


	conn.commit()


