import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--list', action='store_true',
                    help='clean film list')
parser.add_argument('--rating', action='store_true',
                    help='clean rating')

args = parser.parse_args()

if args.list:
    film_file, short_file, new_film_file, new_short_file  = 'film.csv', 'short.csv', 'new_film.csv', 'new_short.csv'
    removed_film_file, new_removed_film_file = 'removed_film.csv', 'new_removed_film.csv'
    if os.path.exists(film_file):
        os.remove(film_file)
    if os.path.exists(short_file):
        os.remove(short_file)
    if os.path.exists(removed_film_file):
        os.remove(removed_film_file)
    os.rename(new_film_file, film_file)
    os.rename(new_short_file, short_file)
    os.rename(new_removed_film_file, removed_film_file)

elif args.rating:
    rating_file, new_rating_file = 'rating.csv', 'new_rating.csv'
    if os.path.exists(rating_file):
        os.remove(rating_file)
    os.rename(new_rating_file, rating_file)
    os.remove('readded_film.csv')

else:
    exit("No action specified.")