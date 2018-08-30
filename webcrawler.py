import requests
import os.path
import codecs
from urllib.parse import urljoin

headers = {
    'User-Agent': 'Ford',
    'From': 'fordfifi@hotmail.com',
    'content-type': 'text/html; charset=utf-8'
}

def get_page(url):
    global headers
    text = ''
    try:
        r = requests.get(url, headers=headers, timeout=2)
        text = r.text
    except(KeyboardInterrupt, SystemExit):
        raise
    except:
        print('GET PAGE ERROR!')
    return text.lower()

def get_normal_page(url):
    global headers
    text = ''
    try:
        r = requests.get(url, headers=headers, timeout=2)
        text = r.text
    except(KeyboardInterrupt, SystemExit):
        raise
    except:
        print('GET PAGE ERROR!')
    return text    

def link_parser(base_url, raw_html):
    urls = []
    pattern_start = '<a href="'
    pattern_end = '"'
    index = 0
    length = len(raw_html)
    while index < length:
        start = raw_html.find(pattern_start, index)
        if start > 0:
            start = start + len(pattern_start)
            end = raw_html.find(pattern_end, start)
            link = raw_html[start:end]
            if len(link) > 0:
                if link not in urls:
                    # print(link)
                    abs_link = urljoin(base_url, link)
                    urls.append(abs_link)
            index = end
        else:
            break
    return urls

domain = []
frontier_q = ['http://www.ku.ac.th/web2012/']
visited_q = []

while len(frontier_q) > 0:
    current_url = frontier_q[0]
    frontier_q = frontier_q[1:]
    visited_q.append(current_url)

    text = get_page(current_url)
    extracted_links = link_parser(current_url ,text)

    for link in extracted_links:
        if link not in frontier_q and link not in visited_q:
            frontier_q.append(link)
            if 'ku.ac.th' in link:
                if link[-3:] == 'htm' or link[-4:] == 'html':
                    print(link)
                    page = get_normal_page(link)
                
                    link = link.replace('http://', '')
                    link = link.replace('https://', '')
                    link = link.replace('www.', '')
                    link = link.split('/')
                    link = list(filter(None, link))
                    
                    domain.append(link[0])
                    print(link)
                    
                    path = os.path.abspath('html')
                    if not os.path.exists(path):
                        os.makedirs(path)
                    for i in range(len(link)):
                        path += '/' + link[i]
                        if not os.path.exists(path) and i < len(link) -1:
                            os.makedirs(path)
                    
                    path = os.path.abspath(path)
                    print(path)
                    file = codecs.open(path, 'w', "utf-8-sig")
                    file.write(page)
                    file.close()

