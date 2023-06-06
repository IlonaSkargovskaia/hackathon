import requests
import psycopg2


HOSTNAME = 'localhost'
USERNAME = 'postgres'
PASSWORD = '1948'
DATABASE = 'Hackathon_1'
MOVIES_TABLE_NAME = 'movies'
ACTORS_TABLE_NAME = 'actors'
RESULTS_LIMIT = 5


def run_query(query):
    connection = psycopg2.connect(host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    results = cursor.fetchall()
    connection.close()
    return results


def get_all_from_database(database):
    return run_query(f"SELECT * FROM {database};")


def print_multiple_result(results):
    if "results" in results:
        results = results["results"]

    results = results[:RESULTS_LIMIT]

    for result in results:
        {print(f"{key}: {value}") for key, value in result.items()}
        print()


def print_single_result(result):
    {print(f"{key}: {value}") for key, value in result.items()}
    print()


class Movie:

    MOVIES = get_all_from_database("movies")

    @staticmethod
    def save(movie_id, title, genres, overview, popularity, poster_path, release_date):
        try:
            return run_query(
                f"INSERT INTO {MOVIES_TABLE_NAME}(movie_id, title, genres, overview, popularity, poster_path, release_date) "
                f"VALUES ('{movie_id}', '{title}', '{genres}', '{overview}', '{popularity}', '{poster_path}', '{release_date}') "
                f"RETURNING id;")
        except psycopg2.errors.UniqueViolation:
            print("Movie with the same movie_id already exists in the database.")

    @staticmethod
    def delete(movie_id):
        if len(run_query(f"DELETE FROM  {MOVIES_TABLE_NAME} WHERE movie_id = '{movie_id}' RETURNING id;")) > 0:
            print("The movie has been deleted successfully")
        else:
            print("The movie has not been found in the database")

    @staticmethod
    def print_all():
        for movie in get_all_from_database('movies'):
            print(f"Title: {movie[2]} (ID: {movie[1]})")


class MoviesSource:

    URL = "https://api.themoviedb.org/3/"
    HEADERS = {"accept": "application/json"}
    PARAMS = {'api_key': '8c4b0b314700fae780304987c31ee568', 'language': 'en-US'}

    def get_data(self, query_tail: str, params=None):
        if params is None:
            params = self.PARAMS

        query = f'{self.URL}{query_tail}'

        response = requests.get(query, headers=self.HEADERS, params=params)

        if not response.status_code == 200:
            return response.status_code

        return response.json()

    def get_actor(self):
        query_tail = 'search/person'

        user_input = input('Please enter your search term: ')

        params = self.PARAMS.copy()
        params['include_adult'] = 'false'
        params['query'] = user_input

        return self.get_data(query_tail, params)

    def get_movies_by_year(self, sort_by: str = 'popularity.desc'):
        query_tail = 'discover/movie'

        year = input('Enter a year: ')

        params = self.PARAMS.copy()
        params['primary_release_year'] = year
        params['sort_by'] = sort_by
        params['include_adult'] = 'false'
        params['include_video'] = 'false'

        results = self.get_data(query_tail, params)
        print_multiple_result(results)

    def get_movie_by_id(self, movie_id):
        query_tail = f'movie/{movie_id}'
        return self.get_data(query_tail)

    def get_movies_by_title(self):
        query_tail = 'search/movie'

        user_input = input('Please enter your search term: ')
        year = input('Enter a year of the movie (leave blank if you don\'t know): ')

        params = self.PARAMS.copy()
        params['query'] = user_input
        if year != '':
            params['year'] = year

        result = self.get_data(query_tail, params)['results'][0]
        print_single_result(result)

    def get_popular_movies(self, page: str = '1', sort_by: str = 'popularity.desc'):
        query_tail = 'discover/movie'

        params = self.PARAMS.copy()
        params['include_adult'] = 'false'
        params['include_video'] = 'false'
        params['page'] = page
        params['sort_by'] = sort_by

        results = self.get_data(query_tail, params)
        print_multiple_result(results)

    # def get_actors_bio(self):
    #     actor_id = self.get_actor()['results'][0]['id']
    #     query_tail = f'person/{actor_id}'
    #
    #     return self.get_data(query_tail)

    def get_actors_movies(self):
        actor_id = self.get_actor()['results'][0]['id']
        query_tail = f'person/{actor_id}'

        params = self.PARAMS.copy()
        params['append_to_response'] = 'credits'

        results = self.get_data(query_tail, params)['credits']['cast']
        print_multiple_result(results)

    def get_all_genres(self):
        query_tail = 'genre/movie/list'
        return self.get_data(query_tail)

    def get_movies_by_genre(self, sort_by: str = 'popularity.desc'):
        query_tail = 'discover/movie'

        genres = input('Enter a list of genres divided by a comma: ')

        requested_genres_list = genres.split(',')
        all_genres = self.get_all_genres()['genres']
        genres_id_str = str()

        for genre_name in requested_genres_list:
            genre_name = genre_name.title().strip()

            for genre in all_genres:
                if genre['name'] == genre_name:
                    genres_id_str += str(genre['id'])
                    genres_id_str += ','

        params = self.PARAMS.copy()
        params['with_genres'] = genres_id_str
        params['sort_by'] = sort_by
        params['include_adult'] = 'false'
        params['include_video'] = 'false'

        results = self.get_data(query_tail, params)
        print_multiple_result(results)


if __name__ == '__main__':
    movies_source = MoviesSource()
