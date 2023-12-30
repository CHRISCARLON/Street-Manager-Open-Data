import streamlit as st
from explore_street_manager_data import ExploreStreetManagerData, connect_to_motherduck
from explore_street_manager_sankey import prepare_sankey_data, prepare_completed_sankey_data
import plotly.graph_objects as go


def home_page():
    st.title(':mag_right: Welcome to the Street Manager Data Explorer Version 1.2')
    st.warning("""
    **Contains public sector information licensed under the Open Government Licence v3.0.**
    \n**Please note that The Street Manager Data Explorer is for educational purposes only and does not have the 
    endorsement, affiliation, support or approval of the Secretary of State for Transport.**
    \n**If you notice a bug or want to contribute please email me at <StreetManagerExplorer@gmail.com> or via GitHub**
    """)
    st.info("""
        **The tool currently runs using Street Manager Data from January 23 to November 23.**
        \n**Please note that Street Manager only covers :flag-england:**
        \n**Archived open data is released by the DfT monthly - data from December 2023 will be 
        available from 01/01/24.**
        """)
    st.subheader("What is the Purpose of this Tool?")
    st.markdown("""
    **1. This tool is designed to make Street Manager Data more accessible for relevant Policy & Programme Teams.** 
    \n**2. Its main aim is to provide an interactive, user-friendly way to become familiar with the basics of Street Manager.**
    """)
    st.subheader("High Level Roadmap:")
    st.markdown("""
    *Version 1*
        \n- Limited to permit data. 
        \n- Basic navigation bar.
        \n- Basic overview of Street Manager.
        \n- Simple tools to visualise and understand the permit lifecycle, completed works, 
        and collaborative street works. 
        \n- Simple folium maps available for basic geospatial analysis. 
    \n*Version 2*
        \n- Activity and section 58 data included. 
        \n- Improved navigation bar. 
        \n Improved Streamlit styling with improved fonts and colour palette. 
    \n*Version 3*
        \n- ChatGPT integration allowing users to interact with Street Manager data via prompts. 
        \n- Real time Street Manager data integration. 
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
    unique_months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
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
        st.info("**Please select filters to view the Sankey diagram!**")


def search_collaborative_street_works(data_manager_3):
    # Check if data is already loaded in the session state
    if 'df_collaborative_works' not in st.session_state:
        st.session_state['df_collaborative_works'] = data_manager_3.get_all_completed_works()

    # Filter for collaborative works
    df_collaborative = st.session_state['df_collaborative_works'][st.session_state['df_collaborative_works']['collaborative_working'] == 'Yes']

    # Display the overall total number of records as a subtitle
    total_records_overall = len(df_collaborative)
    st.write(f'**Total Collaborations: {total_records_overall}**')

    # Find the promoter with the most collaborations and count
    promoter_counts = df_collaborative['promoter_organisation'].value_counts()
    top_promoter, top_promoter_count = promoter_counts.idxmax(), promoter_counts.max()
    st.write(f'**The works promoter with the most collaborations is {top_promoter} with {top_promoter_count} collaborations**')

    # Find the highway authority with the most collaborations and count
    authority_counts = df_collaborative['highway_authority'].value_counts()
    top_authority, top_authority_count = authority_counts.idxmax(), authority_counts.max()
    st.write(f'**Most collaborations took place in {top_authority} with {top_authority_count} collaborations**')

    # Get unique values for filters
    unique_highway_authorities = df_collaborative['highway_authority'].unique()
    unique_promoter_organisations = df_collaborative['promoter_organisation'].unique()
    unique_months = df_collaborative['month'].unique()
    unique_years = df_collaborative['year'].unique()
    unique_activity_types = df_collaborative['activity_type'].unique()
    unique_work_categories = df_collaborative['work_category'].unique()
    unique_street_names = df_collaborative['street_name'].unique()

    # Sidebar filters
    selected_highway_authorities = st.sidebar.multiselect('Select Highway Authorities', unique_highway_authorities)
    selected_promoter_organisations = st.sidebar.multiselect('Select Promoter Organisations', unique_promoter_organisations)
    selected_months = st.sidebar.multiselect('Select Months', unique_months)
    selected_years = st.sidebar.multiselect('Select Years', unique_years)
    selected_activity_types = st.sidebar.multiselect('Select Activity Types', unique_activity_types)
    selected_work_categories = st.sidebar.multiselect('Select Work Categories', unique_work_categories)
    selected_street_names = st.sidebar.multiselect('Select Street Names', unique_street_names)

    # Check if the selected options are still valid
    if not all(auth in unique_highway_authorities for auth in selected_highway_authorities) or \
       not all(org in unique_promoter_organisations for org in selected_promoter_organisations) or \
       not all(month in unique_months for month in selected_months) or \
       not all(year in unique_years for year in selected_years) or \
       not all(activity in unique_activity_types for activity in selected_activity_types) or \
       not all(category in unique_work_categories for category in selected_work_categories) or \
       not all(street in unique_street_names for street in selected_street_names):
        st.session_state['df_collaborative_works'] = data_manager_3.get_all_completed_works()
        df_collaborative = st.session_state['df_collaborative_works'][st.session_state['df_collaborative_works']['collaborative_working'] == 'Yes']

    # Apply any filter
    filter_applied = any([
        selected_highway_authorities,
        selected_promoter_organisations,
        selected_months,
        selected_years,
        selected_activity_types,
        selected_work_categories,
        selected_street_names
    ])

    if filter_applied:
        # Apply filters conditionally
        if selected_highway_authorities:
            df_collaborative = df_collaborative[df_collaborative['highway_authority'].isin(selected_highway_authorities)]
        if selected_promoter_organisations:
            df_collaborative = df_collaborative[df_collaborative['promoter_organisation'].isin(selected_promoter_organisations)]
        if selected_months:
            df_collaborative = df_collaborative[df_collaborative['month'].isin(selected_months)]
        if selected_years:
            df_collaborative = df_collaborative[df_collaborative['year'].isin(selected_years)]
        if selected_activity_types:
            df_collaborative = df_collaborative[df_collaborative['activity_type'].isin(selected_activity_types)]
        if selected_work_categories:
            df_collaborative = df_collaborative[df_collaborative['work_category'].isin(selected_work_categories)]
        if selected_street_names:
            df_collaborative = df_collaborative[df_collaborative['street_name'].isin(selected_street_names)]

        # Reset the index and hide it in the displayed table
        df_display = df_collaborative.reset_index(drop=True)
        st.dataframe(df_display)
    else:
        st.info("**Please select at least one filter to view the data.**")


def main():
    st.set_page_config(layout="wide")

    # Sidebar header
    st.sidebar.header("**Navigation Bar**")
    page = st.sidebar.radio("**Please Select a Page**", [":house: Home",
                                                         "LHAs & Works Promoters",
                                                         "Permit Lifecycle",
                                                         "Completed Works",
                                                         "Completed Collaborative Street Works"])

    if page == ":house: Home":
        home_page()
    elif page == "LHAs & Works Promoters":
        high_lev_overview()
    elif page == "Permit Lifecycle":
        st.title("Understanding the permit life cycle")
        st.subheader('How do street work permit records relate to each other?')
        st.write('**Click the button below to load a random permit reference number showing all '
                 'attached permit records:**')

        # Define token
        my_token = st.secrets['key']

        # Initiate the connection
        get_quacky = connect_to_motherduck(my_token, "sm_permit")

        # Create an instance of ExploreStreetManagerData
        data_manager = ExploreStreetManagerData(get_quacky)

        # Call the function for exploring random data
        random_data_explore_page(data_manager)
    elif page == "Completed Works":
        st.title('Completed works')
        st.subheader('Use the filters to explore the activity of Statutory Undertakers in selected Highway Authorities'
                     ' across England - 2023 data only.')
        st.subheader("*A random Highway Authority has been chosen for you as an example.*")
        st.subheader("*Available Filters*:")
        st.markdown("""
        \n**Select Local Highway Authorities**: Legal bodies responsible for managing and maintaining the road network 
        within their designated boundary. 
        \n**Select Months**: Filter the data based on the month.
        \n**Select Activity Types**: For more information visit [DfT's Street Manager business rules](https://department-for-transport-streetmanager.github.io/street-manager-docs/articles/business-rules-version-2-00-works.html#2143-works-categories).
        \n**Select Work Category**: For more information visit [DfT's Street Manager business rules](https://department-for-transport-streetmanager.github.io/street-manager-docs/articles/business-rules-version-2-00-works.html#2143-works-categories). 
        """)
        # Define token
        my_token = st.secrets['key']

        # Initiate the connection
        get_quacky_2 = connect_to_motherduck(my_token, "sm_permit")

        # Create an instance of ExploreStreetManagerData
        data_manager_2 = ExploreStreetManagerData(get_quacky_2)

        # Call the function for exploring completed works data
        explore_completed_works_sankey_page(data_manager_2)
    elif page == ("Completed Collaborative Street Works"):
        st.title('Completed Collaborative Street works')

        # Define token and initiate connection
        my_token = st.secrets['key']
        get_quacky_3 = connect_to_motherduck(my_token, "sm_permit")

        # Create an instance of ExploreStreetManagerData
        data_manager_3 = ExploreStreetManagerData(get_quacky_3)

        # Call the function for searching collaborative street works
        search_collaborative_street_works(data_manager_3)


if __name__ == "__main__":
    main()
