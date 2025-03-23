import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import os
import kagglehub

# Set page configuration
st.set_page_config(
    page_title="Exoplanet Explorer",
    page_icon="🪐",
    layout="wide"
)

# Function to load data
@st.cache_data
def load_data():
    # Define a local path to store the dataset
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    csv_path = os.path.join(data_dir, "exoplanets.csv")
    
    # Check if the dataset is already downloaded and saved locally
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            return df
        except Exception as e:
            st.error(f"Error reading local dataset: {e}")
    
    # If not available locally, download from Kaggle
    try:
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Download dataset
        st.info("Downloading dataset from Kaggle (this will only happen once)...")
        kaggle_path = kagglehub.dataset_download("shivamb/all-exoplanets-dataset")
        
        # Find the CSV file in the downloaded directory
        for file in os.listdir(kaggle_path):
            if file.endswith('.csv'):
                file_path = os.path.join(kaggle_path, file)
                df = pd.read_csv(file_path)
                
                # Save locally for future use
                df.to_csv(csv_path, index=False)
                return df
        
        st.error("No CSV file found in the downloaded dataset.")
        return None
    except Exception as e:
        st.error(f"Error downloading dataset: {e}")
        return None

# Main title
st.title("🪐 Exoplanet Explorer")
st.write("Explore and visualize data from thousands of confirmed exoplanets.")

# Load the dataset
with st.spinner("Loading exoplanet data..."):
    df = load_data()

if df is not None:
    # Display basic information about the dataset
    st.header("Dataset Overview")
    
    # Show a sample of the data
    with st.expander("View Sample Data"):
        st.dataframe(df.head())
    
    # Show summary statistics
    with st.expander("View Summary Statistics"):
        st.dataframe(df.describe())
    
    # Sidebar for filtering
    st.sidebar.header("Filter Data")
    
    # Identify numeric columns for filtering
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    
    # Mass filter (if available)
    if 'Mass' in numeric_cols:
        min_mass, max_mass = float(df['Mass'].min()), float(df['Mass'].max())
        mass_range = st.sidebar.slider(
            "Planet Mass (Jupiter masses)",
            min_value=min_mass,
            max_value=max_mass,
            value=(min_mass, max_mass)
        )
    
    # Radius filter (if available)
    if 'Stellar Radius' in numeric_cols:
        min_radius, max_radius = float(df['Stellar Radius'].min()), float(df['Stellar Radius'].max())
        radius_range = st.sidebar.slider(
            "Stellar Radius (Solar radii)",
            min_value=min_radius,
            max_value=max_radius,
            value=(min_radius, max_radius)
        )
    
    # Orbital period filter (if available)
    if 'Orbital Period Days' in numeric_cols:
        min_period, max_period = float(df['Orbital Period Days'].min()), float(df['Orbital Period Days'].max())
        period_range = st.sidebar.slider(
            "Orbital Period (days)",
            min_value=min_period,
            max_value=max_period,
            value=(min_period, max_period)
        )
    
    # Temperature filter (if available)
    if 'Equilibrium Temperature' in numeric_cols:
        min_temp, max_temp = float(df['Equilibrium Temperature'].min()), float(df['Equilibrium Temperature'].max())
        temp_range = st.sidebar.slider(
            "Equilibrium Temperature (K)",
            min_value=min_temp,
            max_value=max_temp,
            value=(min_temp, max_temp)
        )
    
    # Distance filter (if available)
    if 'Distance' in numeric_cols:
        min_dist, max_dist = float(df['Distance'].min()), float(df['Distance'].max())
        dist_range = st.sidebar.slider(
            "Distance (parsecs)",
            min_value=min_dist,
            max_value=max_dist,
            value=(min_dist, max_dist)
        )
    
    # Apply filters
    filtered_df = df.copy()
    
    if 'Mass' in numeric_cols:
        filtered_df = filtered_df[(filtered_df['Mass'] >= mass_range[0]) & 
                                 (filtered_df['Mass'] <= mass_range[1])]
    
    if 'Stellar Radius' in numeric_cols:
        filtered_df = filtered_df[(filtered_df['Stellar Radius'] >= radius_range[0]) & 
                                 (filtered_df['Stellar Radius'] <= radius_range[1])]
    
    if 'Orbital Period Days' in numeric_cols:
        filtered_df = filtered_df[(filtered_df['Orbital Period Days'] >= period_range[0]) & 
                                 (filtered_df['Orbital Period Days'] <= period_range[1])]
    
    if 'Equilibrium Temperature' in numeric_cols:
        filtered_df = filtered_df[(filtered_df['Equilibrium Temperature'] >= temp_range[0]) & 
                                 (filtered_df['Equilibrium Temperature'] <= temp_range[1])]
    
    if 'Distance' in numeric_cols:
        filtered_df = filtered_df[(filtered_df['Distance'] >= dist_range[0]) & 
                                 (filtered_df['Distance'] <= dist_range[1])]
    
    # Show number of planets after filtering
    st.sidebar.metric("Filtered Exoplanets", filtered_df.shape[0])
    st.sidebar.metric("Total Exoplanets", df.shape[0])
    
    # Visualizations
    st.header("Exoplanet Visualizations")
    
    # Scatter plot
    st.subheader("Relationship Between Exoplanet Properties")
    
    # Get numeric columns for scatter plot
    scatter_cols = [col for col in numeric_cols if col not in ['No.']]
    
    col1, col2 = st.columns(2)
    with col1:
        x_axis = st.selectbox("X-axis", scatter_cols, 
                             index=scatter_cols.index('Orbital Period Days') if 'Orbital Period Days' in scatter_cols else 0)
    with col2:
        y_axis = st.selectbox("Y-axis", scatter_cols, 
                             index=scatter_cols.index('Mass') if 'Mass' in scatter_cols else min(1, len(scatter_cols)-1))
    
    # Color by
    color_by = st.selectbox("Color by", ['None'] + scatter_cols, index=0)
    
    # Create scatter plot
    fig = px.scatter(
        filtered_df,
        x=x_axis,
        y=y_axis,
        color=None if color_by == 'None' else color_by,
        hover_name='Planet Name' if 'Planet Name' in filtered_df.columns else None,
        log_x=st.checkbox("Log scale (X-axis)", value=True),
        log_y=st.checkbox("Log scale (Y-axis)", value=True),
        title=f"{y_axis} vs {x_axis}"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Distribution plots
    st.subheader("Distribution of Exoplanet Properties")
    
    dist_tabs = st.tabs(["Histogram", "Box Plot"])
    
    with dist_tabs[0]:
        # Histogram
        hist_col = st.selectbox("Select property for histogram", scatter_cols, key="hist_select")
        
        fig = px.histogram(
            filtered_df, 
            x=hist_col,
            title=f"Distribution of {hist_col}",
            log_y=st.checkbox("Log scale (Y-axis)", value=False, key="hist_log")
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with dist_tabs[1]:
        # Box plot
        box_col = st.selectbox("Select property for box plot", scatter_cols, key="box_select")
        
        fig = px.box(
            filtered_df,
            y=box_col,
            title=f"Box Plot of {box_col}"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Top 5 lists
    st.header("Interesting Statistics")
    stat_cols = st.columns(2)
    
    # Top 5 largest planets (by mass)
    with stat_cols[0]:
        if 'Mass' in numeric_cols:
            st.subheader("5 Most Massive Planets")
            largest_planets = filtered_df.sort_values('Mass', ascending=False).head(5)
            st.table(largest_planets[['Planet Name', 'Mass']].reset_index(drop=True))
    
    # Top 5 planets with shortest orbital periods
    with stat_cols[1]:
        if 'Orbital Period Days' in numeric_cols:
            st.subheader("5 Planets with Shortest Orbital Periods")
            shortest_period = filtered_df.sort_values('Orbital Period Days').head(5)
            st.table(shortest_period[['Planet Name', 'Orbital Period Days']].reset_index(drop=True))
    
    # Additional information
    st.header("Additional Information")
    
    # Discovery methods
    if 'Discovery Method' in df.columns:
        st.subheader("Discovery Methods")
        
        detection_counts = filtered_df['Discovery Method'].value_counts().reset_index()
        detection_counts.columns = ['Method', 'Count']
        
        fig = px.pie(
            detection_counts, 
            values='Count', 
            names='Method',
            title="Exoplanet Discovery Methods"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Year of discovery
    if 'Discovery Year' in df.columns:
        st.subheader("Discoveries Over Time")
        
        # Group by year and count
        yearly_counts = filtered_df.groupby('Discovery Year').size().reset_index(name='count')
        
        fig = px.bar(
            yearly_counts,
            x='Discovery Year',
            y='count',
            title="Exoplanet Discoveries by Year"
        )
        st.plotly_chart(fig, use_container_width=True)
else:
    st.error("Failed to load the dataset. Please check your internet connection and try again.")

# Footer
st.markdown("---")
st.markdown("Exoplanet Explorer App | Data source: Kaggle - All Exoplanets Dataset by Shivam Bansal")
