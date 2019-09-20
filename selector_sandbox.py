""" This is a temporary file to test out selectors on an offline copy of the page HTML
without involving the rest of scrapy."""

from scrapy.selector import Selector

with open("FULL_SOURCE.html", 'r') as f:
    body = f.read()  # f.readlines()

selector_str = "//div/ul/li"
# selector_str = "//div"

# print(body)

# if 'div' in body:
#     print('Hmm')
# else:
#     print('Wtf')

#
# for item in body:
#     print(item)

# print(type(body))
# print(Selector(text=body).xpath(selector_str).get())


# body = '<html><body><span>good</span></body></html>'
# selector_str = '//span/text()'

for item in Selector(text=body).xpath(selector_str):
    print(item.extract())