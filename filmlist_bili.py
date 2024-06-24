import csv
import requests
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'
}


def is_short(url):
    return '<span>短片' in requests.get(url, headers=HEADER).text


def movie_type(link, film_dict, short_dict):
    if link in film_dict:
        del film_dict[link]
        return "film"
    elif link in short_dict:
        del short_dict[link]
        return "short"
    return "unseen"


with open('film.csv', 'r', newline='', encoding='utf-8') as film, \
        open('short.csv', 'r',  newline='', encoding='utf-8') as short, \
        open('new_film.csv', 'w', newline='', encoding='utf-8') as new_film, \
        open('new_short.csv', 'w', newline='', encoding='utf-8') as new_short, \
        open('removed_film.csv', 'r', newline='', encoding='utf-8') as removed_film, \
        open('new_removed_film.csv', 'w', newline='', encoding='utf-8') as new_removed_films, \
        open('readded_film.csv', 'w', newline='', encoding='utf-8') as readded_films, \
        open('rating.csv', 'r', newline='', encoding='utf-8') as rating:
    readded_film_list = []
    new_removed_film_writer = csv.writer(new_removed_films)
    removed_film_dict = {row[1]: row for row in list(csv.reader(removed_film))}
    film_list, short_list = list(
        csv.reader(film)), list(csv.reader(short))
    film_dict, short_dict = {row[2]: row for row in film_list}, {
        row[2]: row for row in short_list}
    new_film_data, new_short_data = [], []
    new_film_writer, new_short_writer = csv.writer(
        new_film), csv.writer(new_short)
    hasnext = True
    index = 1
    page = 1
    while hasnext:
        url = f'https://api.bilibili.com/pgc/season/index/result?order=0&area=-1&style_id=-1&release_date=-1&season_status=-1&sort=1&page={page}&season_type=2&pagesize=200&type=1'
        print(url)
        try:
            resp = requests.get(url, headers=HEADER).json()
            total, hasnext, movies = resp['data']['total'], resp['data']['has_next'], resp['data']['list']
            for movie in movies:
                row = [index] + [_.strip() for _ in [movie['title'], movie['link'],
                                 movie['index_show']]]
                if movie['link'] in removed_film_dict:  # 旧电影上架了
                    print(f"{movie['title']} is back!")
                    readded_film_list.append(removed_film_dict[movie['link']])
                    del removed_film_dict[movie['link']]
                type = movie_type(movie['link'], film_dict, short_dict)
                if type == 'unseen':
                    # if movie['order'] != '' and movie['order'][:-2] in movie['index_show']: 另一种判断是否为短片的方法，不过不一定可靠
                    if is_short(movie['link']):
                        print(f"Adding {movie['title']} to new short list.")
                        row.append(movie['order'])
                        new_short_data.append(row)
                    else:
                        print(f"Adding {movie['title']} to new film list.")
                        new_film_data.append(row)
                elif type == 'film':
                    new_film_data.append(row)
                else:
                    new_short_data.append(row)
                index += 1
            page += 1
        except Exception as e:
            print(f"Error occurred: {e}.")
            break
    new_film_writer.writerows(new_film_data)
    new_short_writer.writerows(new_short_data)
    for key in film_dict:
        print(f"{film_dict[key][1]} is removed!")
    rating_dict = {row[2]: row for row in list(csv.reader(rating))}
    film_dict = {key: rating_dict[key][1:] for key in film_dict}
    film_dict.update(removed_film_dict)
    new_removed_film_writer.writerows(
        [film_dict[key] for key in film_dict])
    readded_film_writer = csv.writer(readded_films)
    readded_film_writer.writerows(readded_film_list)
