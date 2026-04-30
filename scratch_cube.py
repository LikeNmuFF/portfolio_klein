import urllib.request
import re

url = 'https://likenmuff.github.io/portfolio/'
try:
    css_url = 'https://likenmuff.github.io/portfolio/styles.css'
    css = urllib.request.urlopen(urllib.request.Request(css_url, headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8')
    print("CSS length:", len(css))
    
    with open('c:\\Users\\Hp\\Documents\\porfolio\\scratch_styles.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("Saved to scratch_styles.css")
except Exception as e:
    print(e)
