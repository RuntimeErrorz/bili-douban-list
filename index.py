import argparse, csv

parser = argparse.ArgumentParser()
parser.add_argument('--create', action='store_true', help='create new index number')
parser.add_argument('--clear', action='store_true', help='clear existed index number')
args = parser.parse_args()
# 首先，将所有数据读取到一个列表中
with open('rating.csv', 'r', encoding='utf-8-sig') as file:
    reader = csv.reader(file)
    rows = list(reader)

# 计算总行数
total_rows = len(rows)

# 然后，关闭文件，再重新打开文件进行写入
with open('rating.csv', 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    for index, row in enumerate(rows):
        if args.create:
            new_row = [total_rows - index] + row
        elif args.clear:
            new_row = row[1:] 
        writer.writerow(new_row)