pip install matplotlib

import streamlit as st
import sqlite3
import datetime
import os
import matplotlib.pyplot as plt
import pandas as pd

# Initialize the database connection
DB_PATH = 'Groceries.db'
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

# Recreate the table to ensure new table is created with updated values. Required after making changes to the table to reflect values.
#cursor.execute('DROP TABLE IF EXISTS groceries')

# Create the table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS groceries (
        id INTEGER PRIMARY KEY,
        product_name TEXT,
        unit_volume INTEGER,
        unit TEXT,
        price REAL,
        store_name TEXT,
        date_entered DATE
    )
''')
conn.commit()

# Function to insert data into the database
def insert_into_db(product_dict):
    cursor.execute('''
        INSERT INTO groceries (product_name, unit_volume, unit, price, store_name, date_entered)
        VALUES (:product_name, :unit_volume, :unit, :price, :store_name, :date_entered)
    ''', product_dict)
    conn.commit()

# Function to fetch unique product names from the database
def print_unique_product_names_from_db():
    cursor.execute("SELECT DISTINCT product_name FROM groceries")
    unique_names = cursor.fetchall()
    return [name[0] for name in unique_names]  # Return a list of names

# Streamlit UI
st.title('GroceryEasy: Track Your Recurring Groceries Easily')

# Display unique product names
unique_names = print_unique_product_names_from_db()
st.subheader("Previously bought (no duplicates):")
st.write(unique_names)

# Streamlit form for product data entry
with st.form(key='product_form'):
    st.write("Enter product details:")
    product_name = st.text_input("Product name", help="Enter the name of the product. E.g., apples")
    unit_volume = st.text_input("Unit volume", help="Enter the volume as a whole number. E.g., 2")
    unit = st.text_input("Unit", help="Enter the unit correctly abbreviated: kg, g, mg, l, ml or piece for whole items")
    price = st.number_input("Price", min_value=0.0, format="%.2f", help="Enter the price per unit. E.g., 1.99")
    store_name = st.text_input("Store name", help="Enter the name of the store. E.g., auchan, pingodoce")
    submit_button = st.form_submit_button(label='Add Product')

if submit_button:
    date_entered = datetime.datetime.now().strftime("%d:%m:%Y")
    product_dict = {
        "product_name": product_name,
        "unit_volume": unit_volume,
        "unit": unit,
        "price": price,
        "store_name": store_name,
        "date_entered": date_entered
    }

    # Insert the product data into the database
    insert_into_db(product_dict)
    st.success('Product Added Successfully!')

    # Update the list of unique product names
    unique_names = print_unique_product_names_from_db()
    st.subheader("Updated Unique Product Names:")
    st.write(unique_names)

#Matplot and pandas graphs
# Example: Creating a simple time series plot
df = pd.DataFrame({
    "Date": ["2021-01-01", "2021-01-02", "2021-01-03"],
    "Apples": [3, 2, None],
    "Bananas": [None, 3, 2]
})
df['Date'] = pd.to_datetime(df['Date'])
plt.figure(figsize=(10, 4))
plt.plot(df['Date'], df['Apples'], marker='o', label='Apples')
plt.plot(df['Date'], df['Bananas'], marker='o', label='Bananas')
plt.xlabel('Date')
plt.ylabel('Quantity Purchased')
plt.title('Product Purchases Over Time')
plt.legend()

# Display the plot in Streamlit
st.pyplot(plt)
