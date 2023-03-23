from bs4 import BeautifulSoup
import csv
import datetime
import random
import time
import os
import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
user_agent_list = [
    # Chrome
    'Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11 Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/4.0 (compatible MSIE 9.0 Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1 WOW64 Trident/7.0 rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible MSIE 9.0 Windows NT 6.1 WOW64 Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1 Trident/7.0 rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2 WOW64 Trident/7.0 rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0 WOW64 Trident/7.0 rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible MSIE 9.0 Windows NT 6.0 Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3 WOW64 Trident/7.0 rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible MSIE 9.0 Windows NT 6.1 Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1 Win64 x64 Trident/7.0 rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible MSIE 10.0 Windows NT 6.1 WOW64 Trident/6.0)',
    'Mozilla/5.0 (compatible MSIE 10.0 Windows NT 6.1 Trident/6.0)',
    'Mozilla/4.0 (compatible MSIE 8.0 Windows NT 5.1 Trident/4.0 .NET CLR 2.0.50727 .NET CLR 3.0.4506.2152 .NET CLR 3.5.30729)',
    'Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Mozilla/5.0 (compatible U ABrowse 0.6 Syllable) AppleWebKit/420+ (KHTML, like Gecko)',
    'Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0 WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0 WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36 OPR/36.0.2130.32',
    'Opera/9.80 (Windows NT 6.1 WOW64) Presto/2.12.388 Version/12.18',
    'Mozilla/5.0 (Windows NT 10.0 WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991',
    'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
    'Opera/9.80 (Windows NT 5.1 WOW64) Presto/2.12.388 Version/12.17'
]
#------ask password------
title = ['ASIN', 'URL', 'NAME', 'PRICE', 'MODEL NUMBER']

page_Num = 1
export_date = datetime.datetime.now()
export_fname = export_date.strftime('%m') + '.' + \
               export_date.strftime('%d') + '.' + \
               export_date.strftime('%Y')   # not compelete file name, after this add watch or headset

def get_tag_of_search_list(soup):
    tags = soup.find('div', {'class' : 's-result-list s-search-results sg-row'})    #watches, headsets
    return tags

def get_tag_of_all_NAME(soup):
    tags = soup.find_all('span', {'class': "a-size-medium a-color-base a-text-normal"})
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

def is_restricted(soup):
    tags = soup.find('i', {'class' : 'a-icon a-icon-VOB-restricted a-icon-small'})
    if tags == None:
        return False
    else:
        return True

def is_trending(soup):
    tags = soup.find_all('span', {'class': 'a-size-large a-color-base'})
    if tags == []:
        return False
    else:
        for tag in tags:
            if tag.get_text().strip() == 'Trending products':
                return True
        return False

def is_out_of_stock(soup):
    tags = soup.find('span', {'aria-label' : 'Temporarily out of stock.'})
    if tags == None:
        return False
    else:
        return True

def get_NAME(soup):
    tag = soup.find('span', {'class' : "a-size-medium a-color-base a-text-normal"})
    return tag.get_text().strip()
#---------Every Page URL, URL is not different type from the others--------- @@@@@@@@@@@@@ MODIFY ---------------

url_first = 'https://www.amazon.co.uk/s?k=binoculars&i=electronics&rh=n%3A560798%2Cn%3A560834%2Cn%3A1083928%2Cp_n_shipping_option-bin%3A2023186031%2Cp_is_offer_tax_enabled%3A15426189031&dc&crid=15JEXVMRRHGHY&qid=1569521102&rnid=15426188031&sprefix=binoculras%2Caps%2C223&ref=sr_nr_p_is_offer_tax_enabled_1'
url_base = ''
export_fname += '_bino.csv'

#---------csv file opened? check---------
if os.path.exists(export_fname):
    try:
        os.rename(export_fname, export_fname + '_')
        os.rename(export_fname + '_', export_fname)
    except OSError as e:
        print("CSV file opened. After close, and then Try.")
        exit()

bug_file = open('error_pages.txt', 'w')
url_file = open('url.txt', 'w')
db_file = open("DB_bino.txt", 'r')
db_list = db_file.readlines()

idx = 0
while True:
    if idx >= len(db_list):
        break
    line = db_list[idx]
    line = line[:line.find('\n')]
    db_list[idx] = line
    idx += 1

chroptions = Options()
chroptions.add_argument("--ignore-certificate-errors")
chroptions.add_argument("--ignore-ssl-errors")
chroptions.add_argument("--system-developer-mode")
chroptions.add_argument("--no-first-run")
# chroptions.add_argument("--enable-automation")
# chroptions.add_argument("--disable-automation")

chroptions.add_argument("--disable-infobars")
chroptions.add_argument("--disable-popup-blocking")

# chroptions.add_argument("--user-data-dir=User Data")        # sign in case

driver = webdriver.Chrome(options=chroptions)

driver.implicitly_wait(5)
driver.maximize_window()

url = url_first

driver.get("https://www.amazon.co.uk/ap/signin?_encoding=UTF8&ignoreAuthState=1&openid.assoc_handle=gbflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.co.uk%2F%3Fref_%3Dnav_signin&switch_account=")
input("Please sign in. And then press Enter to continue.")
time.sleep(3)
driver.get(url)

with open(export_fname, mode = 'w', newline='', errors='ignore') as csv_file:
    page_No = 1
    writer = csv.writer(csv_file)
    writer.writerow(title)
    while True:

        url = driver.current_url
        url_file.write(url + '\n')

        sys.stdout.write('\r' + 'scraping page No.' + str(page_No) + ' ...')

        retry_num = 0
        error_retry_num = 0

        while True:
            time.sleep(random.randint(5, 10))
            try:
                user_agent = random.choice(user_agent_list)
                headers = {'User-Agent': user_agent}

                soup = BeautifulSoup(driver.page_source, "html.parser")
                soup_search_list = get_tag_of_search_list(soup)

                if soup_search_list == None or driver.page_source.find("captcha") != -1:
                    retry_num += 1
                    if retry_num == 2:
                        print("Can't scrap page No." + page_No)
                        break
                    time.sleep(600)
                    driver.get(url)
                    continue

                products = []

                #--------get_page_Num-----------
                if page_No == 1:
                    tags_page_Num = get_tag_of_pageNum(soup)
                    tmp = tags_page_Num[len(tags_page_Num) - 1].get_text().strip()
                    page_Num = int(tmp)
                    print(page_Num)

                #--------get_NAME---------------
                # i = 0
                # tags_NAME = get_tag_of_all_NAME(soup_search_list)
                # Num_products = len(tags_NAME)
                # while i < Num_products:
                #     products.append(['', '', tags_NAME[i].get_text().strip(), '', ''])
                #     i += 1
                #--------get_ASIN---------------
                i = 0
                tags_ASIN = get_tag_of_all_ASIN_INDEX(soup_search_list)
                # while i < len(tags_ASIN):
                #     index = tags_ASIN[i].attrs['data-index']
                #     asin = tags_ASIN[i].attrs['data-asin']
                #     products[int(index)][0] = asin.strip()
                #     i += 1
                #error_message----------
                # if len(tags_ASIN) != Num_products:
                #     print('asin num != name num : ' + url)
                #     exit()

                #--------get_image_URL_PRICE----------
                Num_products = len(tags_ASIN)

                while i < Num_products:
                    soup_per_products = tags_ASIN[i]

                    name = get_NAME(soup_per_products)
                    asin = soup_per_products.attrs['data-asin'].strip()

                    if asin == "" or is_restricted(soup_per_products) == True:
                        i += 1
                        continue

                    if is_out_of_stock(soup_per_products) == True:
                        i += 1
                        continue

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
                    PRICE = PRICE[1: ]

                    model_num = ""
                    for model_num_line in db_list:
                        if model_num_line.split(',')[0] == asin:
                            model_num = model_num_line.split(',')[1]
                            break

                    products.append([asin, URL_str, name, PRICE, model_num])

                    i += 1

                i = 0
                while i < len(products):
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
                time.sleep(300)
                driver.get(url)
                continue

        try:
            xpath = "//li[@class='a-last']"
            driver.find_element_by_xpath(xpath).click()

        except NoSuchElementException:
            break

        page_No += 1
        if page_No > page_Num:  # sign in case
            break

csv_file.close()
bug_file.close()
url_file.close()
db_file.close()
driver.quit()

print('-----THE_END-----')