import retrieve_countries as rc
import retrieve_utility as rp
import retrieve_income as ri
import retrieve_boxer_stats as rb
import constant_variables as cv
import data_processing as dp
import data_analysis as da

def remote_introduction():
    print("\n")
    print("Full version of the program will take approximately 40-45 minutes to execute, ")
    print("Test version of the program will take approximately 3-7 minutes to execute. \n")
    print("Please specify whether you wish to execute the test version (t) or the full version (f). ")

def local_introduction():
    print("Please specify whether you wish to load the test version (t) or the full version (f). ")

def get_operation_ui():
    while(True):
        print("Valid inputs: t or f")
        user_input = input("Enter the version ")
        if user_input == "t":
            print("\nYou are now running the *test* version. \n")
            return user_input
        elif user_input == "f":
            print("\nYou are now running the *full* version. \n")
            return user_input
        else:
            print("Invalid input\n")

def load_data_ui(version):
    if version not in ["f", "t"]:
        raise ValueError("Invalid version")
    print("\n============= Loading Data ============= \n\n")
    print(" - 1. Loading Data ...")
    data = dp.load_data(version)
    print(data)
    print("Done\n")
    return data

def format_and_store_ui(countries_list, incomes, boxers, version):
    if version not in ["f", "t"]:
        raise ValueError("Invalid version")
    print("\n============= Format and Store Data ============= \n\n")
    print(" - 1. Format and Store Data\n")
    data = dp.format_data(boxers, incomes)
    print("* Removed all zero-entries. * ")
    dp.store_data(data, version)
    print("Done\n")
    return data

def analyze_data_ui(data, version):
    if version not in ["f", "t"]:
        raise ValueError("Invalid version")
    print("\n============= Analyze Data ============= \n\n")
    print(data)
    coeff = da.get_correlation_coefficient(data)
    print(" - 1. Get Correlation Coefficient for Linear Regression...\n")
    print(f"correlation coefficient r = {coeff} ")
    print(f"Strength of Correlation between each country's boxer records and Income Level is {da.get_correlation_strength(coeff)}")
    print(f"with size n={len(data)} (** discarding all zero-entries **)")
    if version == "t":
        print("\nNote that the results in the test version do not reflect the accurate correlation")
    da.show_and_store_graph(data, version)
    print("\nDone\n")

def retrieve_raw_data_ui(version: "f or t"):
    if version not in ["f", "t"]:
        raise ValueError("Invalid version")

    print("\n============= Data Retrieval ============= \n\n")


    #1. Retrieve Countries
    print(f" - 1. Retrieving Country Lists from {cv.country_codes_url} ...")

    countries_list = rc.get_country_codes()
    print(countries_list)
    print("Done\n")

    #2. Retrieving Incomes
    print(f" - 2. Retrieving Income Level for Each Country from API: {cv.country_api} ...")
    print("(50-70 seconds)")

    incomes = ri.get_incomes(countries_list)
    print(incomes)
    print("*Incomes designated as 'None' means the World Bank API does not contain the entry*")
    print("Done\n")


    #3.Sampling Boxer Stats
    print(f" - 3. Sampling Boxer Stats from 10 random Countries from {cv.boxing_url} ...")
    if version == "t":
        n = 110
        print("(3-5 minutes)\n")
    else:
        n=150
        print("(40-45 minutes)")
    print(f"Retrieving {n} random proxies from {cv.proxies_list_url} ...")
    proxies = rp.retrieve_random_proxies(n)
    print("Done\n")
    print("Extracting Valid Proxies ...")
    print("(1-3 minutes)")
    valid_proxies = rp.retrieve_valid_proxies(cv.boxing_url, proxies)
    if len(valid_proxies)>6:
        valid_proxies = valid_proxies[:6] # for efficiency
    print("Done\n")
    if version == "t":
        print(f"Sampling Pro Boxers from {10} random countries...")
        print("country: [sampled_win_count, sampled_fight_count]")
        boxers = rb.sample_boxers_test(countries_list, valid_proxies, 10)
    else:
        print(f"Sampling Pro Boxers from all {len(countries_list)} countries...")
        print("country: [sampled_win_count, sampled_fight_count]")
        boxers = rb.sample_boxers(countries_list, valid_proxies)
    print("Done\n")
    return countries_list, incomes, boxers
