import instaloader
from datetime import datetime
from itertools import takewhile, dropwhile

bot = instaloader.Instaloader()
bot.login("paul_martino_test", "paulmartino9487")
posts = instaloader.Hashtag.from_name(bot.context, "instagram").get_posts()
SINCE = datetime(2021, 3, 10)
UNTIL = datetime(2021, 3, 12)
print("b")
for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, posts)):
    print("a")
    print(f"Post date : {post.date}, post like : {post.likes}, post owner : {post.owner_username}")
