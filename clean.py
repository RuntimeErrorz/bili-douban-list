import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--list', action='store_true',
                    help='clean film list')
parser.add_argument('--rating', action='store_true',
                    help='clean rating')

args = parser.parse_args()

if args.list:
    source_file, short_file, new_source_file, new_short_file  = 'source.csv', 'short.csv', 'new_source.csv', 'new_short.csv', 
    if os.path.exists(source_file):
        os.remove(source_file)
    if os.path.exists(short_file):
        os.remove(short_file)
    os.rename(new_source_file, source_file)
    os.rename(new_short_file, short_file)

elif args.rating:
    rating_file, new_rating_file = 'rating.csv', 'new_rating.csv'
    if os.path.exists(rating_file):
        os.remove(rating_file)
    os.rename(new_rating_file, rating_file)

else:
    exit("No action specified.")