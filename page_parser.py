from selenium import webdriver
from bs4 import BeautifulSoup
from kaomoji.models import Category, SubCategory, Emoticon
import sys
import django

urls = [
    "http://japaneseemoticons.net/all-japanese-emoticons/",
    "http://japaneseemoticons.net/all-japanese-emoticons/2/",
    "http://japaneseemoticons.net/all-japanese-emoticons/3/",
    "http://japaneseemoticons.net/all-japanese-emoticons/4/",
    "http://japaneseemoticons.net/all-japanese-emoticons/5/",
    "http://japaneseemoticons.net/all-japanese-emoticons/6/",
    "http://japaneseemoticons.net/all-japanese-emoticons/7/",
    "http://japaneseemoticons.net/all-japanese-emoticons/8/",
    "http://japaneseemoticons.net/all-japanese-emoticons/9/",
    "http://japaneseemoticons.net/all-japanese-emoticons/10/"
]

encoding = sys.stdin.encoding

def determine_format(first_cell, second_cell):
    response = raw_input("First row of this table is " + first_cell.encode(encoding) + "; " + second_cell.encode(encoding) + ". Is this a name-emoticon format? [y/n] ")
    return response.lower()[0] == 'y'

django.setup()

print "Clearing tables:"
Emoticon.objects.all().delete()
print "Finished clearing emoticons"
SubCategory.objects.all().delete()
print "Finished clearing subcategories"
Category.objects.all().delete()
print "Finished clearing categories"

profile = webdriver.FirefoxProfile();
profile.set_preference("javascript.enabled", False);
driver = webdriver.Firefox(firefox_profile=profile);
driver.set_window_size(1120, 550)

emoticon_count = 0

for url in urls:
    driver.get(url)
    html = driver.page_source

    soup = BeautifulSoup(html)
    category = None
    subcategory = None
    for element in soup.find_all(['h2', 'table', 'h3']):
        if (element.name == 'h2' and not unicode(element.contents[0]).startswith("<")):
            category_name = unicode(element.contents[0])
            category = Category(name=category_name)
            category.save()
            subcategory = None
            print "Category: " + category_name
        elif (element.name == 'h3' and not unicode(element.contents[0]).startswith("<")):
            subcategory_name = unicode(element.contents[0])
            subcategory = SubCategory(name=subcategory_name, category=category)
            subcategory.save()
            print "Subcategory: " + subcategory_name
        elif (element.name == 'table'):
            name_icon_format_set = False
            name_icon_format = False
            for tr in element.find("tbody").find_all("tr"):
                td_list = tr.find_all("td")
                if len(td_list) == 2 and (not name_icon_format_set or name_icon_format):
                    first_cell = unicode(td_list[0].contents[0])
                    second_cell = unicode(td_list[1].contents[0])
                    if (not name_icon_format_set):
                        name_icon_format = determine_format(first_cell, second_cell)
                        name_icon_format_set = True
                    if name_icon_format:
                        emoticon_name = first_cell
                        emoticon_content = second_cell
                        emoticon = Emoticon(category=category, subcategory=subcategory, name=emoticon_name, content = emoticon_content, index=emoticon_count)
                        emoticon_count += 1
                        emoticon.save()
                    else:
                        Emoticon(category=category, subcategory = subcategory, content=first_cell, index=emoticon_count).save()
                        Emoticon(category=category, subcategory = subcategory, content=second_cell, index=emoticon_count).save()
                        emoticon_count+=2
                else:
                    for td in td_list:
                        if (td.contents):
                            emoticon_content = unicode(td.contents[0])
                            emoticon = Emoticon(category=category, subcategory=subcategory, content = emoticon_content, index=emoticon_count)
                            emoticon_count+=1
                            emoticon.save()

driver.quit()
