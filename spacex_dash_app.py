# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options = [{'label' : 'All Sites',
                                                                            'value' : 'ALL'},
                                                                            {'label': 'Cape Canaveral Launch Complex 40 (CAFS LC-40)',
                                                                            'value': 'CCAFS LC-40'},
                                                                            {'label': 'Cape Canaveral Space Launch Complex 40 (CCAFS SLC-40)',
                                                                            'value': 'CCAFS SLC-40'},
                                                                            {'label': 'Kennedy Space Center Launch Complex 39A (KSC LC-39A)',
                                                                            'value': 'KSC LC-39A'},
                                                                            {'label': 'Vandenberg Air Force Base Space Launch Complex (VAFB SLC-4E)',
                                                                            'value': 'VAFB SLC-4E'}], 
                                                                value = 'ALL',            
                                                                placeholder = "Select a Launch Site here",
                                                                searchable = True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min = 0, max = 10000, 
                                                step = 1000, value = [min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(    
    Output(component_id = 'success-pie-chart',
    component_property = 'figure'),
    
    Input(component_id = 'site-dropdown', 
    component_property = 'value')
            )

def get_pie_chart(entered_launch_site):
    filtered_df = spacex_df.groupby(['Launch Site'], as_index=False)
    if entered_launch_site == 'ALL':
        fig = px.pie(filtered_df, values = 'class', names = 'Launch Site',
        title = 'Total of sucessful launches by site')
        return fig
    
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_launch_site]
        
        for i in filtered_df['class']:
            if i == 1:
                filtered_df['outcome'] = 'Success'
            else:
                filtered_df['outcome'] = 'Failure'    
        
        filtered_df['counts'] = 1
        fig = px.pie(filtered_df, values='counts', names='outcome', 
        title='Total of sucessful launches for the site:' + entered_launch_site)
        return fig



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id = 'sucess-payload-scatter-chart',
        component_property = 'figure'),
    
    [Input(component_id = 'site-dropdown',
        component_property = 'value'),
    Input(component_id = 'payload-slider',
        component_property = 'value')]
            )

def get_scatter_plot(entered_launch_site, slider_val):
    
    filtered_df = spacex_df[(slider_val[0] <= spacex_df["Payload Mass (kg)"] <= slider_val[1])]

    if entered_launch_site == 'ALL':
        fig = px.scatter(filtered_df, x = 'Payload Mass (kg)', y = 'Class', title = 'Sucessful launches by site',
        color='Booster Version Category')
        return fig

    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_launch_site]
        
        for i in filtered_df['class']:
            if i == 1:
                filtered_df['outcome'] = 'Success'
            else:
                filtered_df['outcome'] = 'Failure'    
        
        filtered_df['counts'] = 1
        fig = px.scatter(filtered_df, x = 'Payload Mass (kg)', y = 'Class', title = 'Sucessful launches for'+ entered_launch_site,
        color='Booster Version Category')
        return fig



# Run the app
if __name__ == '__main__':
    app.run_server()
