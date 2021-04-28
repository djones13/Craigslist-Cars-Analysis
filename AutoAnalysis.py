"""
Name: Dylan Jones
CS230: Section SN1
Data: Used cars for sale on Craigslist
URL: Link to your web application online (see extra credit)

Description: This program will examine the large dataset of used cars listed on Craigslist, performing various
comparisons across manufacturers, models, years, and conditions.
The first interactive bar chart shows trends in average price listings across 5 possible categories. The bar color
can be customized using the color selector in the sidebar
Secondly is a map displaying each of the listings' locations.
"""

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import statistics


def barchart(xlist, ylist, xlabel, ylabel, title, height, color, size=22, rot=90):
    f = plt.figure()
    f.set_figwidth(25)
    f.set_figheight(height)  # Allows different heights to be used for different data, for better fits
    plt.bar(xlist, ylist, color=color)
    plt.xticks(xlist, rotation=rot, size=size, family='serif')
    plt.yticks(size=22, family='serif')
    plt.xlabel(xlabel, size=32, family='serif')
    plt.ylabel(ylabel, size=32, family='serif')
    plt.title(title, size=42, family='serif')
    plt.grid(axis='y')

    return plt


def read_data(fileName, columns):  # From Harrison's review session
    df = pd.read_csv(fileName)
    lst = []

    for index, row in df.iterrows():
        sub = []
        for col in columns:
            index_no = df.columns.get_loc(col)
            sub.append(row[index_no])
        lst.append(sub)

    return lst


def get_unique(data, col):
    unique = []

    for i in range(len(data)):
        if data[i][col] not in unique and not pd.isnull(data[i][col]):  # Makes sure there are no 'NaN' in our data
            unique.append(data[i][col])
    unique.sort()  # Sort in descending order (numerically or alphabetically)
    return unique

# Average function to iterate through the data and pull all of the prices of listings that match certain criteria,
# then calculate the average. (ex. iterate through data to find all listings in MA, store all those prices in a list,
# then average the list, and return that value)
def average(data, col, value):
    prices = []
    for i in range(len(data)):
        if data[i][col] == value:  # Check if criteria is matched for that listing
            price = data[i][0]  # Grab price from that listing if criteria is matched
            prices.append(price)
    avg = statistics.mean(prices)
    return avg


# Import data as data frame
columns = ['price', 'year', 'manufacturer', 'condition', 'type', 'state']
data_list = read_data("cars.csv", columns)

# Title and initial formatting for StreamLit UI
st.title("Craigslist Used Cars Listings")
st.header("Average Listed Prices:")

# Bar chart of stats by manufacturer
sort = ['year', 'manufacturer', 'condition', 'type', 'state']
type = st.sidebar.radio("Select a graph filter: ", sort)

years = get_unique(data_list, 1)
manufacturers = get_unique(data_list, 2)
conditions = ['salvage', 'fair', 'good', 'excellent', 'like new', 'new']
types = get_unique(data_list, 4)
states = get_unique(data_list, 5)

title = "Average Listed Price by "
ylabel = "Average Listed Price"

color = st.sidebar.color_picker("Choose a graph color: ")

# Create bar charts unique to each user-selection

if type == "year":
    xlist = years
    ylist = []

    for year in years:
        ylist.append(average(data_list, 1, year))

    xlabel = "Year"
    title = title + "Year"
    st.pyplot(barchart(xlist, ylist, xlabel, ylabel, title, 7.5, color, 14))

elif type == 'manufacturer':
    xlist = manufacturers
    ylist = []

    for manufacturer in manufacturers:
        ylist.append(average(data_list, 2, manufacturer))

    xlabel = "Manufacturer"
    title = title + "Manufacturer"
    st.pyplot(barchart(xlist, ylist, xlabel, ylabel, title, 10, color))

elif type == 'condition':
    xlist = conditions
    ylist = []

    for condition in conditions:
        ylist.append(average(data_list, 3, condition))

    xlabel = "Conditions"
    title = title + "Conditions"
    st.pyplot(barchart(xlist, ylist, xlabel, ylabel, title, 5, color, rot=0))

elif type == "type":
    xlist = types
    ylist = []

    for thing in types:
        ylist.append(average(data_list, 4, thing))

    xlabel = "Type"
    title = title + "Type"
    st.pyplot(barchart(xlist, ylist, xlabel, ylabel, title, 5, color, rot=30))

elif type == "state":
    xlist = [state.upper() for state in states]  # Capitalize state abbreviations
    ylist = []

    for state in states:
        ylist.append(average(data_list, 5, state))

    xlabel = "State"
    title = title + "State"
    st.pyplot(barchart(xlist, ylist, xlabel, ylabel, title, 15, color,))

# Grab new data (list of lists) for map
columns = ['price', 'year', 'manufacturer', 'model', 'state', 'lat', 'long']
map_data = read_data('cars.csv', columns)

# Change list of lists into data frame
map_df = pd.DataFrame(map_data, columns=['price', 'year', 'manufacturer', 'model', 'state', 'lat', 'lon'])

# Remove rows containing NaN
map_df = map_df.dropna(subset=['lat', 'lon'])

# Create two-ended slider to choose map price range
minimum = int(map_df['price'].min())
maximum = int(map_df['price'].max())

# (Default range is $1,000 - $100,000)
values = st.sidebar.slider('Choose a price range for the map: ', min_value=minimum, max_value=maximum, value=(1000, 100000))

# Add manufacturer checkbox to filter map
choices = st.sidebar.multiselect("Choose manufacturer(s):", options=manufacturers)

# Filter map_df for listings within range
filter_range = [num for num in np.arange(values[0], values[1], 1)]
filtered_df = map_df[map_df['price'].isin(filter_range)]
filtered_df = filtered_df[filtered_df['manufacturer'].isin(choices)]

# Create map
st.header('Map')
st.map(filtered_df)

st.write(f"Showing cars listed between ${values[0]} and ${values[1]}")
st.write(f"Cars made by {choices} are showing.")
