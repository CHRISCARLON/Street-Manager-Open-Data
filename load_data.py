import duckdb
import streamlit as st


# Quack quack

@st.cache_resource
def connect_to_motherduck(token, database):
    """
    Establishes a MotherDuck connection using a service token.
    """
    connection_string = f'md:{database}?motherduck_token={token}'
    quack = duckdb.connect(connection_string)
    return quack


# Class for creating database queries using SQL
class ExploreStreetManagerData:
    def __init__(self, quack):
        self.quack = quack

    def get_all_completed_works(self):
        """
        Fetch records for all completed works within a given month range.
        """
        query = """
        SELECT filename,
            activity_type,
            actual_end_date_time,
            actual_start_date_time,
            area_name,
            close_footway,
            close_footway_ref,
            collaboration_type,
            collaboration_type_ref,
            collaborative_working,
            current_traffic_management_type,
            current_traffic_management_type_ref,
            current_traffic_management_update_date,
            highway_authority,
            highway_authority_swa_code,
            is_covid_19_response,
            is_deemed,
            is_traffic_sensitive,
            is_ttro_required,
            permit_conditions,
            permit_reference_number,
            permit_status,
            promoter_organisation,
            promoter_swa_code,
            proposed_end_date,
            proposed_end_time,
            proposed_start_date,
            proposed_start_time,
            road_category,
            street_name,
            town,
            traffic_management_type,
            traffic_management_type_ref,
            usrn,
            work_category,
            work_category_ref,
            work_reference_number,
            work_status,
            work_status_ref,
            works_location_coordinates,
            works_location_type,
            year,
            month,
            event_type
        FROM permit_2023_final
        WHERE month BETWEEN 11 AND 12
        AND work_status_ref = 'completed'
        """
        result = self.quack.execute(query)
        return result.fetchdf()


@st.cache_data(show_spinner=True)
def get_cached_completed_works(_data_manager):
    return _data_manager.get_all_completed_works()
