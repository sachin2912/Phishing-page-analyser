import requests
import urllib
from bs4 import BeautifulSoup
from urllib.parse import * 
import socket


def get_url(url):                                          # get contents of the page

    page=requests.get(url)
    soup=BeautifulSoup(page.content,'html.parser')
    return soup,page



def get_all_anchor_tags(soup):                            #get all anchor tag details
    all_tags={}

    a_tags = soup.find_all("a",href=True)

    for a_tag in a_tags:

        if a_tag["href"]!="#" and a_tag["href"]!="":
            parse_url = urlparse(a_tag["href"])
            all_tags[a_tag.get_text()] = list((a_tag["href"] ,parse_url))

    return all_tags


def get_IP(url):                                      #get IP address of the given url
    try :
        if ":" in url:
            idx=url.index(":")
            new_url=url[:idx]
            ip = socket.gethostbyname(new_url)
        else:
        
            ip=socket.gethostbyname(url)
    except:
        ip=" Cannot be Found"
    
    return ip        


def parse_main_url(url):                                  # get information about the url
    parse_url = urlparse(url)     
    return parse_url 




def get_headers(page):                                    # get header information of the page

    return page.headers


def get_meta_data(soup):                               # get meta data of the page
    meta_data = { meta['name'].lower(): meta['content'] for meta in soup.find_all('meta', attrs=dict(name=True, content=True))}

    return meta_data



def get_script(soup):                             # get external scripts of the page
    script_tags = [script['src'] for script in soup.find_all('script', src=True)]


    return script_tags



def analyse_url(url):                            # function to execute all the function defined above
    soup,page = get_url(url)
    result_pmu = parse_main_url(url)
    final_result = {} 
    
    final_result["URL Information"] =  list(( str(" Protocol Used : ") + result_pmu.scheme ,str(" Hostname : ") + result_pmu.netloc ))
    
    result_gh = get_headers(page)
    final_result["Header Information"] = list(( str(" Content-Type :") + result_gh["Content-Type"] , str(" Server : ") + result_gh["Server"]))
    
    result_ip = get_IP(result_pmu.netloc)
    
    if result_ip != " Cannot be Found":
        final_result["IP Address "] = result_ip
    
    result_gmd = get_meta_data(soup)
    
    temp_gmd = []
    for key in result_gmd.keys():
        temp_gmd.append((key+" - "+result_gmd[key]))
    
    final_result["Meta-Data"] = temp_gmd
    # result_script = get_script(soup)
    
    final_result["Source of External Scripts used"] = get_script(soup)
    
    # print (final_result)
    
    final_result["*"] =  str(u'\u2718')+"  - The Hostname of external link does not match with given url \n     " + str(u'\u2714')+"  - The Hostname of external link does match with given url "
    
    result_a_tag = get_all_anchor_tags(soup)
    # print (result_a_tag)
    temp_tags =[]
    count_w=0
    count_r=0
    for name in result_a_tag.keys():
        if result_a_tag[name][1].netloc != "" and result_pmu.netloc != result_a_tag[name][1].netloc:
            temp_tags.append(str(" Link Text : ") + name + str(" , Redirect Link: '") + result_a_tag[name][0] + str("'      ") + str(u'\u2718'))     
            count_w+=1
            
        else:
            temp_tags.append(str(" Link Text : ") + name + str(" , Redirect Link: '") + result_a_tag[name][0] + str("'      ") + str(u'\u2714'))   
            count_r+=1  
    final_result["All the anchor tags of the page "] = temp_tags
    final_result["Count of Redirects outside given URL hostname"] = count_w
    final_result[" Conclusion "] = " Can be a phishing page" if count_w>(count_r/2) else " seems to be safe "
    # print (final_result)
    return final_result

