""" This is a temporary file to test out selectors on an offline copy of the page HTML
without involving the rest of scrapy."""

from scrapy.selector import Selector

with open("source.html", 'r') as f:
    body = f.read()  # f.readlines()

# selector_str = "//div/div/div/ul/li"  # Way too many results.

# This correctly selects only the two headers that I care about, but not the ULs adjacent (which contain meeting data)
# selector_str = "//div/div/div/h3"

# ------------------------------------------- FUTURE MEETINGS ---------------------------------------------------------
# This selects the first UL I care about, but also 2 others I don't, and misses one that I do want.
# selector_str = "//div/div/div/h3/following-sibling::ul"
#
# # Either an extract_first() or narrowing down further might work.
# first_result = Selector(text=body).xpath(selector_str).extract_first()
#
# for item in Selector(text=first_result).xpath('//li'):
#     print(item.extract())
    # This can then be passed over to it's own special parser. I can drop those which are in the past - those will be
    # present in the next section (with the "Commission Meetings" header, that details past meetings).

# --------------------------------------------- PAST MEETINGS ---------------------------------------------------------

# This selector works great until the very last row of the table, at which point some lazy web-dev started just using
# <br> for new meeting entries, rather than <tr> rows. That's going to complicate parsing.

# I think I'll check the contents for <br> and then send them off to a tertiary parser if they contain such.
selector_str = "//div/div/div/h3/following-sibling::table/tbody/tr"

print(f"Number of items matching selector: {len(Selector(text=body).xpath(selector_str))}")

for item in Selector(text=body).xpath(selector_str):
    print(item.extract())

