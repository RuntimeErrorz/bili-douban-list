import argparse
import requests
import time
import csv
import tqdm
from win11toast import toast
from wcwidth import wcswidth

MAX_LEN = 80
skip_cnt = 0
readd_cnt = 0
new_cnt = 0
def search_douban_rating(title, date):
    res = []
    while True:
        try:
            for movie in requests.get(f'https://api.wmdb.tv/api/v1/movie/search?q={title}').json():
                alias_list = [] if not movie.get('alias') else [
                    _.strip() for _ in movie['alias'].split('/')]
                dateReleased = None if not movie.get(
                    "dateReleased") else movie.get("dateReleased")[:4]
                if (movie['data'][0]["name"] == title or title in alias_list) \
                        and (date == '全1话' or movie.get("year") == date[:4] or dateReleased == date[:4]):
                    res.extend(
                        [movie["doubanRating"], f'https://movie.douban.com/subject/{movie["doubanId"]}/'])
            if res == []:
                tqdm.tqdm.write(
                    f"Searched {title}{' '* (MAX_LEN - wcswidth(title))} | Nothing Found!")
            else:
                tqdm.tqdm.write(
                    f"Searched {title}{' '* (MAX_LEN - wcswidth(title))} | Found {len(res) // 2} items matched")
            return res
        except Exception as e:
            toast(f"Error occurred: {e}. Retrying...", scenario='urgent')
        finally:
            time.sleep(30)


def write_douban_rating(title, date, film_row, rating_writer):
    film_row.extend(search_douban_rating(title, date))
    rating_writer.writerow(film_row)


def export_douban_rating(film_rows, new_rating_fd, reference_rating_dict={}, readded_film_dict={}):
    new_rating_writer = csv.writer(new_rating_fd)
    global skip_cnt, readd_cnt, new_cnt
    for film_row in tqdm.tqdm(film_rows, bar_format='{desc}: {percentage:3.2f}%| {bar}{r_bar}', ncols=75):
        title, link_id, date = film_row[1], film_row[2], film_row[3]
        if link_id in reference_rating_dict:
            skip_cnt += 1
            new_rating_writer.writerow(
                film_row[:4] + reference_rating_dict[link_id][4:])
        elif link_id in readded_film_dict:
            readd_cnt += 1
            new_rating_writer.writerow(film_row[:4] + readded_film_dict[link_id][3:])
        else:
            new_cnt += 1
            write_douban_rating(title, date, film_row, new_rating_writer)
        new_rating_fd.flush()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--create', action='store_true',
                        help='create new rating')
    parser.add_argument('--update', action='store_true',
                        help='update rating based on an existing rating file')
    args = parser.parse_args()
    if args.create:
        with open('rating.csv', 'a+', newline='', encoding='utf-8') as rating, \
                open('film.csv', 'r', newline='', encoding='utf-8') as film:
            rating.seek(0)
            start = len(list(csv.reader(rating)))
            export_douban_rating(film.readlines()[start:], rating)
    elif args.update:
        with open('new_rating.csv', 'a+', newline='', encoding='utf-8') as new_rating, \
                open('rating.csv', 'r', newline='', encoding='utf-8') as rating, \
                open('film.csv', 'r', newline='', encoding='utf-8') as film, \
                open('readded_film.csv', 'r', newline='', encoding='utf-8') as readded_film:
            new_rating.seek(0)
            film_rows = list(csv.reader(film))
            reference_rating_rows = list(csv.reader(rating))
            reference_rating_dict = {
                reference_rating_row[2]: reference_rating_row for reference_rating_row in reference_rating_rows}
            readded_film_dict = {readded_film_row[1]: readded_film_row for readded_film_row in list(csv.reader(readded_film))}
            export_douban_rating(film_rows[
                len(list(csv.reader(new_rating))):], new_rating, reference_rating_dict, readded_film_dict)
            print(f"Skipped {skip_cnt} items.")
            print(f"Readded {readd_cnt} items.")
            print(f"Newly Added {new_cnt} items.")
    else:
        exit("No action specified.")
