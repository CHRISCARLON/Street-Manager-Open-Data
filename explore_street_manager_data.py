import duckdb


# Quack quack


def connect_to_motherduck(token, database):
    """
    Establishes a MotherDuck connection using a service token.

    Parameters:
    token (str): The service token for MotherDuck connection.

    Returns:
    The connection object to the MotherDuck database.
    """
    connection_string = f'md:{database}?motherduck_token={token}'
    quack = duckdb.connect(connection_string)
    return quack


# Class for creating database queries using SQL
class ExploreStreetManagerData:
    def __init__(self, quack):
        self.quack = quack

    def records_for_random_work_ref(self):
        """
        Fetch records for a randomly selected permit reference number from the database.

        Returns:
        DataFrame: A DataFrame containing the records for a random permit reference number.
        """
        query = """
            SELECT filename, promoter_organisation, highway_authority, 
                   event_type, permit_status, p.permit_reference_number, 
                   work_reference_number, activity_type, work_category, 
                   work_status_ref, current_traffic_management_type, is_traffic_sensitive, 
                   promoter_swa_code, highway_authority_swa_code, year, month
            FROM new_table p
            INNER JOIN (
                SELECT permit_reference_number 
                FROM permit_2023 
                ORDER BY RANDOM() 
                LIMIT 1
            ) AS random_ref
            ON p.permit_reference_number = random_ref.permit_reference_number
            ORDER BY filename
        """
        result = self.quack.sql(query)
        return result.df()

    def get_all_completed_works(self):
        """
        Fetch records for all completed works within a given month range.

        Returns:
        DataFrame: A DataFrame containing the completed works data.
        """
        query = """
        SELECT promoter_organisation, highway_authority, month, year, activity_type, work_category
        FROM new_table
        WHERE work_status_ref = 'completed'
        AND month IN (6, 7, 8, 9, 10, 11);
        """
        result = self.quack.execute(query)
        return result.fetchdf()
