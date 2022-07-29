import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')


# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)
# Display the table on the page.

def get_fruity_choice(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized


try:
  streamlit.header("Fruityvice Fruit Advice!")
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error("please select a fruit to get inforamtion")
  else:
    back_from_function = get_fruity_choice(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()


streamlit.header("The fruit list contains:")
def get_fruit_load_list():
	streamlit.text("test2.1")
	my_cur = my_cnx.cursor()
	# with my_cnx.cursor() as my_cur:
	streamlit.text("test2.2")
	my_cur.execute("select * from fruit_load_list")
	# streamlit.text(my_cur.fetchall())
	return my_cur.fetchall()	
  
if streamlit.button('Get fruit load list'):
	streamlit.text("test1")
	my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
	streamlit.text('test2')
	my_data_row = get_fruit_load_list()
	
	streamlit.dataframe(my_data_row)

# streamlit.stop()
def insert_row_into_snowflake(new_fruit):
	with my_cnx.cursor() as my_cur:
		my_cur.execute("insert into fruit_load_list(fruit_name) values('"+ new_fruit + "')" )
		return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add to the list?')
if streamlit.button( 'add a fruit to the list'):
	my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
	back_from_function = insert_row_into_snowflake (add_my_fruit)
	streamlit.text(back_from_function)
# my_cur.execute("insert into fruit_load_list(fruit_name) values('"+ add_my_fruit + "')")
# my_cur.execute("delete from fruit_load_list where fruit_name='' or fruit_name IS NULL")
