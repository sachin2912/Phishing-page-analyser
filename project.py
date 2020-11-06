import requests
import urllib
from bs4 import BeautifulSoup
from urllib.parse import * 
import socket


def get_url(url):

    page=requests.get(url)
    soup=BeautifulSoup(page.content,'html.parser')
    return soup,page



def get_all_anchor_tags(soup):
    all_tags={}

    a_tags = soup.find_all("a",href=True)

    for a_tag in a_tags:

        if a_tag["href"]!="#" and a_tag["href"]!="":
            parse_url = urlparse(a_tag["href"])
            all_tags[a_tag.get_text()] = list((a_tag["href"] ,parse_url))

    return all_tags


def get_IP(url):
    try :
        ip=socket.gethostbyname(url)
    except:
        ip=" Cannot be Found"
    
    return ip        


def parse_main_url(url):
    parse_url = urlparse(url) 
    return parse_url 




def get_headers(page):

    return page.headers


def get_meta_data(soup):
    meta_data = { meta['name'].lower(): meta['content'] for meta in soup.find_all('meta', attrs=dict(name=True, content=True))}

    return meta_data



def get_script(soup):
    script_tags = [script['src'] for script in soup.find_all('script', src=True)]


    return script_tags



def analyse_url(url):
    soup,page = get_url(url)
    result_pmu = parse_main_url(url)
    print (" "*20,"URL Information")
    print (" Protocol Used : ",result_pmu.scheme)
    print (" Hostname :" , result_pmu.netloc)
    print ("*"*155)
    result_gh = get_headers(page)
    print (" "*20,"Header Information")
    print (" Content-Type ",result_gh["Content-Type"])
    print (" Server ",result_gh["Server"])
    result_ip = get_IP(url)

    # print ("IP Address : ",result_ip)
    # print ("*"*155)
    print (" "*20,"Meta-Data")
    result_gmd = get_meta_data(soup)
    for key in result_gmd.keys():
        print (key," - ",result_gmd[key])

    print ("*"*155)
    print (" "*20,"Source of External Scripts used")
    result_script = get_script(soup)
    for i in result_script:
        print (i)
    print ("*"*155)
    
    ch = int(input(" Enter 1 to view all links to external page: "))
    if ch==1:
        result_a_tag = get_all_anchor_tags(soup)
        #
        # print (result_a_tag)
        for name in result_a_tag.keys():
            if result_a_tag[name][1].netloc!="" and result_pmu.netloc != result_a_tag[name][1].netloc:
                print (" Name : " ,name, " Redirect Link ",result_a_tag[name][0],end="    ")
            
                print ("The Hostname of external link does not match with given url ")
            # else:
            #     print ( u'\u2713' )    
        print ("*"*155)
    
    
url = input("Enter the url to be scanned : ")

analyse_url(url)
