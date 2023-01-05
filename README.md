# CoinGecko Portfolio Tracker
Script reads crypto portfolio entries from file provided as parameter and pulls pricing information from CoinGecko.
It allows to track portfolio state. Pricing feed is pulled via CoinGecko API.

## Requirements
 - Python 3.8 or newer

## Installation

1. Clone repository and create a Python virtual environment
```bash
$ git clone https://github.com/ChainTools-Tech/cg_portfolio_tracker
$ cd cg_portfolio_tracker
$ python -m venv ./venv
$ source venv/bin/activate
(venv) $
```

2. Install the requirements
```bash
(venv) $ python -m pip install -r requirements.txt
```

3. Install script
```bash
(venv) $ pip install -e .
```

## Configuration
Portfolio information is provided to cg_portfolio_trakcer in form of json file.
 - **general** section contains URL to CoinGecko API endpoint, which provides pricing details as well as denomination for portfolio valuation (default usd)
  - **portfolio** section is a list of portfolio entries, which are composed of coin id and amount of coins in wallet; coin id is value corresponding to "API id" listed in coin details on CoinGecko website

Example portfolio fole:
```json
{
  "general": [
    {
      "api_url": "https://api.coingecko.com/api/v3/coins/",
      "reference_currency": "usd"
    }
  ],
  "portfolio": [
    {
      "id": "algorand",
      "amount": 10078.138272
    },
    {
      "id": "litecoin",
      "amount": 11
    },
    {
      "id": "storj",
      "amount": 2006
    },
    {
      "id": "icon",
      "amount": 10018.42
    },
    {
      "id": "digibyte",
      "amount": 110564
    },
    {
      "id": "cosmos",
      "amount": 651
    },
    {
      "id": "sentinel",
      "amount": 2434132
    }
  ]
}
```



## Usage
Example script output for portfolio presented above.
```bash
(venv) $ cg_portfolio_tracker -f portfolio.json            
+------------+--------+----------+-------------+---------------+----------------+----------------+----------+---------+----------+----------+--------------+-------------+
|       Name | Symbol |       ID | Price (USD) |       Mkt cap |     Total supp |      Circ supp | %chg 24h | %chg 7d | %chg 14d | %chg 30d |       Amount | Value (USD) |
+------------+--------+----------+-------------+---------------+----------------+----------------+----------+---------+----------+----------+--------------+-------------+
|   Algorand |   algo | algorand |      0.1862 | 1,325,561,064 |  7,355,849,159 |  7,133,651,037 |    -1.61 |   11.40 |     7.48 |   -21.58 |    10,078.14 |    1,876.72 |
| Cosmos Hub |   atom |   cosmos |     10.0400 | 2,937,629,735 |              0 |    292,586,164 |    -2.04 |   10.07 |    13.62 |    -2.28 |       651.00 |    6,536.04 |
|   DigiByte |    dgb | digibyte |      0.0080 |   127,695,451 | 21,000,000,000 | 15,922,960,505 |     0.35 |    5.67 |    -1.12 |     6.14 |   110,564.00 |      886.66 |
|       ICON |    icx |     icon |      0.1541 |   138,555,678 |    953,739,558 |    900,186,962 |     0.73 |    4.37 |     0.66 |   -15.22 |    10,018.42 |    1,543.40 |
|   Litecoin |    ltc | litecoin |     74.8900 | 5,377,751,801 |     84,000,000 |     71,985,371 |    -1.88 |   13.00 |    14.69 |    -6.69 |        11.00 |      823.79 |
|   Sentinel |   dvpn | sentinel |      0.0002 |     3,388,397 | 19,882,787,142 | 14,108,167,217 |    -2.58 |    6.55 |    39.05 |   -17.18 | 2,434,132.00 |      584.58 |
|      Storj |  storj |    storj |      0.2562 |    36,640,457 |    424,999,998 |    143,787,439 |    -0.92 |    2.12 |    -5.16 |   -22.55 |     2,006.00 |      513.94 |
+------------+--------+----------+-------------+---------------+----------------+----------------+----------+---------+----------+----------+--------------+-------------+

```
In case of any questions contact support@chaintools.tech

