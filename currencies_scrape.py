from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import date
import os

csv_file = "C:/Users/karel/exchange_rates/exchange_rates_czk.csv"


url = "https://www.cnb.cz/en/financial-markets/foreign-exchange-market/central-bank-exchange-rate-fixing/central-bank-exchange-rate-fixing/"
driver = webdriver.Edge()
driver.get(url)

# Handle cookie consent
decline_cookies_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#s-rall-bn"))
)
decline_cookies_button.click()

# Wait for the table to load
table = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#apollo-page > section > div:nth-child(2) > div > div > main > div > div > div.dynapps-exrates > div:nth-child(5) > table"))
)

# Extract table data
headers = table.find_elements(By.TAG_NAME, 'th')
column_names = [header.text.strip() for header in headers]

# Create an empty DataFrame with the extracted headers
df = pd.DataFrame(columns=column_names)

rows = table.find_elements(By.TAG_NAME, 'tr')
for row in rows[1:]:  # Skip the header row
    row_data = [cell.text.strip() for cell in row.find_elements(By.TAG_NAME, 'td')]
    df = pd.concat([df, pd.DataFrame([row_data], columns=column_names)], ignore_index=True)
df['date'] = date.today()
# Print or save the DataFrame
print(df)

# Close the driver
driver.quit()

if os.path.exists(csv_file):
    df.to_csv(csv_file, mode='a', index=False, header=False)  # Append without headers
    print(f"Appended data to {csv_file}")
else:
    df.to_csv(csv_file, index=False)  # Create a new file with headers
    print(f"Created new file {csv_file} and saved data")