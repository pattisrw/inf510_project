import retrieve_utility as rp
import constant_variables as cv

def get_country_codes():
    """
        Returns a list of 2-digit country codes for every country
        from https://www.iban.com/country-codes
    """
    soup = rp.retrieve_page(cv.country_codes_url)
    codes_list = []
    table_body = soup.find("tbody")
    for row in table_body.findAll("tr"):
        data = row.contents
        country_name = data[1].contents[0]
        country_name = country_name.split("(")[0].strip()
        two_letter = data[3].contents[0]
        three_letter = data[5].contents[0]
        codes_list.append(two_letter)
    return codes_list

if __name__ == "__main__":
    # country_codes_url = "https://www.iban.com/country-codes"
    # s= dict()
    # t = list()
    # get_codes(rp.retrieve_page(country_codes_url), s, t)
    # print(s, t)
    pass
