import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Mom\'s New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🐔 Hard-Boiled Free Range Egg')
streamlit.text('🥗 Kale, Spinach Smoothie')
streamlit.text('🥑🍞 Avocadeo Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')    
                                
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
                            
# Display the table on the page.
streamlit.dataframe(fruits_to_show)                

# create the repeatable code block(function)
def get_fruitvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

# New section to display fruityvise API response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?', 'Kiwi')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_fuction = get_fruitvice_data(fruit_choice)
    streamlit.dataframe(back_from_fuction)
#     streamlit.write('The user entered', fruit_choice)
except URLError as e:
  streamlit.error()
  
# import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# requests.get("https://fruityvice.com/api/fruit/kiwi")
# streamlit.text(fruityvice_response) #writes how many responses were received

streamlit.header("The fruit load list contains:")
# Snowflake related function
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
       my_cur.execute("select * from fruit_load_list")
       return my_cur.fetchall()
    
# Add a button to load the fruit
# streamlit.dataframe(my_data_rows)
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

# Allow end user to add a fruit
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
       my_cur.execute("insert into fruit_load_list values('" + new_fruit + "')")
       return "Thanks for adding " + new_fruit
    
add_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_function = insert_row_snowflake(add_my_fruit)
   streamlit.text(back_from_function)
    
streamlit.stop()    
streamlit.write('Thanks for adding', add_fruit)
# This will not work correctly but just go with it for now
my_cur.execute("insert into fruit_load_list values('from stremlit')")
# import snowflake.connector 
# streamlit.stop()
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")#("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)


