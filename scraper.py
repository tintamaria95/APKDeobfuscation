from requests_tor import RequestsTor
# from selenium import webdriver
# from selenium.webdriver.common import by
from pathlib import Path

# If you use the Tor browser
rt = RequestsTor()

# use github search query( stars>500 and Language:Java android )
url_query_root = (
    'https://github.com/search?q=stars%3A%3E500+language%3AJava+android')

test_link = 'https://github.com/hmkcode/Android/archive/refs/heads/master.zip'

r = rt.get(test_link)
path_file = Path('./scraped_data', 'Android.zip')
open(path_file, 'wb').write(r.content)

# driver = webdriver()
