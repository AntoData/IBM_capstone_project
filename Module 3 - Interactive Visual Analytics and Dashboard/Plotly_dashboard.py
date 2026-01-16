# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_sites = [{'label': x, 'value': x} for x in
                spacex_df['Launch Site'].unique()]
launch_sites.append({'label': 'All Sites', 'value': 'ALL'})
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center',
                                               'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                #
                                dcc.Dropdown(id='site-dropdown',
                                             options=[x for x in launch_sites],
                                             value='ALL',
                                             placeholder=
                                             "Select a Launch Site here",
                                             searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0, max=10000, step=50,
                                    marks={
                                        0: '0',
                                        2500: '2500',
                                        5000: '5000',
                                        7500: '7500',
                                        10000: '10000'
                                    },
                                    value=[min_payload, max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(
                                    id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@dash.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value"),
)
def success_pie_chart(launch_site_value):
    df_site = spacex_df
    if launch_site_value != 'ALL':
        df_site = df_site[df_site['Launch Site'] == launch_site_value]
        df_site_class = df_site.groupby(["class"])["class"].count().rename("Ratio")
        df_site_class = df_site_class.to_frame()
        df_site_class.reset_index(inplace=True)
        print(df_site_class)
        pie_chart = \
            px.pie(df_site_class, names="class", values="Ratio")
        return pie_chart
    else:
        df_site_class = (
            df_site[df_site["class"] == 1]
            .groupby("Launch Site")["class"]
            .sum()
            .rename("successful_launches")
        )
        df_site_class = df_site_class.to_frame()
        df_site_class.reset_index(inplace=True)
        print(df_site_class)
        pie_chart = \
            px.pie(df_site_class, names="Launch Site", values="successful_launches")
        return pie_chart
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@dash.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value"),
    Input(component_id="payload-slider", component_property="value")
)
def get_graph(launch_site_value, payload_range):
    df_site = spacex_df
    df_site = df_site[df_site["Payload Mass (kg)"] <= payload_range[1]]
    df_site = df_site[df_site["Payload Mass (kg)"] >= payload_range[0]]
    print(payload_range)
    if launch_site_value != 'ALL':
        df_site = df_site[df_site['Launch Site'] == launch_site_value]
        df_site_class = df_site.groupby(["class"])["class"].count().rename("Ratio")
        df_site_class = df_site_class.to_frame()
        df_site_class.reset_index(inplace=True)
        print(df_site_class)
        scatter_plot = px.scatter(df_site, x="Payload Mass (kg)", y="class",
                                  color="Booster Version Category")
        return scatter_plot
    else:
        scatter_plot = px.scatter(df_site, x="Payload Mass (kg)", y="class",
                                  color="Booster Version Category")
        return scatter_plot

# Run the app
if __name__ == '__main__':
    app.run()
