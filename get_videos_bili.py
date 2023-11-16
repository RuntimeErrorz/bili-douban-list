from bilibili_api import user, sync
from bilibili_api import settings
import time
# settings.proxy = "http://39.104.57.170:10001"
u = user.User(15773384)

async def main():
    pn = 122
    ps = 30
    _ = await u.get_videos()
    total = _["page"]["count"] - (pn - 1) * ps
    print(total)
    br = True
    with open('title_source.txt', 'a', encoding='utf-8') as file_object:
      while br:
          if (total < 30):
              ps = total
              br = False
          print(pn, ps)
          page = await u.get_videos(pn=pn, ps=ps)
          for video in page["list"]["vlist"]:
              title = video["title"] 
              file_object.write('\n' + title)
          pn += 1
          total -= ps
          time.sleep(5)
# 入口
sync(main())