from selenium import webdriver
from bs4 import BeautifulSoup

profile = webdriver.FirefoxProfile();
profile.set_preference("javascript.enabled", False);
driver = webdriver.Firefox(firefox_profile=profile);
#driver = webdriver.PhantomJS(profile)
driver.set_window_size(1120, 550)
driver.get("http://japaneseemoticons.net/all-japanese-emoticons/")
html = driver.page_source
driver.quit()

soup = BeautifulSoup(html)
for element in soup.find_all(['h2', 'table']):
    if (element.name == 'h2'):
        print element.contents[0]
    if (element.name == 'table'):
        for tr in element.find("tbody").find_all("tr"):
            for td in tr.find_all("td"):
                if (td.contents):
                    print td.contents[0]
