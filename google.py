from magic_google import MagicGoogle
import pprint

# Or PROXIES = None
PROXIES = [{
    'http': 'http://127.0.0.1:1080',
    'https': 'http://127.0.0.1:1080'
}]

# Or MagicGoogle()
mg = MagicGoogle(PROXIES)

#  Crawling the whole page


# Crawling url
for i in range(4):
    for url in mg.search_url(query='"com.cpic" site::https://github.com', start=10*i):
        pprint.pprint(url)
        
print("google的数据为三页，但是比较准确")
