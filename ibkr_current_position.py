# [1]:

''' Program to extract stocks and options from IBKR Activity Statement
    Generated from ibkr.com -> Reports -> Activity Statements -> "Options Only"
    Choose previous day's report in CSV format

    Date: 18 June 2017     Rev: 1.0
'''

import csv
import pandas as pd

# for stock price history...
import pandas_datareader.data as web        
from datetime import datetime, timedelta

raw_data = []                      # raw_data list extracted from yesterday's csv file
clean_data = []                    # data cleansed from raw_data


# [2]:

with open('datafiles/Yesterday.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',' )

    for row in reader:

        # filter for "Open Positions" without "Total"

        if (str(row[0]) == "Open Positions" and str(row[1]) != "Total" ):
            raw_data.append(row)    # Append raw_data list

show_df = pd.DataFrame(raw_data[0:9]) # Show the first 10 rows
show_df


# [3]:

# Rename dataframe header with first element of raw_data
df = pd.DataFrame(raw_data)
df.columns = df.iloc[0]
df = df[1:]

# Remove excess DataDiscriminator rows
df = df[df.DataDiscriminator != "DataDiscriminator" ]

df['Asset Category'] = df['Asset Category'].str.replace('Equity and Index Options','Options') # Shorten "Options" in Category

show_df = pd.DataFrame(df[0:5]) # Show the first 6 rows
show_df


# [4]:

# Replace "Open" column with date from the next row for "Summary"

df.loc[ df.DataDiscriminator=='Summary','Open'] = df.Open.shift(-1).str.slice(0,10)
df = df[ df.DataDiscriminator=='Summary' ]

df = df[df.DataDiscriminator == "Summary"] # Keep only the Summary rows in the dataset


# [5]:

# Simplify dataframe field names
df.columns.values[3] = 'Category'
df.columns.values[9] = 'Cost'
df.columns.values[11] = 'Close'


# [6]:

# Assign and Split Options into separate columns
df = df.assign(**df.Symbol.str.split(' ', expand=True).rename(columns={0:'Symbol', 1:'Expiry', 2:'Strike', 3:'Right'}))


# [7]:

# Assemble the most important fields
clean_data = df[['Open', 'Symbol', 'Category', 'Right', 'Strike', 'Currency','Expiry', 'Quantity', 'Mult', 'Cost', 'Close']]

show_df = pd.DataFrame(clean_data[0:5]) # Show the first 6 rows
show_df


# [8]:

#list out the 
Symbols = df.Symbol.unique()


# [12]:

end = datetime.today()
start = end - timedelta(days=5)        # days = days-to-subtract

price_hist = pd.DataFrame()

for symbol in Symbols:                  # needed for some suspect symbols like 'SHOP'
    try:
        f = web.DataReader(str(symbol), 'google', start, end)
    except:
        f = web.DataReader("NYSE:"+str(symbol), 'google', start, end)
    f['Symbol'] = symbol 
    price_hist = price_hist.append(f)

price_hist[:20]


# [ ]:



