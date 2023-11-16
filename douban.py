import requests, time, csv, tqdm
from win11toast import toast
def main():
    with open('final_list.csv', 'r', newline='', encoding='utf-8-sig') as csv_file:
        START = len(list(csv.reader(csv_file)))

    with open('final_list.txt', 'r', encoding='utf-8') as file_object, open('final_list.csv', 'a', newline='', encoding='utf-8-sig') as csv_file:
        writer = csv.writer(csv_file)
        print(START)
        for line in tqdm.tqdm(file_object.readlines()[START:], bar_format='{desc}: {percentage:3.2f}%|{bar}{r_bar}'):
            title = line.split()[1].strip()
            print(title)
            row = [title]
            for movie in requests.get(f'https://api.wmdb.tv/api/v1/movie/search?q={title}').json():
                if movie['data'][0]["name"] == title:
                    row.append(movie["doubanRating"])
                    row.append(f'https://movie.douban.com/subject/{movie["doubanId"]}/')
            writer.writerow(row)
            csv_file.flush()
            time.sleep(30)

while True:
    try:
        main()
        break 
    except Exception as e:
        toast(f"Error occurred: {e}. Retrying...", scenario='urgent')
        print(f"Error occurred: {e}. Retrying...") 
        time.sleep(60)