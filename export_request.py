from bs4 import BeautifulSoup
import csv
import datetime
import urllib.request
import urllib.response
import random
import time
import requests
import os
import sys
from itertools import cycle
user_agent_list = [
    # Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    # Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'

    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36 OPR/36.0.2130.32'
    'Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.18'
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991'
    'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14'
    'Opera/9.80 (Windows NT 5.1; WOW64) Presto/2.12.388 Version/12.17'
]
#------ask password------
title = ['ASIN', 'URL', 'NAME', 'PRICE']

page_Num = 1
export_date = datetime.datetime.now()
export_fname = export_date.strftime('%m') + '.' + \
               export_date.strftime('%d') + '.' + \
               export_date.strftime('%Y')   # not compelete file name, after this add watch or headset

def get_tag_of_search_list(soup):
    tags = soup.find('div', {'class' : 's-result-list s-search-results sg-row'})    #watches, headsets
    return tags

def get_tag_of_all_NAME(soup):
    #tags = soup.find_all('span', {'class' : "a-size-medium a-color-base a-text-normal"})   #headsets
    #tags = soup.find_all('span', {'class': "a-size-base-plus a-color-base a-text-normal"})  #watches
    tags = soup.find_all('span', {'class': XPATH_NAME})
    return tags

def get_tag_of_all_ASIN_INDEX(soup):
    tags = soup.find_all('div', {'data-asin' : True, 'data-index' : True})      #watches, headsets
    return tags

def get_tag_of_all_image_URL(soup):
    tags = soup.find_all('img')     #watches, headsets
    return tags

def get_tag_of_all_PRICE(soup):
    tags = soup.find_all('span', {'class' : 'a-price', 'data-a-size' : "l", 'data-a-color' : "base"})   #watches, headsets
    return tags

def get_subtag_of_all_PRICE(soup):
    sub_tags = soup.find_all('span', {'class' : 'a-offscreen'})     #watches, headsets
    return  sub_tags

def get_tag_of_all_incl_PRICE(soup):
    tags = soup.find_all('span', {'class' : 'a-price', 'data-a-size' : "b", 'data-a-color' : "secondary"})  # watches, headsets
    return tags

def get_tag_of_excl(soup):
    tags = soup.find_all('span', {'class' : 'a-size-base a-color-base'})
    return tags

def get_tag_of_incl(soup):
    tags = soup.find('span', {'class' : 'a-color-secondary'})
    return tags

def get_tag_of_pageNum(soup):
    tags = soup.find_all('li', {'class' : 'a-disabled'})    #watches, headsets
    return tags

#---------Every Page URL, URL is not different type from the others--------- @@@@@@@@@@@@@ MODIFY ---------------
url_first = ''
url_base = ''
XPATH_NAME = ''
while True:
    flag = input('Watches or Cars Audio? press [ w \ c ], If close, press [ x ] : ')
    if flag == 'w':
        XPATH_NAME = "a-size-base-plus a-color-base a-text-normal"
        url_first = 'https://www.amazon.co.uk/s?bbn=10103528031&rh=n%3A328228011%2Cn%3A%21328229011%2Cn%3A10103528031%2Cp_76%3A419158031&dc&fst=as%3Aoff&qid=1559673226&rnid=419157031&ref=lp_10103528031_nr_p_76_0'
        url_base = 'https://www.amazon.co.uk/s?i=watches&bbn=10103528031&rh=n%3A328228011%2Cn%3A328229011%2Cn%3A10103528031%2Cp_76%3A419158031&dc&page='
        export_fname +=  '_watches.csv'
        break
    # elif flag == 'h':
    #     XPATH_NAME = "a-size-medium a-color-base a-text-normal"
    #     url_first = 'https://www.amazon.co.uk/s?k=headsets&i=electronics&rh=n%3A560798%2Cn%3A4085731%2Cp_76%3A419158031%2Cp_is_offer_tax_enabled%3A15426189031&dc&qid=1559750396&rnid=15426188031&ref=sr_nr_p_is_offer_tax_enabled_1'
    #     url_base = 'https://www.amazon.co.uk/s?k=headsets&i=electronics&rh=n%3A560798%2Cn%3A4085731%2Cp_76%3A419158031%2Cp_is_offer_tax_enabled%3A15426189031&dc&page='
    #     #url_base = 'https://www.amazon.co.uk/s?k=headsets&i=electronics&rh=n%3A4085731%2Cp_76%3A419158031%2Cp_is_offer_tax_enabled%3A15426189031&dc&page='
    #     export_fname += '_headsets.csv'
    #     break
    elif flag == 'c':
        XPATH_NAME = "a-size-medium a-color-base a-text-normal"
        url_first = 'https://www.amazon.co.uk/s?i=electronics&bbn=3030791&rh=n%3A560798%2Cn%3A560800%2Cn%3A3030781%2Cn%3A1342661031%2Cn%3A3030851%2Cn%3A3030791%2Cp_is_offer_tax_enabled%3A15426189031&dc&fst=as%3Aoff&qid=1562216348'
        url_base = 'https://www.amazon.co.uk/s?i=electronics&bbn=3030791&rh=n%3A560798%2Cn%3A560800%2Cn%3A3030781%2Cn%3A1342661031%2Cn%3A3030851%2Cn%3A3030791%2Cp_is_offer_tax_enabled%3A15426189031&dc&page='
        url_first_iz = 'https://www.amazon.co.uk/s?i=electronics&bbn=3030791&rh=n%3A560798%2Cn%3A560800%2Cn%3A3030781%2Cn%3A1342661031%2Cn%3A3030851%2Cn%3A3030791%2Cp_is_offer_tax_enabled%3A15426189031&dc&fst=as%3Aoff&qid=1562216348&rnid=419157031&ref=sr_nr_p_76_1'

        export_fname += '_car.csv'
        break
    elif flag == 'x':
        exit()
    else:
        print('Input invalid. Try input.')

#---------csv file opened? check---------
if os.path.exists(export_fname):
    try:
        os.rename(export_fname, export_fname + '_')
        os.rename(export_fname + '_', export_fname)
    except OSError as e:
        print("CSV file opened. After close, and then Try.")
        exit()

bug_file = open('error_pages.txt', 'w')
with open(export_fname, mode = 'w', newline='', errors='ignore') as csv_file:
    page_No = 1
    url = ''
    writer = csv.writer(csv_file)
    writer.writerow(title)
    while page_No <= page_Num:
        if page_No == 1:
            url = url_first
        else:
            url = url_base + str(page_No)

        sys.stdout.write('\r' + 'scraping page No.' + str(page_No) + ' ...')

        retry_num = 0
        error_retry_num = 0

        while True:
            time.sleep(random.randint(10, 30))
            try:
                user_agent = random.choice(user_agent_list)
                headers = {'User-Agent': user_agent}
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}
                try:
                    request = urllib.request.Request(url, headers=headers)
                    response = urllib.request.urlopen(request)
                    html_doc = response.read()
                except Exception as ee:
                    print('\n')
                    print(ee)
                    print("In request, Error occured.")
                    csv_file.close()
                    bug_file.close()
                    input('Press Enter to exit.')
                    exit()

                soup = BeautifulSoup(html_doc, "html.parser")
                soup_search_list = get_tag_of_search_list(soup)

                if soup_search_list == None or html_doc.find(str.encode("captcha")) != -1:
                    retry_num += 1
                    if retry_num == 2:
                        print("Can't scrap page No." + page_No)
                        break
                    print("Robot?... After 5 minutes, will retry.")
                    time.sleep(300)
                    continue

                products = []

                #--------get_page_Num-----------
                if page_No == 1:
                    tags_page_Num = get_tag_of_pageNum(soup)
                    tmp = tags_page_Num[len(tags_page_Num) - 1].get_text().strip()
                    page_Num = int(tmp)
                    print(page_Num)

                #--------get_NAME---------------
                i = 0
                tags_NAME = get_tag_of_all_NAME(soup_search_list)
                Num_products = len(tags_NAME)
                while i < Num_products:
                    products.append(['', '', tags_NAME[i].get_text().strip(), ''])
                    i += 1
                #--------get_ASIN---------------
                i = 0
                tags_ASIN = get_tag_of_all_ASIN_INDEX(soup_search_list)
                while i < len(tags_ASIN):
                    index = tags_ASIN[i].attrs['data-index']
                    asin = tags_ASIN[i].attrs['data-asin']
                    products[int(index)][0] = asin.strip()
                    i += 1
                #error_message----------
                if len(tags_ASIN) != Num_products:
                    print('asin num != name num : ' + url)
                    exit()

                #--------get_image_URL_PRICE----------
                i = 0
                while i < Num_products:
                    soup_per_products = tags_ASIN[i]
                    tag_URL = get_tag_of_all_image_URL(soup_per_products)
                    URL_str = ''
                    #error_message----------
                    if len(tag_URL) >=2:
                        print('here 2 images : ' + products[i][1])
                    URL_str = tag_URL[0].attrs['srcset']            #com recognize that tag_URL is the result.
                    temp = URL_str
                    while True:
                        end_pos = temp.find('.jpg') + 4
                        temp_url = temp[temp.find('https') : end_pos]
                        temp = temp[end_pos : ]
                        if temp.find('https') == -1:
                            URL_str = temp_url
                            break
                    products[i][1] = URL_str
                    #-------------------------------
                    tag_PRICE = get_tag_of_all_PRICE(soup_per_products)
                    PRICE = ''
                    if len(tag_PRICE) == 1:
                        subtag_PRICE = get_subtag_of_all_PRICE(tag_PRICE[0])
                        tag_excl = get_tag_of_excl(soup_per_products)
                        #error_message------------
                        if len(subtag_PRICE) >= 2:
                            print('here 2 price : ' + products[i][1])
                        if len(tag_excl) == 0:
                            PRICE = subtag_PRICE[0].get_text().strip()
                        else:
                            tag_incl = get_tag_of_incl(soup_per_products)
                            if len(tag_incl) == 1:
                                tag_incl_PRICE = get_tag_of_all_incl_PRICE(soup_per_products)
                                subtag_incl_PRICE = get_subtag_of_all_PRICE(tag_incl_PRICE[0])
                                PRICE = subtag_incl_PRICE[0].get_text().strip()
                    products[i][3] = PRICE[1: ]
                    i += 1

                i = 0
                while i < Num_products:
                    if products[i][3] != '':
                        writer.writerow(products[i])
                    i += 1

                print('Successfully scraped from ' + url)
                print('completed ' + str(page_No) + '/' + str(page_Num))
                break

            except Exception as e:
                print(e)
                print(url)
                error_retry_num += 1
                if error_retry_num == 2:
                    print('Cant scrap the page No.' + str(page_No) + '\n')
                    bug_file.write(str(page_No) + '\n')
                    if page_No == 1:
                        input('Try again. Press Enter to exit...')
                        exit()
                    error_retry_num = 0
                    break
                print("Robot?... After 5 minutes, will retry.")
                time.sleep(300)
                continue
        page_No += 1

        if (page_No == 3):          ###################################################
            break
csv_file.close()
bug_file.close()
input('Press Enter to exit.')




