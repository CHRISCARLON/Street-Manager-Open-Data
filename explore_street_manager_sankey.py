def prepare_sankey_data(data):
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
