# Exoplanet Explorer

An interactive Streamlit web application to explore and visualize exoplanet data from the Kaggle "All Exoplanets Dataset".

## Project Overview

This application allows users to:
- View summary statistics about known exoplanets
- Filter exoplanets by properties like mass, radius, and orbital period
- Create interactive scatter plots to explore relationships between different planetary properties
- Visualize distributions of exoplanet characteristics
- See interesting statistics like the largest planets and those with the shortest orbital periods

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone or download this repository to your local machine
2. Install the required packages:

```bash
pip install -r requirements.txt
```

### Running the Application

1. Navigate to the project directory in your terminal
2. Run the Streamlit app:

```bash
streamlit run exoplanet_app.py
```

3. The app will open in your default web browser at `http://localhost:8501`

## Data Source

This project uses the "All Exoplanets Dataset" by Shivam Bansal, available on Kaggle. The dataset is automatically downloaded when you run the application for the first time.

## Features

- **Dataset Overview**: Basic statistics and sample data from the exoplanet dataset
- **Interactive Filtering**: Filter the dataset by planet mass, radius, and orbital period
- **Visualizations**:
  - Scatter plots with customizable axes and color mapping
  - Histograms showing distributions of planetary properties
  - Box plots for statistical summaries
- **Interesting Statistics**: Tables showing notable exoplanets
- **Additional Information**: Charts showing discovery methods and discoveries over time

## Technologies Used

- Streamlit: For the interactive web application
- Pandas: For data manipulation
- Plotly: For interactive visualizations
- Kagglehub: For downloading the dataset

## License

This project is open source and available for educational and personal use.
