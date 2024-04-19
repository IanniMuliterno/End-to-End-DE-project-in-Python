from shiny import App, ui, render, reactive
import plotly.express as px
import pandas as pd

# Load your CSV data into a DataFrame
df = pd.read_csv('data/flights_main.csv')

# Define the UI layout
app_ui = ui.page_fluid(
    ui.layout_sidebar(
        # Sidebar panel for inputs
        ui.panel_sidebar(
            ui.input_text("airline_input", "Enter Airline Code"),
            ui.input_text("origin_input", "Enter Origin Airport Code"),
            ui.input_text("destination_input", "Enter Destination Airport Code"),
            ui.input_action_button("go_button", "Go!")
        ),
        
        # Main panel for outputs
        ui.panel_main(
            ui.output_text_verbatim("stats_output"),
            ui.output_plot("plot_output")
        )
    )
)

# Define the server logic
def server(input, output, session):
    # A reactive expression to filter the data based on user inputs
    @reactive.Calc
    def filtered_data():
        temp_df = df
        if input.airline_input() != "":
            temp_df = temp_df[temp_df["airline"] == input.airline_input()]
        if input.origin_input() != "":
            temp_df = temp_df[temp_df["origin"] == input.origin_input()]
        if input.destination_input() != "":
            temp_df = temp_df[temp_df["destination"] == input.destination_input()]
        return temp_df

    # Display statistics based on the filtered data
    @output
    @render.text
    def stats_output():
        temp_df = filtered_data()
        total_flights = len(temp_df)
        average_duration = temp_df['duration'].mean()
        flights_per_airline = temp_df['airline'].value_counts().to_frame()
        return (f"Total Flights: {total_flights}\n"
                f"Average Flight Duration: {average_duration}\n"
                f"Flights Per Airline: \n{flights_per_airline}")

    # Create a Plotly figure based on the filtered data
    @output
    @render.plotly
    def plot_output():
        temp_df = filtered_data()
        fig = px.bar(temp_df, x='airline', y='duration', title='Average Flight Duration by Airline')
        return fig

# Create the app
app = App(app_ui, server)

# Run the app
if __name__ == "__main__":
    app.run()
