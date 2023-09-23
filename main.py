import gradio as gr
from gradio import components  # Import the components
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# Load all the CSV files from the 'data' folder
college_data = pd.read_csv('data/college_data.csv')
rent_data = pd.read_csv('data/big_10_rent.csv')
cost_of_living_data = pd.read_csv('data/cost-of-living-database.csv')
transportation_data = pd.read_csv('data/transportation.csv')
crime_data = pd.read_csv('data/crime_data.csv')
tuition_data = pd.read_csv('data/tution_data.csv')

# Function to search for a university and visualize data
def search_university(university_name):
    result = college_data.loc[college_data['UniversityName'] == university_name]
    if len(result) == 0:
        return "University not found!"
    
    # Create some example plots (replace this with your actual visualizations)
    fig, axs = plt.subplots(2, 3, figsize=(15, 10))
    
    row = rent_data.loc[rent_data['university'] == university_name].squeeze()

    fmr_0_value = row['fmr_0']
    fmr_1_value = row['fmr_1']
    fmr_2_value = row['fmr_2']
    fmr_3_value = row['fmr_3']
    fmr_4_value = row['fmr_4']

    data = [fmr_0_value, fmr_1_value, fmr_2_value, fmr_3_value, fmr_4_value]

    axs[0, 0].bar(["studio", "1 bedroom", "2 bedroom", "3 bedroom", "4 bedroom"], data)
    axs[0, 0].set_title('Rent Data')
    
    """
    axs[0, 1].bar(cost_of_living_data['Location'], cost_of_living_data['Cost'])
    axs[0, 1].set_title('Cost of Living')
    
    axs[0, 2].bar(transportation_data['Location'], transportation_data['Transport_Cost'])
    axs[0, 2].set_title('Transportation Costs')
    
    axs[1, 0].bar(crime_data['Location'], crime_data['Crime_Rate'])
    axs[1, 0].set_title('Crime Data')
    
    axs[1, 1].bar(tuition_data['University'], tuition_data['Tuition'])
    axs[1, 1].set_title('Tuition Data')
    
    axs[1, 2].axis('off')  # Hide the last plot
    
    """
    plt.tight_layout()
    return fig

# Gradio interface
iface = gr.Interface(
    fn=search_university,
    inputs=components.Dropdown(choices=list(college_data["UniversityName"]), label="University"),  # Updated
    outputs='plot',
    live=False,
    title='Beyond the Book',
    description='Enter the name of a university to visualize related data.'
)

if __name__ == "__main__":
    iface.launch()
