import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach, & Rocket Smoothie')
streamlit.text('🐔 Hard-BOiled Free Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
try:
fruit_choice = streamlit.text_input('What fruit would you like information about?')
if not fruit_choice:
streamlit.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)

# write your own comment -what does the next line do? 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
streamlit.dataframe(fruityvice_normalized)


def get_fruityvicedata(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  # take the json version of the response and normalise it
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
# End of function definition

# New section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error('Please select a fruit to get info.')
  else:
    back_from_function = get_fruityvicedata(fruit_choice)
    # output it to the screen as a table
    streamlit.dataframe(back_from_function)

except URLError as e:
      streamlit.error()  
    
# end of second section
# exit script here
#streamlit.stop()

streamlit.header("View Our List - Add Your Favourites!")

# snowflake-related function (with no parameters) ...
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()
# End of function definition

# add a button to load the fruit ...
if streamlit.button('Get Fruit List'):
  # import snowflake connector
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  #grab the fruit load list using the snowflake-related function
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  # display the list in a frame
  streamlit.dataframe(my_data_rows)

 # end of third section
# exit script here
# streamlit.stop() 
  
# Allow the end user to add a fruit to the list

# Define another function
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("INSERT into fruit_load_list values ('" + add_my_fruit +"')")
    return 'Thanks for adding '+ new_fruit
# End of function

# exit script here
# streamlit.stop()

add_my_fruit = streamlit.text_input('Any fruit you would like to add?') #invite user to fill in a text box with a fruit
if streamlit.button('Add a fruit to the list'): # Define a button then determine what to do when it is pressed
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"]) #invoke the same snowflake connection
  back_from_function = insert_row_snowflake(add_my_fruit) 
  my_cnx.close()
  streamlit.text(back_from_function)
  
# exit script here
streamlit.stop()

# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")

my_cur.execute("SELECT * from fruit_load_list")

my_data_row = my_cur.fetchall()

# streamlit.text("Hello from Snowflake:")

streamlit.text("The fruit load list contains:")

streamlit.dataframe(my_data_row)



# Let's put another pick list here so they can pick the fruit they want to add to the list 
add_my_fruit = streamlit.multiselect("Any fruit you would like to add?:", list(my_fruit_list.index))

streamlit.write('Thanks for adding ', add_my_fruit)

