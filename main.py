from pseudo_spider import PsuedoSpider

with open("source.html", 'r') as f:
    body = f.read()


spider = PsuedoSpider()
meetings = spider.parse(body)

for meeting in meetings:
    print(meeting)