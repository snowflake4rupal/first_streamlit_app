import streamlit

streamlit.title('My Mom\'s New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🐔 Hard-Boiled Free Range Egg')
streamlit.text('🥗 Kale, Spinach Smoothie')
streamlit.text('🥑🍞 Avocadeo Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')    
                                
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
                            
# Display the table on the page.
streamlit.dataframe(fruits_to_show)                

# New section to display fruityvise API response
streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?', 'Kiwi')
streamlit.write('The user entered', fruit_choice)

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# requests.get("https://fruityvice.com/api/fruit/kiwi")
# streamlit.text(fruityvice_response) #writes how many responses were received

# write your own comment -flattens the json file
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - puts the normalized data in a dataframe (table format) to make it easy to read
streamlit.dataframe(fruityvice_normalized)
import snowflake.connector
# cffi==1.15.0
# pyarrow==6.0.1

