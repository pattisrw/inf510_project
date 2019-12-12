import retrieve_utility as rp
import json
import constant_variables as cv


def fetch_status(code: "2-digit str"):
    """
        code - a list of 2-digit country codes(str)
        using the World Bank API, http://api.worldbank.org/v2/country,

        returns the socioeconomic status as a string. If the country's data DNE,
        then simply return None
    """
    j = rp.retrieve_json(f"{cv.country_api}{code}?format=json")
    try:
        return (j[1][0]["incomeLevel"]["value"])
    except IndexError:
        return None # empty values

def get_incomes(country_codes: "list of 2-digit str"):
    """
        country_codes - a list of 2-digit country codes(str)
        using the World Bank API, http://api.worldbank.org/v2/country,

        returns a dict, where the keys are the 2-digit country codes and the values
        values are the corresponding socioeconomic status of each country. None if missing info.
    """
    result = dict()
    for code in country_codes:
        result[code] = fetch_status(code)
    return result

if __name__ == "__main__":
    pass
