""" Code as at the end of week 7 activities """
# Note to self: Run the Flask REST app first, then run this Dash app
import pandas as pd
import requests
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from figures import line_chart, bar_gender, scatter_geo, event_data, create_card, create_card_from_df, app

# Create the Plotly Express line chart object, e.g. to show number of sports
line = line_chart("sports")

# Create the Plotly Express stacked bar chart object to show gender split of participants for the type of event
bar = bar_gender("winter")

# Create the scatter map
map = scatter_geo()


# Layout variables

@app.callback(
    Output(component_id='line', component_property='figure'),
    Input(component_id='type-dropdown', component_property='value')
)
def update_line_chart(chart_type):
    figure = line_chart(chart_type)
    return figure

@app.callback(
    Output('card', 'children'),
    Input('map', 'hoverData'),
)
def display_card(hover_data):
    if hover_data is not None:
        event_id = hover_data['points'][0]['customdata'][0]
        if event_id is not None:
            return create_card(event_id)


# This version requires the Flask REST app to be running
# card = create_card(12)

# This version does not require the Flask REST app to be running
#card = create_card_from_df(12)

dropdown = dbc.Select(
    id="type-dropdown",
    options=[
        {"label": "Events", "value": "events"},
        {"label": "Sports", "value": "sports"},
        {"label": "Countries", "value": "countries"},
        {"label": "Athletes", "value": "participants"},
    ],
    value="events"
)

checklist = dbc.Checklist(
    options=[
        {"label": "Summer", "value": "summer"},
        {"label": "Winter", "value": "winter"},
    ],
    value=["summer"],
    id="checklist-input",
    inline=True,
)

row_one = html.Div(
    dbc.Row([
        dbc.Col([html.H1("Paralympics Dashboard"), html.P(
            "Use the charts to help you answer the questions.")
                 ], width=12),
    ]),
)

row_two = dbc.Row([
    dbc.Col(children=[
        dropdown
    ], width=2),
    dbc.Col(children=[
        checklist,
    ], width={"size": 2, "offset": 4}),
], align="start")

row_three = dbc.Row([
    dbc.Col(children=[
        dcc.Graph(id="line", figure=line),
    ], width=6),
    dbc.Col(children=[
        dcc.Graph(id="bar", figure=bar),
        # html.Img(src=app.get_asset_url('bar-chart-placeholder.png'), className="img-fluid"),
    ], width=6),
], align="start")

row_four = dbc.Row([
    dbc.Col(children=[
        dcc.Graph(id="map", figure=map)
        # html.Img(src=app.get_asset_url('map-placeholder.png'), className="img-fluid"),
    ], width=8, align="start"),
    dbc.Col(children=[
        html.Br(),
        html.Div(id="card"),
    ], width=4, align="start"),
])

app.layout = dbc.Container([
    row_one,
    row_two,
    row_three,
    row_four,
])

if __name__ == '__main__':
    app.run(debug=True, port=8050)
    # Runs on port 8050 by default, this just shows the parameter to use to change to another port if needed
