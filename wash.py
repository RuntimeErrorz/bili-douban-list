import re
def extract_movie_title(movie_string):
    movie = re.search('】(.*?)（', movie_string)
    if movie is None:
        movie = re.search('】(.*?)[ ，,]', movie_string)
    if movie is None:
        movie = re.search('(.*?)（', movie_string)
    if movie is not None:
        return movie.group(1)
    else:
        return "---!!未!!--- " + movie_string

with open('titles.txt', 'r', encoding='utf-8') as titles, open('res.txt', 'w', encoding='utf-8') as titles_res:
    index = 1
    for title in titles.readlines():
        titles_res.write(str(index) + " ")
        if (index <= 2052):
            start_index = title.find("【")
            end_index = title.find("】")
            if (start_index == -1 or end_index == -1):
                titles_res.write("---!!未!!--- " + title + '\n')
            else:
                titles_res.write(title[start_index + 1:end_index].strip() + '\n')
        else:
            titles_res.write(extract_movie_title(title) + '\n')
        index += 1