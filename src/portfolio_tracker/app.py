import os
import os.path
import sys
import json
import time

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from prettytable import PrettyTable

from modules import color_terminal


def retrieve_coin_data(api_url, api_headers = {}, api_params = {}, amount = 0):
    """
    Retrieves coin details from Coin Gecko API.

    Args:
        :api_url: URL to access coin info.
        :api_headers: additional header details for API call.
        :api_params: additional parameters for API call.
        :amount: amount of coin help in portfolio.

    Returns:
        :return: JSON data retrieved from API + information about coin amount in portfolio.
    """
    api_session = Session()
    api_session.headers.update(api_headers)

    try:
        api_response = api_session.get(api_url, params=api_params)
        api_json_data = json.loads(api_response.text)
        api_json_data["amount"] = amount
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    return api_json_data


def load_portfolio_file(file_name):
    """
    Reads JSON file with list of coins in portfolio.

    Args:
        :file_name: name of JSON file with portfolio items.

    Returns:
        :return: JSON data loaded from file.
    """
    print("Loading portfolio file...")
    if os.path.isfile(file_name):
        print("Processing: {}".format(file_name))
        with open(file_name, 'r') as json_file:
            json_data = json.load(json_file)
            return json_data
    else:
        print("File: {} does not exist. Exiting.".format(file_name))
        sys.exit()


def prepare_portfolio_data(raw_data):
    """
    Iterates through data read from portfolio file, build array with portfolio
    and pulls data via Coin Gecko API.

    Args:
        :param raw_data: portfolio data in JSON format.

    Returns:
        :return: array with objects representing portfolio items.
    """
    print("Preparing portfolio data...")
    coin_list = []

    for item in raw_data["general"]:
        api_url = item["api_url"]
        ref_curr = item["reference_currency"]

    for item in raw_data["portfolio"]:
        print(f'\x1b[1K\r-- Pulling {item["id"]} pricing data.', end = "")
        coin_list.append(retrieve_coin_data(api_url + item["id"], amount=item["amount"]))
        time.sleep(12)

    return coin_list, ref_curr


def portfolio_table(data_list, ref_currency):
    """
    Reads data from list of Coin objects, prepares and displays portfolio table.

    Args:
        :param data_list: list fo Coin objects with portfolio data.

    Returns:
        :return: nothing is returned from portfolio_table function.
    """
    print("Generating portfolio table...")
    total = 0
    coins_table = PrettyTable()
    coins_table.field_names = ["Name", "Symbol", "ID", "Price ({})".format(ref_currency.upper()),
                               "Mkt cap", "Total supp", "Circ supp", "%chg 24h", "%chg 7d",
                               "%chg 14d", "%chg 30d", "Amount", "Value ({})".format(ref_currency.upper())]

    coins_table.align = 'r'
    coins_table.sortby = 'Name'

    for obj in data_list:
        try:
            obj_m = obj["market_data"]
            coins_table.add_row([
                obj["name"],
                obj["symbol"],
                obj["id"],
                "{:,.4f}".format(obj_m["current_price"][ref_currency] if obj_m["current_price"][ref_currency] != None else 0),
                "{:,.0f}".format(obj_m["market_cap"][ref_currency] if obj_m["market_cap"][ref_currency] != None else 0),
                "{:,.0f}".format(obj_m["total_supply"] if obj_m["total_supply"] != None else 0),
                "{:,.0f}".format(obj_m["circulating_supply"] if obj_m["circulating_supply"] != None else 0),
                "{}{:,.2f}{}".format(color_terminal.Blue if obj_m["price_change_percentage_24h"] == None else color_terminal.Green if obj_m["price_change_percentage_24h"] > 0 else color_terminal.Red,
                                 obj_m["price_change_percentage_24h"] if obj_m["price_change_percentage_24h"] != None else 0,
                                 color_terminal.Color_Off),
                "{}{:,.2f}{}".format(color_terminal.Green if obj_m["price_change_percentage_7d"] > 0 else color_terminal.Red,
                                 obj_m["price_change_percentage_7d"],
                                 color_terminal.Color_Off),
                "{}{:,.2f}{}".format(color_terminal.Green if obj_m["price_change_percentage_14d"] > 0 else color_terminal.Red,
                                 obj_m["price_change_percentage_14d"],
                                 color_terminal.Color_Off),
                "{}{:,.2f}{}".format(color_terminal.Green if obj_m["price_change_percentage_30d"] > 0 else color_terminal.Red,
                                 obj_m["price_change_percentage_30d"],
                                 color_terminal.Color_Off),
                "{:,.2f}".format(obj["amount"]),
                "{:,.2f}".format(obj["amount"] * obj_m["current_price"][ref_currency])
            ])
            total += obj["amount"] * obj_m["current_price"][ref_currency]
        except KeyError as e:
            print(obj)
            coins_table.add_row([
                "None",
                "None",
                "None",
                "None",
                "None",
                "None",
                "None",
                "None",
                "None",
                "None",
                "None",
                "None",
                "None"
            ])

    print(coins_table)
    print("Total: {:,.2f} {}".format(total, ref_currency.upper()))