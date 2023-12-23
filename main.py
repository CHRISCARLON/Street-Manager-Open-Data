import streamlit as st
from explore_street_manager_data import ExploreStreetManagerData, connect_to_motherduck
from explore_street_manager_sankey import prepare_sankey_data
import plotly.graph_objects as go


def random_data_explore(data_manager):
    if st.button('Generate Data'):
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


def home_page():
    st.title(':mag_right: Street Manager Data Explorer (Version 1.0)')
    st.subheader('An attempt to make Street Manager Data more accessible')
    st.subheader('Use the side bar to start exploring')
    st.write("Currently running from a MotherDuck database & using Street Manager data from 2023")
    st.write("check out MotherDuck here: [link](https://motherduck.com/#)")


def main():
    st.set_page_config(layout="wide")

    # Navigation
    page = st.sidebar.radio("Navigate", ["Home", "Explore Permit Records"])

    if page == "Home":
        home_page()
    elif page == "Explore Permit Records":
        st.title('How do street work permit records relate to each other?')
        st.subheader('Takes a random permit reference number and shows all attached records')

        # Define token
        my_token = st.secrets['key']

        # Initiate the connection
        get_quacky = connect_to_motherduck(my_token, "sm_permit")

        # Create an instance of ExploreStreetManagerData
        data_manager = ExploreStreetManagerData(get_quacky)

        # Call the function for exploring random data
        random_data_explore(data_manager)


if __name__ == "__main__":
    main()
