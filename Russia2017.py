# -*- coding: utf-8 -*-
import requests
#from bs4 import BeautifulSoup  as bs
import re
from scrapy.selector import Selector as Sel
from scrapy.http import HtmlResponse as HR 
import csv
import ast

agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'
headers = {
        'User-Agent': agent
  }

url = 'http://www.europaplus.ru/index.php?go=Chart40'

def saveHTML(url,name, headers = headers):
  try:
    req = requests.get(url, headers = headers)
    print req.encoding
    with open(name, 'w') as f:
      text = req.text.splitlines()
      for line in text:
        try:
          f.write(line.encode('windows-1251'))
        except:
          f.write(line)
    print "File is saved"
  except:
    print "Bad request or not saved file. Sorry ;("


def writeCSV(List, filename = 'test.csv'):
  with open('russia2017.csv', 'a') as csvfile:
      writer = csv.writer(csvfile, delimiter=',')
      for row in List:
        try:
          writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5]])
        except UnicodeEncodeError:
          writer.writerow([row[0].encode('utf-8'), row[1].encode('utf-8'), row[2].encode('utf-8'), row[3].encode('utf-8')])
        finally:
          #print "data view as: ", row[0], ' and ', row[1]  
          pass

def getAudio(author, sing):
  reqStr = author + ' ' + sing 
  reqStr = reqStr.replace('& ','')
  #print reqStr  
  reqStr = reqStr.replace(' ','+')
  #print reqStr
  googurl = 'https://www.google.ru/search?newwindow=1&ei=O41KWrz4J-nX6QTFgbWYDQ&q=%s'%reqStr

  req = requests.get(googurl, headers = headers)
  response = HR(url=googurl, body = req.text, encoding='utf-8')

  try:
    links = response.css('.kv ._Rm::text').extract()
    mp3party = ''
    for link in links:
      if 'mp3party.net' in link:
        mp3party = 'http://' + link
        break
    print mp3party 
    req = requests.get(mp3party,headers = headers)
    response = HR(url=mp3party, body = req.text, encoding='utf-8')
    audio = response.css('.jp-play::attr(href)').extract_first()
    print audio
  except:
    audio = ''
  return audio

def getCover(author, sing):
  reqStr = author + ' ' + sing
  reqStr = reqStr.replace(' ','+') 
  coverurl = 'https://www.google.ru/search?q=%s&newwindow=1&client=opera&hs=1DR&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjRus-zrLDYAhXNJVAKHZTsBPQQ_AUICigB&biw=1277&bih=673'%reqStr

  req = requests.get(coverurl, headers = headers)
  response = HR(url=coverurl, body = req.text, encoding='utf-8')

  img = response
  img = unicode(img.css('.rg_bx .rg_meta::text').extract_first())
  img = ast.literal_eval(img)
  img = img['ou']  
  return img

req = requests.get(url, headers = headers)
response = HR(url=url, body = req.text, encoding='windows-1251')

songs = response.css('.songs-holder > .jp-title').extract()

authors = response.css('.songs-holder > .jp-title > strong > a::text').extract()
sings = response.css('.songs-holder > .jp-title > span::text').extract()


List = []
for i in xrange(len(songs)):
  img = getCover(authors[i], sings[i])
  audio = getAudio(authors[i], sings[i])
  if audio == None:
    audio = ''
  List.append([authors[i], sings[i], img, audio, 'Russia', '2017'])

writeCSV(List, filename = 'Russia2017.csv')

#saveHTML(url,'test.html')

