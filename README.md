# Energy Usage Data Project

## Overview  
The purpose of this project was to create an energy usage dashaboard to analyze trends in energy usage for different forms of energy and different buildings on campus.

---

## Dashboard Features  
- **Feature 1:** Select from multiple csv files in a folder
- **Feature 2:** Plot all data / average reading per day / average reading per week
- **Feature 3:** Show changes in energy usage data between weekdays and weekends
- **Feature 4:** Highlight summer months in energy plot / highlight indiviudal months
- **Feature 5:** Visualize usage data interactively with zoom, pan, and range slider features
- And more!

![Alt Text](https://drive.google.com/uc?id=19hmf4ydC5bcJ_QhyOwj3L-NMqKrgUN0X)

---

## Setup Instructions  

### Prerequisites  
1. Install Python

### Installation  
1. Clone the repository:  
   ```bash
   git clone https://github.com/superstarcoder/energy-usage-data-project.git
   cd energy-usage-data-project
   ```
2. Install the required libraries:
   ```bash
   pip3 install gradio pandas plotly
   ```
3. Create a folder inside the `energy-usage-data-project` folder called `input_data`. This folder should contain all the .csv files that you want the dashboard to analyze.
4. Run the dashboard!
   ```bash
   python3 energy_data_dashboard.py
   ```
