from pseudo_spider import PsuedoSpider

with open("source.html", 'r', encoding='utf-8') as f:
    # body = f.read().replace(u'\u200b', '')
    body = f.read()

# print(body)

# if u'\u200b' in body:
#     print(True)
# else:
#     print(False)

spider = PsuedoSpider()
meeting_gen = spider.parse(body)
meeting_list = [meeting for meeting in meeting_gen]
print(f"Length of meeting_list: {len(meeting_list)}")

for meeting in meeting_list:
    pass
    print(meeting)
    print('\n')
