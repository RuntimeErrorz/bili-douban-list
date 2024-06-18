import argparse
import requests
import time
import csv
import tqdm
from win11toast import toast
from wcwidth import wcswidth

MAX_LEN = 80
skip_cnt = 0


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


def write_douban_rating(title, date, source_row, rating_writer):
    source_row.extend(search_douban_rating(title, date))
    rating_writer.writerow(source_row)


def export_douban_rating(source_rows, rating_fd, reference_rating=None):
    writer = csv.writer(rating_fd)
    for source_row in tqdm.tqdm(source_rows, bar_format='{desc}: {percentage:3.2f}%| {bar}{r_bar}', ncols=75):
        title, date = source_row[1], source_row[3]
        if reference_rating is None:
            write_douban_rating(title, date, source_row, writer)
        else:
            need_search = True
            for reference_row in reference_rating:
                # if source_row[2] == reference_row[2] and reference_row[4] != '':
                if source_row[2] == reference_row[2]:
                    skip_cnt += 1
                    writer.writerow(source_row[:4] + reference_row[4:])
                    need_search = False
            if need_search:
                write_douban_rating(title, date, source_row, writer)
        rating_fd.flush()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--create', action='store_true',
                        help='create new rating')
    parser.add_argument('--update', action='store_true',
                        help='update rating based on an existing rating file')
    args = parser.parse_args()
    if args.create:
        with open('rating.csv', 'a+', newline='', encoding='utf-8') as rating, \
                open('source.csv', 'r', newline='', encoding='utf-8') as source:
            rating.seek(0)
            start = len(list(csv.reader(rating)))
            export_douban_rating(source.readlines()[start:], rating)
    elif args.update:
        with open('new_rating.csv', 'a+', newline='', encoding='utf-8') as new_rating, \
                open('rating.csv', 'r', newline='', encoding='utf-8') as rating, \
                open('source.csv', 'r', newline='', encoding='utf-8') as source:
            new_rating.seek(0)
            source_rows = list(csv.reader(source))
            start = len(list(csv.reader(new_rating)))
            reference_rating = list(csv.reader(rating))
            export_douban_rating(source_rows[
                start:], new_rating, reference_rating)
            print(f"Skipped {skip_cnt} items.")
    else:
        exit("No action specified.")
