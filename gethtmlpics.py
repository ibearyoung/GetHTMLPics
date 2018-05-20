#!/usr/bin/python2
#-*- coding: utf-8 -*-

import re
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
#from html.entities import name2codepoint
import os
import urllib2

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.datas = []
        self.title = ''
        self.picURLs = []
        self.in_head = False

    def get_datas(self):
        return self.datas

    def get_title(self):
        return self.title

    def get_picURLs(self):
        return self.picURLs
        
    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            pics = re.compile(r'^http[s]?://(.*)\.(?:gif|jpg|jpeg|png|bmp)$')
            for k, v in attrs:
                if (k == 'src' or k == 'data-src') and pics.match(v):
                    self.picURLs.append(v)
        if tag == 'head':
            self.in_head = True


    def handle_endtag(self, tag):
        if tag == 'head':
            self.in_head = False

    def handle_startendtag(self, tag, attrs):
        pics = re.compile(r'^http://(.*)\.(?:jpg|jpeg|gif)$')

    def handle_data(self, data):
        if self.lasttag == 'title' and self.in_head == True:
            if data != None and len(data.strip()) > 0:
                self.title = data.decode('gbk').encode('utf-8')

    def handle_comment(self, data):
        co = 1

    def handle_entityref(self, name):
        er = 1

    def handle_charref(self, name):
        cr = 1


if __name__ == "__main__":
    highlight_yellow = "\033[1;33;40m"
    highlight_red = "\033[1;31;40m"
    default_color = "\033[0m"

    gallery_path = "/home/bear/Pictures/CLPics/GetByPython"
    pics_counter = 0
    expected_amount = 0

    # Input URL which contain the PICS:
    while(True):
        clurl = raw_input("Please Enter the URL:")
        if clurl != None and len(clurl.strip()) > 0:
            break

    #clurl = "http://www.baidu.com"
    #page_uri = clurl.split("/")[-1]
    #page_name = page_uri.split(".")[0]
    #print("S:  %s" %page_name)
    #cmd = "wget" + " " + clurl
    #print("CMD:%s" %cmd)
    #os.system(cmd)

    # Get HTML Page online:
    hdr = {'User-Agent':'Mozilla/5.0'}
    request = urllib2.Request(clurl, headers = hdr)
    response = urllib2.urlopen(request)
    page = response.read()

    parser = MyHTMLParser()
    parser.feed(page)

    #Get local HTML page
    #file_uri = "./" + page_uri
    #with open(file_uri, 'r') as f:
    #    parser.feed(f.read())

	# Prepare the storage dir:
    page_title = parser.get_title()
    print(highlight_yellow)
    print(page_title)
    print(default_color)
    dir_name = page_title.split('-')[0].strip()
    storage_path = os.path.join(gallery_path, dir_name)
    if os.path.exists(storage_path) == False:
        os.mkdir(storage_path)
    os.chdir(storage_path)

    # Download the Pics by wget:
    expected_amount = len(parser.get_picURLs())
    for url in parser.get_picURLs():
        pics_counter += 1
        print(highlight_red)
        print("Fetching picture No. %s of %s..." % (pics_counter, expected_amount))
        print(default_color)
        os.system("wget" + " " + url)

    print(highlight_yellow)
    print("%s pics get, EXPECTED %s" % (pics_counter, expected_amount))
    print(default_color)

    parser.close()


#                print(v.encode('iso-8859-1').decode('utf-8'))
