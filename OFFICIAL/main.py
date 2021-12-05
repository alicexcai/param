import streamlit as st

# Custom imports 
from multipage import MultiPage
from pages import experiment, visualize, testpage

# Create an instance of the app 
app = MultiPage()

# Title of the main page
st.title("Data Storyteller Application")

# Add all your applications (pages) here
app.add_page("Experiment", testpage.app)
# app.add_page("Experiment", experiment.app)
# app.add_page("Visualize", visualize.app)

# app.add_page("Upload Data", data_upload.app)
# app.add_page("Change Metadata", metadata.app)
# app.add_page("Machine Learning", machine_learning.app)
# app.add_page("Data Analysis",data_visualize.app)
# app.add_page("Y-Parameter Optimization",redundant.app)

# The main app
app.run()