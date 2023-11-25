import requests, csv

with open('source.csv', 'r', newline='', encoding='utf-8-sig') as f:
    data = list(csv.reader(f))
    original_len = len(data)

with open('source.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    hasnext = True
    page, num = 1, 0
    while hasnext:
        url = f'https://api.bilibili.com/pgc/season/index/result?order=0&area=-1&style_id=-1&release_date=-1&season_status=-1&sort=0&page={page}&season_type=2&pagesize=200&type=1'
        print(url)
        try:
            resp = requests.get(url).json()
            total, hasnext, movies = resp['data']['total'], resp['data']['has_next'], resp['data']['list']
            print(f"to be updated: {total - original_len}")
            if num >= total - original_len:
                break
            for movie in movies:
                if num >= total - original_len:
                    break
                date, link, title = movie['index_show'], movie['link'], movie['title']
                data.insert(num, [title, link, date])
                num += 1 
            page += 1
        except Exception as e:
            print(f"Error occurred: {e}.")
            break
    writer.writerows(data)

print("Need to manually handle the overlapping of source.csv due to the upcoming movies problems of bili api ")
