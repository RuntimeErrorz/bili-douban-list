import csv, requests, time, tqdm
from win11toast import toast

# 打开源文件和目标文件
with open('new_file.csv', 'r', newline='', encoding='utf-8-sig') as target:
    len = len(list(csv.reader(target)))
with open('rating.csv', 'r', newline='', encoding='utf-8-sig') as source, \
     open('new_file.csv', 'a', newline='', encoding='utf-8-sig') as target:
    # 创建一个 CSV reader 和 writer
    lines = source.readlines()[len:]
    writer = csv.writer(target)
    for line in tqdm.tqdm(lines, bar_format='{desc}: {percentage:3.2f}%|{bar}{r_bar}', ncols=80): # title, link, date, rating, douban_link
        row = line.split(',')
        if row[2] != '全1话' and row[4] != '' and row[6] != '':
            row = row[:3]
            year = row[2][:4]
            while True:
                try: 
                    tqdm.tqdm.write(f"research: {row[0]}")
                    for movie in requests.get(f'https://api.wmdb.tv/api/v1/movie/search?q={row[0]}').json():
                        dateReleased = None if movie.get("dateReleased") is None else movie.get("dateReleased")[:4] 
                        if movie['data'][0]["name"] == row[0] and (movie.get("year") == year or dateReleased == year):
                            row.append(movie["doubanRating"])
                            row.append(f'https://movie.douban.com/subject/{movie["doubanId"]}/')
                    break
                except Exception as e:
                    toast(f"Error occurred: {e}. Retrying...", scenario='urgent')
                finally:
                    time.sleep(30)
        else:
            tqdm.tqdm.write(f"skip: {row[0]}")
        writer.writerow([_.strip() for _ in row])
        target.flush()