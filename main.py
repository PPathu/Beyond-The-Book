import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt

# Load all the CSV files
college_data = pd.read_csv('college_data.csv')
rent_data = pd.read_csv('rent_data.csv')
cost_of_living_data = pd.read_csv('cost-of-living-database.csv')
transportation_data = pd.read_csv('transportation.csv')
crime_data = pd.read_csv('crime_data.csv')
tuition_data = pd.read_csv('tution_data.csv')

# Function to search for a university and visualize data
def search_university(university_name):
    result = college_data[college_data['University_Name'].str.contains(university_name, case=False, na=False)]
    
    if len(result) == 0:
        return "University not found!"
    
    # Create some example plots (replace this with your actual visualizations)
    fig, axs = plt.subplots(2, 3, figsize=(15, 10))
    
    axs[0, 0].bar(rent_data['Location'], rent_data['Rent'])
    axs[0, 0].set_title('Rent Data')
    
    axs[0, 1].bar(cost_of_living_data['Location'], cost_of_living_data['Cost'])
    axs[0, 1].set_title('Cost of Living')
    
    axs[0, 2].bar(transportation_data['Location'], transportation_data['Transport_Cost'])
    axs[0, 2].set_title('Transportation Costs')
    
    axs[1, 0].bar(crime_data['Location'], crime_data['Crime_Rate'])
    axs[1, 0].set_title('Crime Data')
    
    axs[1, 1].bar(tuition_data['University'], tuition_data['Tuition'])
    axs[1, 1].set_title('Tuition Data')
    
    axs[1, 2].axis('off')  # Hide the last plot
    
    plt.tight_layout()
    return fig

# Gradio interface
iface = gr.Interface(
    fn=search_university,
    inputs=gr.inputs.Textbox(lines=1, placeholder='Enter University Name...'),
    outputs='plot',
    live=False,
    title='University Data Visualization',
    description='Enter the name of a university to visualize related data.'
)

if __name__ == "__main__":
    iface.launch()

