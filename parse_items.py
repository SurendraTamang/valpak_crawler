import requests
import re
from lxml import html
url = 'https://www.valpak.com/local/dallas-tx/hellofresh-usa-190626?store=91968'

response = requests.get(url)


# parsing from local html file sample.html
text_file = open("sample.html", "r").read()
tree = html.fromstring(open('sample.html').read())
#business_name = tree.xpath('//title/text()')
business_name = tree.xpath("//span[contains(@class,'capitalize')]/text()")[0].strip()
address = re.compile('singleLineAddress:"(.*?)",address').findall(text_file)[0]




breakpoint()
