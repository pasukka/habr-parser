# -*- coding: utf-8 -*-
from lxml import etree
import time as t
import os

# import requests
import requests
from bs4 import BeautifulSoup

class Document:
  def __init__(self, number):
    self.number = number
    self.hubs = []
    self.tags = []
    self.data = {}  # dictionary with number, text, hubs, tags
    self.list_of_keywords = []
    self.dict_of_keywords_used_together = {}
    self.txt_path = ''
    self.html_path = ''
    self.comments = True
    self.error = False
    self.count_hubs = 0

  def set_txt_path(self, path):
    self.txt_path = path
  
  def set_html_path(self, path):
    self.html_path = path

  def set_comments(self, comments):
    self.comments = comments
  
  def set_list_of_keywords(self, list_of_keywords):
    self.list_of_keywords = list_of_keywords

  def set_dict_of_keywords_used_together(self, dict_of_keywords_used_together):
    self.dict_of_keywords_used_together = dict_of_keywords_used_together

  def check_path(self):
    if self.txt_path:
      self.make_path(self.txt_path)
    else:
      self.error = True
    if self.html_path:
      self.make_path(self.html_path)
      self.error = False

  def make_path(self, path):
    if not os.path.exists(path):
      os.mkdir(path)

  def make_request(self):
    self.request = requests.get('https://habrahabr.ru/post/' + str(self.number) + '/')
    if not self.request:
      self.error = True
      if self.comments:
        print('No page')

  def extract_data(self, sleep):
    self.soup = BeautifulSoup(self.request.text, 'lxml')
    t.sleep(sleep)

    self.data['id'] = self.number
    time = self.soup.find("span", {"class": "tm-article-snippet__datetime-published"})
    if time:
      self.data['time'] = time.text

    if self.soup.find("h1", {"class": "tm-article-snippet__title"}):
      self.error = True
      if self.comments:
        print('No title')

  def set_hubs(self, list_of_hubs):
    for hub in list_of_hubs:
      hub = hub.text.replace(' *', '').rstrip()
      self.hubs.append(hub)
    self.data['hubs'] = self.hubs

  def set_tags(self, list_of_tags):
    self.tags = []
    for tag in list_of_tags:
      self.tags.append(tag.text)
    self.data['tags'] = self.tags

  def check_hub_existence(self, first_list, second_list):
    self.count_hubs = 0
    for word in first_list:
      if word in second_list:
        self.count_hubs += 1
        break

  def compare_hubs(self):
    list_of_hubs = self.soup.find_all("a", {"class": "tm-article-snippet__hubs-item-link"})
    list_of_tags = self.soup.find_all("a", {"class": "tm-tags-list__link"})
    
    self.set_hubs(list_of_hubs)
    self.set_tags(list_of_tags)
  
    if self.list_of_keywords:
      self.check_hub_existence(self.data['hubs'], self.list_of_keywords)
    
    if self.count_hubs == 0 and self.dict_of_keywords_used_together:
      for hub in self.data['hubs']:
        if hub in self.dict_of_keywords_used_together:
          self.check_hub_existence(self.dict_of_keywords_used_together[hub], self.data['hubs'])
    
    if not self.count_hubs:
      if self.comments:
        print('No hubs')

  def add_nonempty_line(self, line, prev_line, lines):
    if line and (prev_line != '\n' or line != '\n'):
      lines.append(line)
    
  def make_document(self, text, path, format):
    filepath = os.path.join(path, 'text_{}.{}'.format(self.number, format))
    if not os.path.exists(filepath):
      with open (filepath, 'w', encoding="utf-8") as file:
        lines = []
        prev_line = ''
        for line in text:
          self.add_nonempty_line(line, prev_line, lines)
          prev_line = line
        file.writelines(lines)
  
  def extract_text(self):
    for script in self.soup(["script", "meta", "noscript", "style", "link"]):
      script.decompose()

    classes = ['tm-footer', 'tm-article-sticky-panel',
              'tm-article-presenter__footer', 'tm-header__container',
              'tm-base-layout__header', 'pull-down__header']
    for i in classes:
      selects = self.soup.findAll("div", {"class": i})
      for match in selects:
        match.decompose()

    selects = self.soup.findAll("span", {"class": 'tm-user-info__user'})
    for match in selects:
        match.decompose()

    if len(self.soup.get_text(strip = True)) == 0:
      self.soup.extract()

    self.html_text = str(self.soup)
    self.txt_text = str(self.data)
    if self.html_path:
      self.make_document(self.html_text, self.html_path, 'html')
    if self.txt_path:
      self.make_document(self.txt_text, self.txt_path, 'txt')
  
  def process(self, sleep=0.2): 
    self.check_path()
    if not self.error:
      self.make_request()
    if not self.error:
      self.extract_data(sleep)
    if not self.error:
      self.compare_hubs()
    if not self.error:
      self.extract_text()