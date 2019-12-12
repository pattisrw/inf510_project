import pickle
import os

# There are 4 levels of income. To run a Linear Regression, we have to convert the categorical
# variable of socioeconomic status to a reasonable numerical value. The higher the value, the higher the incomes
# the lower the value, the lower the income
STATUS = {"High income" : 3, "Upper middle income" : 2, "Lower middle income" : 1, "Low income": 0}


def format_data(boxers, incomes):
    """
        boxers - a dict representing each country's summed sampled winnings and totals
                - {"US":[399,480], ....}
        incomes - a dict representing each country's income Level
                - {"US":"High Income", ....}

        returns a list of tuples of merged data for each individual country (sampled_win_rate, STATUS(income))
        [(399/480, 3), ......]
    """
    result = []
    for country in boxers:
        if boxers[country][1] != 0 and incomes[country] != None:
            result.append( (boxers[country][0]/boxers[country][1], STATUS[incomes[country]]) )
    return result

def store_data(data: "list of tuples", version="f"):
    """
        data - a list of tuples to be serialized and stored into a file called data.pkl
        using the pickle module
        version ("f" by default) must be string "f" or string "t". Otherwise,
            an ValueError will be raised. This string indicates the version of
            the program.

        saves and displays the data. If version is f, then stores cleaned data
        as data_full.pkl. If version is t, then stores cleaned data as data_test.pkl
    """
    if version not in ["f", "t"]:
        raise ValueError("Invalid version")
    try:
        if version == "f":
            with open(os.path.join("..", "data", "data_full.pkl"), "wb") as f:
                pickle.dump(data, f)
        else:
            with open(os.path.join("..", "data", "data_test.pkl"), "wb") as f:
                pickle.dump(data, f)
    except FileNotFoundError:
        print("Cannot find data.pkl")
        raise

def load_data(version="f"):
    """
        version ("f" by default) must be string "f" or string "t". Otherwise,
            an ValueError will be raised. This string indicates the version of
            the program.

        loads the data. If version is f, then loads data
        from data_full.pkl. If version is t, then loads data from data_test.pkl
    """
    if version not in ["f", "t"]:
        raise ValueError("Invalid version")
    try:
        if version == "f":
            with open(os.path.join("..", "data", "data_full.pkl"), "rb") as f:
                return pickle.load(f)
        else:
            with open(os.path.join("..", "data", "data_test.pkl"), "rb") as f:
                return pickle.load(f)
    except FileNotFoundError:
        print("Cannot find data.pkl")
        raise

if __name__ == "__main__":
    # countries = ["US", "RU", "MX"]
    # boxers = {"US":[100,120], "RU":[0,1], "MX":[0,0]}
    # incomes = {"US":"High income", "RU":"Upper middle income", "MX":"Lower middle income"}
    # data=[]
    # format_data(data, boxers, incomes, countries)
    # print(data)
    # store_data(data)
    # data = load_data("data.pkl")
    # print(data)

    pass
