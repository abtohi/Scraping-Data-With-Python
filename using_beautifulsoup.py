import requests
from bs4 import BeautifulSoup
import pandas as pd

#Download and parse the HTML
start_url = "https://en.wikipedia.org/wiki/Tesla,_Inc."

#Download the HTML from start_url
downloaded_html = requests.get(start_url)

#Parse the HTML with BeautifulSoup and create a soup object
soup = BeautifulSoup(downloaded_html.text)

#Save a local copy
with open('downloaded.html','w', encoding='utf-8') as file:
    file.write(soup.prettify())
    
#Select table wikitable
full_table = soup.select('table.wikitable tbody')[0]
print(full_table)

#Extract the table column heading
# End result : A list with all the column headings

table_head = full_table.select('tr th')
print('-------------')

import re #regex, tujuan disini mau menghilangkan [b] [c] pada heading column
regex = re.compile('_\[\w\]')

table_columns = []
for element in table_head:
    column_label = element.get_text(separator=" ", strip=True)
    column_label = column_label.replace(' ', '_')
    column_label = regex.sub('', column_label) #dibuat blank setelah sub karena agar mereplace setiap elemen yg cocok
    table_columns.append(column_label)
    print(column_label) #tidak perlu di print tidak apa apa

print('-------------')
print(table_columns)

# Extract the table rata (rows)
# End Result : A multi-dimensional list containing a list for each row

table_rows = full_table.select('tr')

print('------------')

table_data = []
for index, element in enumerate(table_rows):
    if index > 0 :
        row_list = []
        values = element.select('td')
        for value in values :
            row_list.append(value.text.strip()) #strip digunakan untuk menghilangkan \n pada data
        table_data.append(row_list)

print(table_data)

# Create a pandas dataframe
df = pd.DataFrame(table_data, columns=table_columns)
df.to_excel('Scraping Data Wikipedia.xlsx', sheet_name='Tesla', index=False)

