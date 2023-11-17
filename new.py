import csv

# 打开你的CSV文件并读取所有的行
with open('final_list.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    rows = list(reader)

# 在每一行的开头添加反行数
for i, row in enumerate(rows):
    row.insert(0, len(rows) - i)

# 将结果写入一个新的CSV文件
with open('new_file.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerows(rows)