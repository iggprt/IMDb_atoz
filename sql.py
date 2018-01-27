import sqlite3
import imdblib
import crawler

conn = sqlite3.connect('IMDb.db')
conn.text_factory = str
c = conn.cursor()

def create_tables():

	c.execute("""CREATE TABLE IF NOT EXISTS movie_tab (movie_id primary key, name, year integer, runtime integer, genre, content_rating, 
		rating real, storyline, original_title, budget, directors, writers, actors, metascore integer, oscars integer)""")
	c.execute("""CREATE TABLE IF NOT EXISTS actors_tab (actor_id primary key, name, 
		birthdate, deathdate, birthplace, jobs, oscars integer, films_played integer, films_directed integer, films_written integer, films_total integer)""")		
	c.execute("""CREATE TABLE IF NOT EXISTS genres_movie_tab (bind_id integer primary key AUTOINCREMENT, movie_id, genre)""")
	c.execute("""CREATE TABLE IF NOT EXISTS actors_movie_tab (bind_id integer primary key autoincrement, movie_id, actor_id)""")
	c.execute("""CREATE TABLE IF NOT EXISTS directors_movie_tab (bind_id integer primary key autoincrement, movie_id, director_id)""")
	c.execute("""CREATE TABLE IF NOT EXISTS writers_movie_tab (bind_id integer primary key autoincrement, movie_id, writer_id)""")

def movie_exists(id_mov):
	c.execute("""SELECT name
		FROM movie_tab
		WHERE movie_id = :id""",{
		'id': id_mov})
	result = c.fetchall()

	if result == []:
		return 0
	else:
		return 1
	


def actor_exists(id_act):
	c.execute("""SELECT name
		FROM actors_tab
		WHERE actor_id = :id""",{
		'id': id_act})
	result = c.fetchall()

	if result == []:
		return 0
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

def films_total(id_act):
	c.execute("""SELECT films_total
		FROM actors_tab
		WHERE actor_id = :id""",{
		'id': id_act})
	result = c.fetchall()
	if result == []:
		return -1 
	else:
		return result[0][0]


def add_movie(movie):
	# i gotta do something with this. the code is too long. i gotta do function for all the inserts. 
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
		   # create the Actor object 

		c.execute("""INSERT INTO actors_movie_tab (actor_id, movie_id) values(:a_id, :m_id)""",{
			'a_id':actor[1],
			'm_id':movie.movieID})

		if actor_exists(actor[1]):
			c.execute("""UPDATE actors_tab
				SET films_played = :played, films_total = :total
				WHERE actor_id = :id""",{
				'played': films_act(actor[1]) + 1,
				'total': films_total(actor[1]) + 1,
				'id': actor[1] 
 				})
		else:
			dude = imdblib.Actor(crawler.get_source('http://www.imdb.com/name/' + actor[1] + '/'))
			c.execute("""INSERT INTO actors_tab (actor_id, name, birthdate, deathdate, birthplace, jobs, oscars, films_played, films_directed, films_written, films_total)
				VALUES(:id, :name, :birthdate, :deathdate, :birthplace, :jobs, :oscars, :films_played, :films_directed, :films_written, :films_total)""",{
				'id':actor[1],
				'name': actor[0],    #dont work
				'birthdate': dude.birthDate,
				'deathdate': dude.death,
				'birthplace': imdblib.display_list(dude.birthPlace),
				'jobs': imdblib.display_list(dude.jobs),    # dont work
				'oscars': dude.oscars,
				'films_played': 1,
				'films_directed': 0,
				'films_written': 0,
				'films_total': 1
				})

	genres = movie.genre
	for genre in genres:
		c.execute("""INSERT INTO genres_movie_tab (movie_id, genre)
			VALUES (:movie_id, :genre)""",{
			'movie_id': movie.movieID,
			'genre': genre
			})

	directors = movie.directors
	for director in directors:

		c.execute("""INSERT INTO directors_movie_tab (director_id, movie_id) values(:d_id, :m_id)""",{
			'd_id':director[1],
			'm_id':movie.movieID})

		if actor_exists(director[1]):
			c.execute("""UPDATE actors_tab
				SET films_directed = :directed, films_total = :total
				WHERE actor_id = :id""",{
				'directed': films_dir(director[1]) + 1,
				'total': films_total(director[1]) + 1,
				'id': director[1] 
 				})
		else:
			dude = imdblib.Actor(crawler.get_source('http://www.imdb.com/name/' + director[1] + '/'))
			c.execute("""INSERT INTO actors_tab (actor_id, name, birthdate, deathdate, birthplace, jobs, oscars, films_played, films_directed, films_written, films_total)
				VALUES(:id, :name, :birthdate, :deathdate, :birthplace, :jobs, :oscars, :films_played, :films_directed, :films_written, :films_total)""",{
				'id':director[1],
				'name': director[0], 
				'birthdate': dude.birthDate,
				'deathdate': dude.death,
				'birthplace': imdblib.display_list(dude.birthPlace),
				'jobs': imdblib.display_list(dude.jobs),
				'oscars': dude.oscars,
				'films_played': 0,
				'films_directed': 1,
				'films_written': 0,
				'films_total': 1
				})


	writers = movie.writers
	for writer in writers:

		c.execute("""INSERT INTO writers_movie_tab (writer_id, movie_id) values(:w_id, :m_id)""",{
			'w_id':writer[1],
			'm_id':movie.movieID})

		if actor_exists(writer[1]):
			c.execute("""UPDATE actors_tab
				SET films_written = :written, films_total = :total
				WHERE actor_id = :id""",{
				'written': films_writ(writer[1]) + 1,
				'total': films_total(writer[1]) + 1,
				'id': writer[1] 
 				})
		else:
			dude = imdblib.Actor(crawler.get_source('http://www.imdb.com/name/' + writer[1] + '/'))
			c.execute("""INSERT INTO actors_tab (actor_id, name, birthdate, deathdate, birthplace, jobs, oscars, films_played, films_directed, films_written, films_total)
				VALUES(:id, :name, :birthdate, :deathdate, :birthplace, :jobs, :oscars, :films_played, :films_directed, :films_written, :films_total)""",{
				'id':writer[1],
				'name': writer[0], 
				'birthdate': dude.birthDate,
				'deathdate': dude.death,
				'birthplace': imdblib.display_list(dude.birthPlace),
				'jobs': imdblib.display_list(dude.jobs),
				'oscars': dude.oscars,
				'films_played': 0,
				'films_directed': 0,
				'films_written': 1,
				'films_total': 1
				})

	conn.commit()


