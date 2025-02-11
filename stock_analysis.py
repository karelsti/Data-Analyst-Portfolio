# Import necessary libraries
from tkinter import filedialog
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
from sklearn.preprocessing import StandardScaler

# Opening files using a file dialog
filename_voe = filedialog.askopenfilename(title='Select Voestalpine stock data file')
voest = pd.read_csv(filename_voe)
print("Voestalpine data loaded:")
print(voest.head())

filename_tes = filedialog.askopenfilename(title='Select Tesla stock data file')
tesla = pd.read_csv(filename_tes)
print("Tesla data loaded:")
print(tesla.head())

# Convert 'Date' column to datetime format
voest['Date'] = pd.to_datetime(voest['Date'])
tesla['Date'] = pd.to_datetime(tesla['Date'])

# Merging the two datasets on 'Date'
stock = pd.merge(voest, tesla, on='Date', how='inner')

# Renaming columns for clarity
stock.rename(columns={
    'Open_x': 'Voest_Open', 'High_x': 'Voest_High', 'Low_x': 'Voest_Low', 'Close_x': 'Voest_Close', 
    'Adj Close_x': 'Voest_Adj_Close', 'Volume_x': 'Voest_Volume',
    'Open_y': 'Tesla_Open', 'High_y': 'Tesla_High', 'Low_y': 'Tesla_Low', 'Close_y': 'Tesla_Close', 
    'Adj Close_y': 'Tesla_Adj_Close', 'Volume_y': 'Tesla_Volume'
}, inplace=True)

# Basic information about the merged dataset
print("Merged dataset info:")
stock.info()

# Exploratory Data Analysis (EDA)
print("Statistical Summary of Closing Prices:")
print(stock[['Voest_Close', 'Tesla_Close']].describe())

# KDE plots for closing prices
plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
sns.kdeplot(stock['Voest_Close'], color='blue', fill=True)
plt.title('Voestalpine Closing Prices Distribution')

plt.subplot(1, 2, 2)
sns.kdeplot(stock['Tesla_Close'], color='red', fill=True)
plt.title('Tesla Closing Prices Distribution')
plt.tight_layout()
plt.show()

# Convert 'Date' to Month-Year format for easier plotting
stock['Month_Year'] = stock['Date'].dt.to_period('M').astype(str)

# Time series plot of raw closing prices
plt.figure(figsize=(14, 7))
plt.plot(stock['Date'], stock['Voest_Close'], label='Voestalpine', color='blue')
plt.plot(stock['Date'], stock['Tesla_Close'], label='Tesla', color='red')

# Formatting the x-axis to show Year-Month with fewer ticks
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.xticks(rotation=45)

plt.xlabel('Date (Month-Year)')
plt.ylabel('Closing Price')
plt.title('Voestalpine vs. Tesla Closing Prices Over Time')
plt.legend()
plt.tight_layout()
plt.show()


# Standardizing the closing prices
scaler = StandardScaler()
stock[['Voest_Close', 'Tesla_Close']] = scaler.fit_transform(stock[['Voest_Close', 'Tesla_Close']])
print("Standardized Closing Prices:")
print(stock[['Date', 'Voest_Close', 'Tesla_Close']].head())

# Time series plot of standardized closing prices
plt.figure(figsize=(14, 7))
plt.plot(stock['Date'], stock['Voest_Close'], label='Voestalpine', color='blue')
plt.plot(stock['Date'], stock['Tesla_Close'], label='Tesla', color='red')

# Formatting the x-axis to show Year-Month with fewer ticks
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.xticks(rotation=45)

plt.xlabel('Date (Month-Year)')
plt.ylabel('Standardized Closing Price')
plt.title('Voestalpine vs. Tesla Standardized Closing Prices Over Time')
plt.legend()
plt.tight_layout()
plt.show()
