import json
from functools import reduce
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def get_data():
    return pd.read_excel("database.xlsx")


def search_by_string(data, q, col):
    choices = list(data[col])
    matches = process.extract(q, choices, limit=15)
    matches_labels = [a for a, b in matches]
    #results = data[data[col].isin(matches_labels)]
    results = reduce(pd.DataFrame.append, map(lambda x: data[data[col] == x], matches_labels))
    as_dict = results.to_dict(orient="records")
    return as_dict


def search_by_location(data, lat, lng):
    data["distance"] = (data["lat"].sub(lat).pow(2).add(data["lng"].sub(lng).pow(2))).pow(.5)
    data = data.sort_values("distance")
    as_dict = data.to_dict(orient="records")[:15]
    return as_dict


if __name__ == "__main__":
    data = get_data()
    search_by_string(data, "pizza", "name")
    search_by_location(data, 1.2915036, 103.7799142)
    #print(data["name"])
