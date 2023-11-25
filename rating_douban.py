import argparse, requests, time, csv, tqdm
from win11toast import toast

def write_rating_douban(source_lines, fd):
    writer = csv.writer(fd)
    for line in tqdm.tqdm(source_lines, bar_format='{desc}: {percentage:3.2f}%|{bar}{r_bar}', ncols=80):
        source_row = line.split(',')
        title = source_row[0].strip()
        if title[0] == '@': # 人工标记短片
            tqdm.tqdm.write(f"skip short: {title}")
            writer.writerow([_.strip() for _ in source_row])
            fd.flush()
            continue
        tqdm.tqdm.write(f"search: {title}")
        while True:
            try: 
                for movie in requests.get(f'https://api.wmdb.tv/api/v1/movie/search?q={title}').json():
                    if movie['data'][0]["name"] == title:
                        source_row.append(movie["doubanRating"])
                        source_row.append(f'https://movie.douban.com/subject/{movie["doubanId"]}/')
                break
            except Exception as e:
                toast(f"Error occurred: {e}. Retrying...", scenario='urgent')
            finally:
                time.sleep(30)
        writer.writerow([_.strip() for _ in source_row])
        fd.flush()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--create', action='store_true', help='create new rating')
    parser.add_argument('--update', action='store_true', help='unshift new rating')
    args = parser.parse_args()
    if args.create:    
        with open('rating.csv', 'a+', newline='', encoding='utf-8-sig') as rating, \
            open('source.csv', 'r', newline='', encoding='utf-8-sig') as source:
            rating.seek(0)
            start = len(list(csv.reader(rating)))
            write_rating_douban(source.readlines()[start:], rating)
    elif args.update:
        with open('rating.csv', 'r', newline='', encoding='utf-8-sig') as rating, \
             open('temp.csv', 'a+', newline='', encoding='utf-8-sig') as temp, \
             open('source.csv', 'r', newline='', encoding='utf-8-sig') as source:
            temp.seek(0, 0)
            temp_len = len(list(csv.reader(temp)))
            source_len, original_len = len(list(csv.reader(source))), len(list(csv.reader(rating)))
            print(f"to be updated: {source_len - original_len + temp_len}")
            source.seek(0, 0)
            write_rating_douban(source.readlines()[temp_len:source_len - original_len], temp)
    print("Manually unshift temp.csv to rating.csv")