import requests
from bs4 import BeautifulSoup as Soup
import pandas as pd
from pandas import DataFrame
import seaborn as sns
import matplotlib.pyplot as plt


def parse_table_to_dataframe(url):
    # Fetch and parse the HTML document
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch URL. Status code: {response.status_code}")

    html_soup = Soup(response.text, 'html.parser')
    tables = html_soup.find_all('table')

    if not tables:
        raise ValueError("No tables found in the document.")

    # Assuming the secret message is in the first table
    rows = tables[0].find_all('tr')
    if len(rows) < 2:
        raise ValueError("Table does not contain enough rows for data.")

    # Parse header and data rows
    header = [cell.get_text(strip=True) for cell in rows[0].find_all('td')]
    data = [[cell.get_text(strip=True) for cell in row.find_all('td')] for row in rows[1:]]

    # Create DataFrame
    df = DataFrame(data, columns=header)

    # Ensure numeric conversion of coordinates
    int_cols = ['x-coordinate', 'y-coordinate']
    df[int_cols] = df[int_cols].apply(pd.to_numeric)
    return df


def plot_secret_message(df):
    # Plot the scatter plot
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='x-coordinate', y='y-coordinate', hue='Character', style='Character')
    plt.xticks([])
    plt.yticks([])
    plt.xlabel('')
    plt.ylabel('')
    plt.title("Secret Message", fontsize=16)
    plt.legend(title='Character', loc='upper right')
    plt.show()


def get_secret_message(url):
    # Parse the table and plot the message
    df = parse_table_to_dataframe(url)
    plot_secret_message(df)


# Usage example
get_secret_message(
    'https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub')
