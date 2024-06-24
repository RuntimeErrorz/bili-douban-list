## 项目简介

本项目用于半自动爬取B站电影抓取豆瓣评分。

### 1. 更新除短片外的电影列表

`python filmlist_bili.py`

由于B站偶会下架电影，以及防止其他突发原因导致的错误，每次运行上述代码会参考当前`film.csv`和`short.csv`全量更新，生成新文件`new_film.csv`和`new_short.csv`。确认无误后，可执行`python clean.py --list`保留最新结果。

特别的，针对下架的情况，做出更新。

| film | removed
| --- | --- 
|  ABC| None|
| ADF | BC |
| ABDEG |CF|

### 2. 更新豆瓣评分

`python rating_douban.py --update`

类似的，确认无误后，同样可执行`python clean.py --rating`保留最新结果。
