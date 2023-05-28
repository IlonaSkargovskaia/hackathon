from main import Movie, MoviesSource
import os


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def print_menu(menu: dict):
    # clear()
    print(" " * 4 + "MENU")
    {print(f"({key}) {value}") for key, value in menu.items()}


def menu_actions(options, actions):
    try:
        users_choice = input(" : ").lower()
    except ValueError:
        print("Only letters are allowed")
    else:
        if users_choice in options.keys():
            action = actions[users_choice]

            action()
        else:
            print("Wrong input...")


def show_user_menu():
    options = {
        "search": "Search for a movie",
        "view": "View favorite movies",
        "add": "Add a movie to your favorites",
        "remove": "Delete a movie from your favorites",
        "x": "Exit",
    }

    actions = {
        "search": show_search_menu,
        "view": view_favorite_movies,
        "add": add_movie_to_favorites,
        "remove": remove_movie_from_favorites,
        "x": quit,
    }

    print_menu(options)
    menu_actions(options, actions)


def remove_movie_from_favorites():
    try:
        user_input = int(input("Enter the movie's id: "))
    except ValueError:
        print("Only numbers are allowed")
    else:
        Movie.delete(
            user_input
        )


def add_movie_to_favorites():
    movie_source = MoviesSource()

    try:
        user_input = int(input("Enter the movie's id: "))
    except ValueError:
        print("Only numbers are allowed")
    else:
        movie_by_id = movie_source.get_movie_by_id(user_input)

        genres_list = list()
        for genre_dict in movie_by_id['genres']:
            genres_list.append(genre_dict['name'].lower())

        genres = ", ".join(genres_list)

        overview = [character for character in movie_by_id['overview'] if character not in ["'", '"']]

        overview = "".join(overview)

        Movie.save(
            movie_by_id["id"],
            movie_by_id["title"],
            genres,
            overview,
            movie_by_id["popularity"],
            movie_by_id["poster_path"],
            movie_by_id["release_date"]
        )


def view_favorite_movies():
    movie_list = Movie()
    movie_list.print_all()


def show_search_menu():
    movie_source = MoviesSource()

    options = {
        "title": "Find movies by title",
        "year": "Find movies by year",
        "genre": "Find movies by genre",
        "actor": "Find movies by actor's name",
        "popular": "Find movies by popularity",
    }

    actions = {
        "title": movie_source.get_movies_by_title,
        "year": movie_source.get_movies_by_year,
        "genre": movie_source.get_movies_by_genre,
        "actor": movie_source.get_actors_movies,
        "popular": movie_source.get_popular_movies,
    }

    print_menu(options)
    menu_actions(options, actions)


if __name__ == "__main__":
    while True:
        show_user_menu()
