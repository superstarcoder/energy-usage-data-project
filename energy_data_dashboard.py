import gradio as gr
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import preprocess_weather_data


""" PLEASE MODIFY THE FOLLOWING PATH:"""
energy_data_folder_path = "input_data"


file_names = os.listdir(energy_data_folder_path)
file_names = [f for f in file_names if os.path.isfile(os.path.join(energy_data_folder_path, f))]
default_i = 1 if len(file_names) > 1 else 0
weather_data_file_path = 'weather_data/full_weather_data_2023.csv'
weather_df = preprocess_weather_data.get_weather_df(weather_data_file_path)


def generate_interactive_plot(fileName, dataFrequency, showWeekend, showWeather, highlightSummer, summerStart, summerEnd, highlightEachMonth, dropZeros, deleteOutliers, deleteOutliersForDifference):

    window_size = 30  # smoothing factor
    df = pd.read_csv("input_data/"+fileName)
    colName = df.columns[1]
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])

    print(df.keys())
    # print(df['Date'])
    print(weather_df['Date'].dtype)

    # print(df.keys())


    allData = (dataFrequency == "Show All Data")
    avgPerDay = (dataFrequency == "Show Average Per Day")
    avgPerWeek = (dataFrequency == "Average Per Week")
    
    def deleteOutliers(df, colName):
        Q1 = df[colName].quantile(0.25)
        Q3 = df[colName].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[(df[colName] >= lower_bound) & (df[colName] <= upper_bound)]
        return df


    print("dropZeros: ",dropZeros)
    if dropZeros:
        df = df[df[colName] != 0]
    if deleteOutliers:
        df = deleteOutliers(df, colName)

    df[colName] = df[colName] - df[colName].shift(1)
    df[colName] = df[colName].fillna(0)
    if deleteOutliersForDifference:
        df = deleteOutliers(df, colName)

    # Base figure setup
    fig = go.Figure()

    # Highlight summer
    if highlightSummer:
        # highlight_start = datetime.strptime(summerStart, "%m/%d/%Y")
        # highlight_end = datetime.strptime(summerEnd, "%m/%d/%Y")
        print(type(summerStart))
        print(type(summerEnd))
        highlight_start = datetime.fromtimestamp(summerStart)
        highlight_end = datetime.fromtimestamp(summerEnd)
        print(highlight_start)
        print(highlight_end)
        fig.add_vrect(x0=highlight_start, x1=highlight_end, fillcolor="orange", opacity=0.3, line_width=0, annotation_text="Summer", annotation_position="top left")

    # Highlight each month if enabled
    if highlightEachMonth:
        for month in df['Date'].dt.to_period('M').unique():
            start, end = pd.Timestamp(month.start_time), pd.Timestamp(month.end_time)
            color = '#eb4034' if month.month % 2 == 0 else '#eb9c34'
            fig.add_vrect(x0=start, x1=end, fillcolor=color, opacity=0.2, line_width=0)

    # preprocess to include weather data
    df["Only_Date"] = df['Date'].dt.date
    df['Only_Date'] = pd.to_datetime(df['Only_Date'], errors='coerce')
    weather_df["Only_Date"] = weather_df["Date"]
    df = df.merge(weather_df[["Only_Date", "Mean"]], on='Only_Date', how='left')

    # Plot data based on configuration
    if allData:
        fig.add_trace(go.Scatter(x=df['Date'], y=df[colName], mode='lines', name='All Data', yaxis="y1"))
        if showWeather:
            fig.add_trace(go.Scatter(
                x=df['Date'],
                y=df["Mean"],
                mode='lines',
                line=dict(color='#b3b3b3'),
                name='Mean Weather',
                yaxis="y2",
            ))
    elif avgPerDay:

        daily_avg_df = df.groupby('Only_Date')[[colName, "Mean"]].mean().reset_index()
        daily_avg_df['Only_Date'] = pd.to_datetime(daily_avg_df['Only_Date'], errors='coerce')

        if showWeekend:
            # Determine color for each date based on whether it's a weekend or not
            colors = ['blue' if pd.to_datetime(date).weekday() in [0, 1, 2, 3, 6] else 'red' for date in daily_avg_df['Only_Date']]

            # Plot each line segment with the specified color
            for i in range(len(daily_avg_df) - 1):
                fig.add_trace(go.Scatter(
                    x=daily_avg_df['Only_Date'].iloc[i:i+2],
                    y=daily_avg_df[colName].iloc[i:i+2],
                    mode='lines',
                    line=dict(color=colors[i]),
                    showlegend=False  # Hide individual segments from the legend
                ))

            # Add custom legend items
            fig.add_trace(go.Scatter(
                x=[None], y=[None],
                mode='lines',
                line=dict(color='red'),
                name='Drop in usage (Friday - Saturday)',
                yaxis="y1"
            ))

            fig.add_trace(go.Scatter(
                x=[None], y=[None],
                mode='lines',
                line=dict(color='blue'),
                name='All other days',
                yaxis="y1"
            ))

            if showWeather:
                fig.add_trace(go.Scatter(
                    x=daily_avg_df['Only_Date'],
                    y=daily_avg_df["Mean"],
                    mode='lines',
                    line=dict(color='#b3b3b3'),
                    name='Mean Weather',
                    yaxis="y2",
                ))


            # move the legend to the bottom
            fig.update_layout(
                legend=dict(
                    orientation="h",  # Horizontal orientation
                    yanchor="bottom",  # Align legend vertically at the bottom
                    y=-300,            # Position below the graph
                    xanchor="center",  # Align legend horizontally at the center
                    x=0.5,              # Center the legend horizontally
                )
            )

        else:
            # Plot entire line in red if showWeekend is False
            fig.add_trace(go.Scatter(
                x=daily_avg_df['Only_Date'],
                y=daily_avg_df[colName],
                mode='lines',
                line=dict(color='red'),
                name='Daily Average',
                yaxis="y1",
            ))

            if showWeather:
                fig.add_trace(go.Scatter(
                    x=daily_avg_df['Only_Date'],
                    y=daily_avg_df["Mean"],
                    mode='lines',
                    line=dict(color='#b3b3b3'),
                    name='Mean Weather',
                    yaxis="y2",
                ))

    elif avgPerWeek:
        df["Week"] = df['Date'].dt.to_period('W')
        weekly_avg_df = df.groupby("Week").mean().reset_index()
        weekly_avg_df['Week'] = weekly_avg_df['Week'].dt.start_time
        fig.add_trace(go.Scatter(x=weekly_avg_df['Week'], y=weekly_avg_df[colName], mode='lines', name='Weekly Average', yaxis="y1"))

        if showWeather:
            fig.add_trace(go.Scatter(
                x=weekly_avg_df['Week'],
                y=weekly_avg_df["Mean"],
                mode='lines',
                line=dict(color='#b3b3b3'),
                name='Mean Weather',
                yaxis="y2",
            ))

    # Final figure layout adjustments
    fig.update_layout(
        title=f"Interactive Usage Data for {colName}",
        xaxis_title="Date",
        # yaxis_title="Usage",
        xaxis=dict(rangeslider=dict(visible=True)),
        template="plotly_white",

        yaxis=dict(title="Primary Y Axis"),
        yaxis2=dict(
            title="Secondary Y Axis",
            overlaying="y",
            side="right"
        )
    )
    
    return fig

# Gradio Interface
interface = gr.Interface(
    fn=generate_interactive_plot,
    inputs=[
        gr.Dropdown(choices=file_names, label="File Name", value=file_names[default_i]),
        gr.Dropdown(choices=["Show All Data", "Show Average Per Day", "Average Per Week"], label="Choose Data Frequency", value="Show Average Per Day"),
        gr.Checkbox(label="Show Weekend (for Daily Avg only)"),
        gr.Checkbox(label="Plot Average Weather"),
        gr.Checkbox(label="Highlight Summer Range", value=True),
        gr.DateTime(label="Summer Start Date", include_time=False, value="2023-05-12"),
        gr.DateTime(label="Summer End Date", include_time=False, value="2023-08-25"),
        gr.Checkbox(label="Highlight Each Month"),
        gr.Checkbox(label="Drop Zero Values", value=True),
        gr.Checkbox(label="Delete Outliers", value=True),
        gr.Checkbox(label="Delete Outliers for Difference", value=True),
    ],
    outputs="plot",
    title="Interactive Usage Plot with Zooming",
    description="Select settings and visualize usage data interactively with zoom, pan, and range slider features."
)

interface.launch()
