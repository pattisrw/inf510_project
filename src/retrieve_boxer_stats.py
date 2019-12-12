import retrieve_utility as rp
import requests
import constant_variables as cv
import random

def get_boxers_by_page(session, stats:dict, country, offset, boxing_url, proxies):
    """
        session -  the request.Session object
        stats -  a dict used to store the statistics
        country -  a 2-digit country code representing the country as a string
        offset -  int representing the page. each page represents an offset of 20.
        boxing_url -  the url of the boxing page as str
        proxies -  the list of valid proxies as returned by rp.retrieve_valid_proxies.

        samples boxers and stores statistics into stats dict
        *This function should only run implicitly from sample_boxers(country_list, proxies)*
    """
    url = f"{boxing_url}?l[country]={country}&offset={offset}"
    soup = rp.continuous_page_retrieval(session, url, proxies, "span")
    if soup == None:
        return None
    results = soup.findAll("span", {"class":["textWon","textLost", "textDraw"]})
    if(len(results)==0):
        return None
    for i in range(int(len(results)/3)):
        wins = int(results[i*3].contents[0])
        losses = int(results[i*3+1].contents[0])
        draws = int(results[i*3+2].contents[0])
        if country not in stats:
            stats[country] = [wins, wins+losses+draws]
        else:
            stats[country][0] += wins
            stats[country][1] += wins+losses+draws
    return None

def sample_boxers_by_country(session, stats:dict, country, boxing_url, proxies, max_pages=5):
    """
        session -  the request.Session object
        stats -  a dict used to store the statistics
        country -  a 2-digit country code representing the country as a string
        boxing_url -  the url of the boxing page as a str
        proxies -  the list of valid proxies as returned by rp.retrieve_valid_proxies
        max_pages (3 by default) - maximum number of pages to be queried at random (int)

        samples boxers and stores statistics into stats dict
        *This function should only run from sample_boxers(country_list, proxies)*
    """
    #find max offset
    url = f"{boxing_url}?l[country]={country}&offset={0}"
    soup = rp.continuous_page_retrieval(session, url, proxies, "a")
    if soup==None:
        stats[country] = [0,0]
        return None
    all_links = soup.findAll("a", {"class":"alt"})
    if(len(all_links)<=2): # login, register links do not count
        get_boxers_by_page(session, stats, country, 0, boxing_url, proxies)
        if country not in stats:
            stats[country] = [0,0] # if nothing on page
        return None
    try:
        num = int(all_links[-2].contents[0])
    except ValueError: # should never happen
        stats[country] = [0,0]
        return None
        get_boxers_by_page(session, stats, country, 0, boxing_url, proxies)
    else: # has links = more than one page
        if num < max_pages:
            max_pages = num
        for n in random.sample(range(num),max_pages):
            get_boxers_by_page(session, stats, country, 20*n, boxing_url, proxies)
    finally:
        pass

def sample_boxers(country_list, proxies):
    """
        country_list - a list of 2-digit country codes as a list of string
        proxies -  the list of valid proxies as returned by rp.retrieve_valid_proxies,

        returns a dict, where the keys are the country codes and the values are a list
        of the form [summed_wins, summed_total_fights] among *sampled* boxers.
    """
    stats = dict()
    with requests.Session() as session:
        post = session.post(cv.boxing_login, data=cv.login_info)
        for country in country_list:
            sample_boxers_by_country(session, stats, country, cv.boxing_url, proxies)
            if country in stats:
                print(country, stats[country])
            else: # purely for testing
                print(country, None)
    return stats

def sample_boxers_test(country_list, proxies, n):
    """
        country_list - a list of 2-digit country codes as a list of string
        proxies -  the list of valid proxies as returned by rp.retrieve_valid_proxies,
        n - number of countries to be sampled (int)

        returns a dict, where the keys are some random country codes (exactly n) and the values are a list
        of the form [summed_wins, summed_total_fights] among *sampled* boxers.
    """
    stats = dict()
    with requests.Session() as session:
        post = session.post(cv.boxing_login, data=cv.login_info)
        randomize_country = random.sample(country_list, n)
        for country in randomize_country:
            sample_boxers_by_country(session, stats, country, cv.boxing_url, proxies)
            if country in stats:
                print(country, stats[country])
            else:
                print(country, None) # purely for testing
    return stats


if __name__ == "__main__":
    pass
