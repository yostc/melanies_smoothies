# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")


name_on_order = st.text_input("Name On Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)


cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop

# Convert the Snowpark Dataframe to a Pandas Datafram so we can use the LOC function
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop

ingredients_list = st.multiselect('Choose up to 5 ingredients:' 
                                  ,my_dataframe
                                  ,max_selections=5
                                 )

if ingredients_list:
    ingredients_string = ' '
    for fruit_chosen in ingredients_list:
         ingredients_string += fruit_chosen + ' '

         search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
         st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

         smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" +fruit_chosen )    
         st_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)     

    #st.write(ingredients_string)

 
    my_insert_stmt = """ insert into smoothies.public.orders(INGREDIENTS,NAME_ON_ORDER)
            values ('""" + ingredients_string + """' , '""" + name_on_order + """' )"""

    #st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
       session.sql(my_insert_stmt).collect()        

       st.success('Your smoothie is ordered! '+ name_on_order, icon="✅")




