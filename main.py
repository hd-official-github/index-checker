from bs4 import BeautifulSoup
import requests
import urllib.parse
from html_sanitizer import Sanitizer
# r = requests.get(url = 'https://async.scraperapi.com/jobs/', json={ 'apiKey': 'c817eec695cab0444aeecb968f833df5', 'url': 'https://example.com' })


def url_parse(url):
    rll =  urllib.parse.unquote(url)
    url = urllib.parse.quote(rll)
    return url
   
irl = url_parse("https://ff.ccc")
r = requests.get(url = 'https://api.scraperapi.com?api_key=c817eec695cab0444aeecb968f833df5&url=https://www.google.com/search?q=site:'+irl+"&device_type=desktop")
# sanitizer = Sanitizer()  
# c=sanitizer.sanitize(r.text)
soup = BeautifulSoup(r.text,"html.parser")
tag = soup.body

for m in tag.strings:
    st=False
    for string in tag.strings:
        print(string)
        if "Make sure that all words are spelled correctly" in string:
            st=False
            break; 
        else:
            st=True

    # return st
