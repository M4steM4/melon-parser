# -*- coding: utf-8 -*-

import requests
import json
import re
from bs4 import BeautifulSoup

import os
import smtplib
import getpass
from email.message import EmailMessage
from email.mime.application import MIMEApplication

def email():
    from_id = input('Input your email ID : ')
    to_id = input('Input opponent email ID : ')
    password = getpass.getpass('Password : ')
    test = input()

    message = EmailMessage()
    message['Subject'] = 'Test'
    message['From'] = from_id + '@naver.com'
    message['To'] = to_id + '@naver.com'

    message.set_content('''
        Python message test''')

    message.add_alternative(test, subtype='html')


    filepath_list = ['1.jpg', '2.jpg']
    for filepath in filepath_list:
        with open(filepath, 'rb') as f:
            filename = os.path.basename(filepath)
            cid = filename
            img_data = f.read()
            part = MIMEApplication(img_data, name=filename)
            if cid == 'f1.jpg':
                part.add_header('Content-ID', '<' + cid + '>')
            else:
                part.add_header("Content-Disposition", "attachment; filename=\"%s\"" % filename)
            message.attach(part)

    with smtplib.SMTP_SSL('smtp.naver.com', 465) as server:
        server.ehlo()
        server.login(from_id, password)
        server.send_message(message)

    print('이메일을 성공적으로 발송했습니다.')

    
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
