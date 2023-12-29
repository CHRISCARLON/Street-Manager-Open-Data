import streamlit as st
from explore_street_manager_data import ExploreStreetManagerData, connect_to_motherduck
from explore_street_manager_sankey import prepare_sankey_data, prepare_completed_sankey_data
import plotly.graph_objects as go


def home_page():
    st.title(':mag_right: Welcome to the Street Manager Data Explorer Version 1.1')
    st.info("""
        **Currently using Street Manager Data from January 23 to October 23**
        \n**Please note that Street Manager only covers :flag-england:**
        \n**Data from November 23 & December 23 TBC!**""")
    st.subheader("What is the Purpose of this Tool?")
    st.markdown("""
        \n- This tool is designed to make Street Manager Data more accessible for relevant Policy & Programme Teams. 
        \n- The main aim is to provide an interactive, user-friendly way to become familiar with 
        the basics of Street Manager - to aid the creation of use cases for the data. 
    """)
    st.subheader("**Getting Started:**")
    st.markdown("""
        - Page :one:: Learn the basics of Street Manager data in 6 bullet points and a diagram.  
        - Page :two:: Visualise and understand the permit lifecycle.
        - Page :three:: Visualise and understand completed works across England.
    """)


def high_lev_overview():
    st.title("**TBC**")


def random_data_explore_page(data_manager):
    if st.button('Generate Random Permit Record'):
        # Display table with random work reference records
        table_data = data_manager.records_for_random_work_ref()
        st.table(table_data)

        # Generate and display Sankey diagram
        indices, sources, targets, values, labels = prepare_sankey_data(table_data)
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color='black', width=0.5),
                label=labels
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values
            ))])

        # Adjust the size of the Sankey diagram
        fig.update_layout(height=700, width=1200)

        # Display Sankey diagram
        st.plotly_chart(fig)


def explore_completed_works_sankey_page(data_manager_2):
    # Check if data is already loaded in the session state
    if 'df_completed_works' not in st.session_state:
        st.session_state['df_completed_works'] = data_manager_2.get_all_completed_works()

    # Get unique values for filters
    unique_highway_authorities = st.session_state['df_completed_works']['highway_authority'].unique()
    unique_months = [6, 7, 8, 9, 10]
    unique_activity_types = st.session_state['df_completed_works']['activity_type'].unique()
    unique_work_categories = st.session_state['df_completed_works']['work_category'].unique()

    # Sidebar filters
    selected_highway_authorities = st.sidebar.multiselect('Select Highway Authorities', unique_highway_authorities,
                                                          default=unique_highway_authorities[0])
    selected_months = st.sidebar.multiselect('Select Months', unique_months,
                                             default=unique_months)
    selected_activity_types = st.sidebar.multiselect('Select Activity Types', unique_activity_types,
                                                     default=unique_activity_types)
    selected_work_categories = st.sidebar.multiselect('Select Work Categories', unique_work_categories,
                                                      default=unique_work_categories)

    # Check if the selected authorities and other filters are in the current data
    if not all(auth in unique_highway_authorities for auth in selected_highway_authorities) or \
       not all(month in unique_months for month in selected_months) or \
       not all(activity in unique_activity_types for activity in selected_activity_types) or \
       not all(category in unique_work_categories for category in selected_work_categories):
        st.session_state['df_completed_works'] = data_manager_2.get_all_completed_works()

    # Display Sankey diagram based on the selected filters
    if selected_highway_authorities and selected_months and selected_activity_types and selected_work_categories:
        fig = prepare_completed_sankey_data(st.session_state['df_completed_works'], selected_highway_authorities,
                                            selected_months, selected_activity_types, selected_work_categories)
        st.plotly_chart(fig)
    else:
        st.write("Please select filters to view the Sankey diagram.")


def main():
    st.set_page_config(layout="wide")

    # Navigation
    page = st.sidebar.radio("**Navigation Bar**", [":house: Home", ":one: High Level Overview of Street Manager data",
                                                   ":two: Explore Permit Records",
                                                   ":three: Explore Completed Works"])

    if page == ":house: Home":
        home_page()
    elif page == ":one: High Level Overview of Street Manager data":
        high_lev_overview()
    elif page == ":two: Explore Permit Records":
        st.title("Understanding the permit life cycle")
        st.subheader('How do street work permit records relate to each other?')
        st.write('Click generate and load a random permit reference number showing all attached permit records:')

        # Define token
        my_token = st.secrets['key']

        # Initiate the connection
        get_quacky = connect_to_motherduck(my_token, "sm_permit")

        # Create an instance of ExploreStreetManagerData
        data_manager = ExploreStreetManagerData(get_quacky)

        # Call the function for exploring random data
        random_data_explore_page(data_manager)
    elif page == ":three: Explore Completed Works":
        st.title('Explore Completed works')
        st.subheader('Use the filters to analyse the activity of Statutory Undertakers in selected Highway Authorities'
                     ' across England - 2023 only!')
        st.subheader("")
        st.markdown("""
        \n**Select Local Highway Authorities**: Legal bodies responsible for managing and maintaining the road network 
        within their designated boundary. 
        \n**Select Months**: Filter the data based on the month (1 = January, 2 = February, etc)
        \n**Select Activity Types**: Description TBC
        \n**Select Work Category**: Description TBC
        """)
        # Define token
        my_token = st.secrets['key']

        # Initiate the connection
        get_quacky_2 = connect_to_motherduck(my_token, "sm_permit")

        # Create an instance of ExploreStreetManagerData
        data_manager_2 = ExploreStreetManagerData(get_quacky_2)

        # Call the function for exploring completed works data
        explore_completed_works_sankey_page(data_manager_2)


if __name__ == "__main__":
    main()
