import csv
import requests
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'
}


def is_short(url):
    return '<span>短片' in requests.get(url, headers=HEADER).text


def movie_type(link, source_list, short_list):
    for row in source_list:
        if link == row[2]:
            return "source"
    for row in short_list:
        if link == row[2]:
            return "short"
    return "unseen"


with open('source.csv', 'r', newline='', encoding='utf-8') as source, \
        open('short.csv', 'r',  newline='', encoding='utf-8') as short, \
        open('new_source.csv', 'w', newline='', encoding='utf-8') as new_source, \
        open('new_short.csv', 'w', newline='', encoding='utf-8') as new_short:
    source_list,  short_list = list(
        csv.reader(source)), list(csv.reader(short))
    new_source_data, new_short_data = [], []
    source_writer, short_writer = csv.writer(new_source), csv.writer(new_short)
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
                if movie_type(movie['link'], source_list, short_list) == 'unseen':
                    # if movie['order'] != '' and movie['order'][:-2] in movie['index_show']: 另一种判断是否为短片的方法，不过不一定可靠
                    if is_short(movie['link']):
                        print(f"Adding {movie['title']} to new short.")
                        row.append(movie['order'])
                        new_short_data.append(row)
                    else:
                        print(f"Adding {movie['title']} to new source.")
                        new_source_data.append(row)
                elif movie_type(movie['link'], source_list, short_list) == 'source':
                    new_source_data.append(row)
                else:
                    new_short_data.append(row)
                index += 1
            page += 1
        except Exception as e:
            print(f"Error occurred: {e}.")
            break
    source_writer.writerows(new_source_data)
    short_writer.writerows(new_short_data)
