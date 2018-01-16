import sqlite3
import imdblib

conn = sqlite3.connect('IMDb.db')
conn.text_factory = str
c = conn.cursor()

def create_tables():
	c.execute("CREATE TABLE IF NOT EXISTS movie_tab (movie_id primary key, name, year integer, runtime integer)")
	c.execute("CREATE TABLE IF NOT EXISTS actors_movie_bind_tab (bind_id integer primary key autoincrement, actor_id, movie_id, actor_name, movie_name )")
	c.execute("CREATE TABLE IF NOT EXISTS genre_movie_tab (bind_id integer primary key autoincrement, genre, movie_id)")


def add_movie(movie):
	c.execute("""insert into movie_tab(movie_id, name, year, runtime) values(:id, :name, :year, :runtime)""",{
		'id': movie.movieID,
		'name': movie.title,
		'year': movie.titleYear,
		'runtime': movie.runtime})

	actors = movie.actors

	for actor in actors:
		c.execute("""insert into actors_movie_bind_tab (actor_id, movie_id, actor_name, movie_name) values(:a_id, :m_id, :a_name, :m_name)""",{
			'a_id':actor[1],
			'm_id':movie.movieID,
			'a_name':actor[0],
			'm_name':movie.title})

	genres = movie.genre

	for genre in genres:
		c.execute("""insert into genre_movie_tab (genre, movie_id) values(:genre, :m_id)""",{
			'genre':genre,
			'm_id':movie.movieID})


	conn.commit()


