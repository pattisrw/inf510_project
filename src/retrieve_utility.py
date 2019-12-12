import requests
import bs4
import constant_variables as cv # user-defined
from fake_useragent import UserAgent
import random
import json

# Debugging Tools for continuous_page_retrieval
_EXEC_DEBUG = {"proxy":0, "no-agent":0, "agent":0}
_DEBUG = False

def retrieve_json(api):
    """
        Returns the json object for the url corresponding to the API query string (as str)
    """
    page = requests.get(api)
    page.raise_for_status()
    try:
        return page.json()
    except ValueError:
        return None

def retrieve_page(url):
    """
        Returns the BeautifulSoup object of the given URL.
        URL: str
    """
    page = requests.get(url)
    page.raise_for_status()
    return bs4.BeautifulSoup(page.content, "html.parser")

def continuous_page_retrieval(session, url, proxies, tag_name=None):
    """
        session -  the requests.Session object,
        url - url of the web page as an integer,
        proxies - a list of proxies (str)
        tag_name (None by default) - str that designates which element to retrieve (used to reduce search time; not parse time)
        Returns BeautifulSoup or None

        Attempts to request the contents of the webpage (designated by url) using
        several of the randomly chosen proxies (at most 2 for efficiency) AND fake headers.
        If successful, returns the BeautifulSoup object of the webpage. If unsuccessful,
        attempts to request contents of webpage with fake headers but without proxies.
        If unsuccessful, then makes one last attempt to request contents of webpage with no
        fake headers and no proxies. If unsuccessful, returns None.

    """
    strainer = None
    if tag_name != None:
        strainer = bs4.SoupStrainer(tag_name)
    soup = retrieve_page_by_session(session, url, random.choice(proxies), True, strainer)
    n=0
    while(soup == None and n != 2):
        soup = retrieve_page_by_session(session, url, random.choice(proxies), True, strainer)
        n += 1
    if soup != None:
        if _DEBUG:
            _EXEC_DEBUG["proxy"] += 1
            print(_EXEC_DEBUG)
        return soup
    # If proxies do not work...
    soup = retrieve_page_by_session(session, url, None, True, strainer)
    if soup == None:
        if _DEBUG:
            _EXEC_DEBUG["no-agent"] += 1
            print(_EXEC_DEBUG)
        return retrieve_page_by_session(session, url, None, False, strainer)
    if _DEBUG:
        _EXEC_DEBUG["agent"] += 1
        print(_EXEC_DEBUG)
    return soup

def retrieve_page_by_session(session, url, proxy=None, agent=True, strainer=None):
    """
        Given the request.Session object and the page's url as str,
        returns the contents of the webpage as BeautifulSoup object (or None if page is
        too slow to respond or cannot be retrieved)

        optional args:
        - proxy (None by default) whether to request for the page using the given proxy (str)
        - agent (True by default) whether to use fake user header to request for the web page. (bool)
        - strainer (None by default) bs4.SoupStrainer object or None

        Note: For optimal efficiency, all queries with specified proxies have a timeout of 1.52
        Note: If a proxy is specified, then a fake user header is specified regardless of agent

        Usage: Only use with continuous_page_retrieval.
    """
    ua = UserAgent()
    if proxy==None and agent:
        try:
            page = session.get(url, headers = {"User-Agent": str(ua.firefox)})
        except:
            return None
    elif proxy == None and not agent:
        try:
            page = session.get(url)
        except:
            return None
    else:
        try:
            page = session.get(url, headers = {"User-Agent": str(ua.firefox)},
                            proxies={"http":proxy, "https":proxy}, timeout=1.52)
        except:
            return None
    page.raise_for_status()
    if strainer != None:
        return bs4.BeautifulSoup(page.content, "lxml", parse_only=strainer)
    return bs4.BeautifulSoup(page.content, "lxml")

def retrieve_valid_proxies(url, proxies):
    """
        url - the url of the website as str
        proxies -  a list of proxies (str),
        returns a list of all proxies (str) that is able to successfully query the webpage of URL

        Important note: this is not a strong guarantee that the resulting proxies
        will all be valid when inserted into retrieve_page_by_session. It simply
        filters out proxies that *for certain* is invalid

        note: the initial timeout for the queries is 1.4. However, if the len(result)=0, then
        the code will run once more with a timeout of 1.45, 1.5
    """
    result = []
    valid = True
    for proxy in proxies:
        try:
            page = requests.get(url, proxies={"http":proxy, "https":proxy}, timeout=1.4)
            # some proxies will not load, hence I need timeout to place a limit
        except:
            valid = False
        if valid:
            print(proxy)
            result.append(proxy)
        valid = True
    # As a failsafe against len(result) being 0
    n=1
    t = 1.4
    while len(result) == 0 and n<10: # just in case
        for proxy in proxies:
            try:
                page = requests.get(url, proxies={"http":proxy, "https":proxy}, timeout=t+0.5*n)
                # some proxies will not load, hence I need timeout to place a limit
            except:
                valid = False
            if valid:
                print(proxy)
                result.append(proxy)
            valid = True
        n+= 1

    return result

def retrieve_random_proxies(n):
    """
        Given integer n, retrieve a list of n proxies from free-proxy-list.net
    """
    if n<100 or n>200:
        raise Exception("n must be between 100 and 200 inclusive")
    url = cv.proxies_list_url
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, "html.parser")
    result = []
    all_rows = soup.findAll("tr")
    for i in range(1, n+1):
        row = all_rows[i]
        proxy = row.contents[0].contents[0] + ":" + row.contents[1].contents[0]
        result.append(proxy)
    print(result)
    return result

if __name__ == "__main__":
    # proxies = retrieve_valid_proxies("https://boxrec.com/en/locations/people", retrieve_random_proxies(70))
    # with requests.Session() as session:
    #     soup = continuous_page_retrieval(session, "https://boxrec.com/en/locations/people", proxies)
    #     # print(soup)
    pass
