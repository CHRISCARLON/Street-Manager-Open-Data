import streamlit as st
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from load_data import ExploreStreetManagerData, connect_to_motherduck, get_cached_completed_works


def home_page():
    st.title(':mag_right: Welcome to the Street Manager Data Explorer')
    st.write('*This is a work in progress and will be subject to continuous improvements.*')
    st.warning("""
    **Contains public sector information licensed under the Open Government Licence v3.0.**
    \n**Please note that The Street Manager Data Explorer is for educational purposes only and does not have the 
    endorsement, affiliation, support or approval of the Secretary of State for Transport.**
    \n**If you notice a bug or want to contribute please email me at <StreetManagerExplorer@gmail.com> or via GitHub.**
    """)
    st.markdown("""
    #### Upcoming Features:
    \n:one: Keep a temporary log of the chat history and improve the conversational flow. 
    \n:two: Allow for basic data visualisation based on text prompts. 
    \n:three: Section 58 and activity data TBC.
    """)


def street_chatter(data_manager):
    st.title("**Chat with Street Manager Data**")
    st.write("*This tool provides an easy and accessible way for relevant policy and programme teams to become familiar"
             " with Street Manager data without all the hassle.*")
    st.warning("""
    **Currently running using gpt-3.5 and Street Manager Data from December 23.**
    \n**Due to Streamlit memory constraints this only contains completed works.**
    \n**The current functionality is quite basic for now with only basic prompts accepted - 
    as a result prompts need to be short and concise.**
    \n**This will improve in the future.**
    """)
    st.info("""
    **Prompt Cheatsheet:**
    \nHow many data fields are there?
    \nList me all the columns and put this in a table.
    \nName me the top 5 works promoters.
    \nName me the top 5 highway authorities.
    \nName me the top street and its usrn.
    \nWhat are the unique values for activity type?
    \nIn activity type, how many section 50s were there?
    \nIn activity type, how many section 50s were there and what was the top works promoter for section 50s?
    \nIn London how many entries are there?
    \nIn London can you list the total entries for each highway authority in table?
    \nIn London how many entries are there? Also, using work category how many major entries are there for London?
    \nIn London, using work category can you list the total major entries for each highway authority?
    """)
    df = get_cached_completed_works(data_manager)

    query = st.text_area("*Please type your message here:*")

    answer = None

    if query:
        try:
            llm = OpenAI(api_token=st.secrets["gpt"])
            query_engine = SmartDataframe(df, config={"llm": llm})
            answer = query_engine.chat(query)

            st.dataframe(answer)
        except Exception as e:
            if answer is not None:
                st.write(answer)
            else:
                st.write("An error occurred: ", str(e))


def main():
    st.set_page_config(layout="wide")

    my_token = st.secrets['key']
    data_manager = ExploreStreetManagerData(connect_to_motherduck(my_token, "sm_permit"))

    st.sidebar.header("**Navigation Bar**")
    page = st.sidebar.radio("**Please Select a Page**", [":house:**Home**", ":speaking_head_in_silhouette:"
                                                                            "**Talk to Street Manager**"])

    if page == ":house:**Home**":
        home_page()
    elif page == ":speaking_head_in_silhouette:**Talk to Street Manager**":
        street_chatter(data_manager)


if __name__ == "__main__":
    main()
