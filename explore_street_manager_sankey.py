import plotly.graph_objects as go


def prepare_sankey_data(data):
    """
    Create a sankey diagram using the returned record from the randomly selected permit reference number.

    Parameters:
    DataFrame: Dataframe containing the permit data

    Returns:
    Variables required to create the sankey: Indices, sources, targets, etc.
    These will be used in the random data explore page function in main.py
    """
    # Create a unique identifier for each event occurrence
    data['event_id'] = data['event_type'] + '_' + data['filename']

    # Initialise lists for sources, targets, and values
    sources, targets, values = [], [], []
    unique_events = data['event_id'].unique()
    indices = {event: i for i, event in enumerate(unique_events)}

    # Determine the starting event
    for permit_ref in data['permit_reference_number'].unique():
        permit_data = data[data['permit_reference_number'] == permit_ref]

        # If 'permit_submitted_event' is present, use it as starting point
        if 'permit_submitted_event' in permit_data['event_type'].values:
            starting_event_id = permit_data[permit_data['event_type'] == 'permit_submitted_event']['event_id'].iloc[0]
        elif 'in_progress' in permit_data['work_status_ref'].values:
            # Fallback: Use 'in_progress' as starting point
            starting_event_id = permit_data[permit_data['work_status_ref'] == 'in_progress']['event_id'].iloc[0]
        else:
            # If neither 'permit_submitted_event' nor 'in_progress' are available, skip this permit
            continue

        starting_index = indices[starting_event_id]

        for _, event_row in permit_data.iterrows():
            if event_row['event_id'] != starting_event_id:
                event_index = indices[event_row['event_id']]
                sources.append(starting_index)
                targets.append(event_index)
                values.append(1)

    # Update labels so they are readable
    labels = ['_'.join(event.split('_')[0:4]) for event in unique_events]

    return indices, sources, targets, values, labels


def prepare_completed_sankey_data(df_completed_works, selected_highway_authorities, selected_months,
                                  selected_activity_types, selected_work_categories,
                                  figure_height=1500, figure_width=1500):

    """
    Create an interactive sankey diagram using the returned completed works records.

    Parameters:
    DataFrame: Dataframe containing the permit data

    Returns:
    Plotly figure required to show the sankey.
    This will be used in the explore completed works sankey page function in main.py
    """

    # Apply additional filters
    df_filtered = df_completed_works[
        (df_completed_works['highway_authority'].isin(selected_highway_authorities)) &
        (df_completed_works['month'].isin(selected_months)) &
        (df_completed_works['activity_type'].isin(selected_activity_types)) &
        (df_completed_works['work_category'].isin(selected_work_categories))
    ]

    # Create labels for nodes
    df_filtered['promoter_label'] = df_filtered['promoter_organisation'] + ' (Works Promoter)'
    df_filtered['authority_label'] = df_filtered['highway_authority'] + ' (Highway Authority)'

    # Aggregate and count the occurrences
    df_grouped = df_filtered.groupby(['promoter_label', 'authority_label']).size().reset_index(name='completed_works')

    # Nodes
    promoters = set(df_grouped['promoter_label'])
    authorities = set(df_grouped['authority_label'])
    nodes = list(promoters | authorities)
    node_dict = {node: i for i, node in enumerate(nodes)}
    node_colors = ['blue' if '(Works Promoter)' in node else 'green' for node in nodes]

    # Links
    links = [{
        'source': node_dict[link['promoter_label']],
        'target': node_dict[link['authority_label']],
        'value': link['completed_works']
    } for link in df_grouped.to_dict('records')]

    # Creating the Sankey diagram
    fig = go.Figure(data=[go.Sankey(node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5), label=nodes, color=node_colors), link=dict(source=[link['source'] for link in links], target=[link['target'] for link in links], value=[link['value'] for link in links]))])
    fig.update_layout(font_size=12, height=figure_height, width=figure_width)
    return fig
