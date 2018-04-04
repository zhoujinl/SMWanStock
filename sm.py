# -*- coding:utf-8 -*-

import requests
proxies = {
  'http': 'http://10.10.1.10:3128',
  'https': 'http://10.10.1.10:1080',
}
requests.get('https://morvanzhou.github.io/tutorials/data-manipulation/scraping/1-01-understand-website/')

