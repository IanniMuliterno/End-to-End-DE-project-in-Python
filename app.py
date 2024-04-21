from shiny import App, ui, render, reactive
import plotly.express as px
import pandas as pd
from datetime import datetime

# Load your CSV data into a DataFrame
df = pd.read_csv('data/flights_main.csv')
depart_tb = pd.read_csv('data/dim_dpt.csv')
arrival_tb = pd.read_csv('data/dim_arr.csv')
airline_tb = pd.read_csv('data/dim_airline.csv')

df2 = df.merge(depart_tb, left_on='dpt_id', right_on='id', how='left') \
        .merge(arrival_tb, left_on='arr_id', right_on='id', how='left') \
        .merge(airline_tb, left_on='airline_id', right_on='iata', how='left')

df2['duration'] = (pd.to_datetime(df2['actual_y']) - pd.to_datetime(df2['actual_x'])).dt.total_seconds() / 3600  # Duration in hours

# Define the UI layout
app_ui = ui.page_fluid(
    ui.layout_sidebar(
        # Sidebar panel for inputs
        ui.panel_sidebar(
            ui.input_text("airline_input", "Enter Airline Code"),
            ui.input_text("origin_input", "Enter Origin Airport Code"),
            ui.input_text("destination_input", "Enter Destination Airport Code"),
            ui.input_action_button("go_button", "Go!"),
            ui.download_button("download_button", "Download Filtered Data")
        ),
        
        # Main panel for outputs
        ui.panel_main(
            ui.output_text_verbatim("stats_output"),
            ui.output_ui("plot_output")
        )
    )
)

# Define the server logic
def server(input, output, session):
    # A reactive expression to filter the data based on user inputs
    @reactive.Calc
    def filtered_data():
        temp_df = df2
        if input.airline_input() != "":
            temp_df = temp_df[temp_df["name"] == input.airline_input()]
        if input.origin_input() != "":
            temp_df = temp_df[temp_df["iata_x"] == input.origin_input()]
        if input.destination_input() != "":
            temp_df = temp_df[temp_df["iata_y"] == input.destination_input()]
        return temp_df

    # Display statistics based on the filtered data
    @output
    @render.text
    def stats_output():
        temp_df = filtered_data()
        total_flights = len(temp_df)
        average_duration = temp_df['duration'].mean()
        flights_per_airline = temp_df['name'].value_counts().to_frame()
        return (f"Total Flights: {total_flights}\n"
                f"Average Flight Duration: {average_duration:.2f} hours\n"
                f"Flights Per Airline: \n{flights_per_airline}")

    # Create a Plotly figure based on the filtered data
    @output
    @render.ui
    def plot_output():
        temp_df = filtered_data()
        if not temp_df.empty:
            avg_duration = temp_df.groupby('name')['duration'].mean().reset_index()
            fig = px.bar(avg_duration, x='name', y='duration', title='Average Flight Duration by Airline')
            return ui.HTML(fig.to_html(full_html=False, include_plotlyjs='cdn'))
        else:
            return "No data to display"


# Create the app
app = App(app_ui, server)

# Run the app
if __name__ == "__main__":
    app.run(port=3003)
