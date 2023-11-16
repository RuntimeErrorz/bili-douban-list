# 创建一个集合来存储已经出现过的电影名字
movie_set = set()

# 打开源文件并读取电影名字
with open('res.txt', 'r', encoding='utf-8') as f:
    # 打开目标文件准备写入
    with open('new_filename.txt', 'w', encoding='utf-8') as nf:
        for line in f:
            _, movie = line.strip().split(' ', 1)
            # 如果电影名字还未出现过，则写入到新的文件
            if movie not in movie_set:
                nf.write(line)
                movie_set.add(movie)