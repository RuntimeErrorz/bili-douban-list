import csv

# 首先，将所有数据读取到一个列表中
with open('new_file.csv', 'r', encoding='utf-8-sig') as file:
    reader = csv.reader(file)
    rows = list(reader)

# 计算总行数
total_rows = len(rows)

# 然后，关闭文件，再重新打开文件进行写入
with open('new_file.csv', 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    for index, row in enumerate(rows):
        # 在开头添加一个新的列，这个列的值是总行数减去当前行的索引
        new_row = [total_rows - index] + row
        writer.writerow(new_row)