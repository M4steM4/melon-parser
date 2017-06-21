# -*- coding: utf-8 -*-

import requests
import json
import re
from bs4 import BeautifulSoup

def top100():
    top100_url = "http://www.melon.com/chart/index.htm"

    html = requests.get(top100_url).text
    soup = BeautifulSoup(html, 'html.parser')

    for tag in soup.select('#tb_list a[href*=playSong]'):
        title = tag.text
        js = tag['href']
        matched = re.search(r"'(\d+)'\);", js)
        if matched:
            song_id = matched.group(1)
            song_url  = "http://www.melon.com/song/detail.htm?songId=" + song_id
            print(title + '\n' + song_url)


def melon_search(q):
    url = "http://www.melon.com/search/keyword/index.json"

    params = {
        'jscallback' : 'jQuery191021691499565277317_1498011450140',
        'query' : q,
    }

    response = requests.get(url, params=params).text
    json_string = response.replace(params['jscallback'] + '(', '').replace(');', '')
    result_dic = json.loads(json_string)

    if 'SONGCONTENTS' not in result_dic:
        print('Can not found' + q)
    else:
        for song in result_dic['SONGCONTENTS']:
            print(song['SONGNAME'] + '(' + song['ALBUMNAME'] + ') - ' + song['ARTISTNAME'] + '\n' + 'Link : http://www.melon.com/song/detail.htm?songId=' + song['SONGID'])

if __name__ == '__main__':
    line = raw_input()
    if line == 'top100':
        top100()
    else:
        melon_search(line)
