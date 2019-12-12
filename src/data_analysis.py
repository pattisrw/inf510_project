import numpy as np
import matplotlib.pyplot as plt
import os

def get_correlation_coefficient(data: "list of 2-tuples"):
    """
        Given a list of coordinate pairs as 2-tuples, returns the
        correlation coefficient as expressed as a float between 0 and 1 inclusive
    """
    return float(np.corrcoef(*zip(*data))[0][1]) # remember that the result of np.corrcoef is a 2d array

def get_correlation_strength(r:float):
    """
        Given the correlation coefficient r, determines whether the linear Regression
        test indicates a Strong, Moderate, Weak, or Very Weak correlation.

        Returns one of the following str: "Strong", "Moderate", "Weak", "Very Weak"
    """
    if r>0.7:
        return "Strong, Positive"
    elif 0.5<r<=0.7:
        return "Moderate, Positive"
    elif 0.3<r<=0.5:
        return "Weak, Positive"
    elif -0.3<=r<=0.3:
        return "Very Weak"
    elif -0.5<=r<-0.3:
        return "Weak, Negative"
    elif -0.7<=r<0.5:
        return "Moderate, Negative"
    else:
        return "Strong, Negative"

def show_and_store_graph(data: "list of 2-tuples", version="f"):
    """
        data - the list of coordinate-pairs as 2-tuples
        version ("f" by default) must be string "f" or string "t". Otherwise,
            an ValueError will be raised. This string indicates the version of
            the program.

        saves and displays the scatterplot. If version is f, then stores scatterplot
        as data_full.png. If version is t, then stores scatterplot as data_test.png
    """
    if version not in ["f", "t"]:
        raise ValueError("Invalid version")
    plt.scatter(*zip(*data))
    if version == "f":
        plt.savefig(os.path.join("..", "data", "data_full.png"))
    else:
        plt.savefig(os.path.join("..", "data", "data_test.png"))
    plt.show()

if __name__ == "__main__":
    # print(get_correlation_coefficient([(0.87,4),(0.8,3),(0.5,2)]))
    # show_graph([(0.87,4),(0.8,3),(0.5,2)])
    # for i in range(10):
    #     print(-i*0.1, get_correlation_strength(-i*0.1))
    pass
