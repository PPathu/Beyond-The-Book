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

# Dictionary to map university names to image URLs (update with actual image URLs)
university_images = {
    "University of Wisconsin-Madison": "/Users/pathup/Desktop/beyond_the_book/images/Madison.jpg",
    
}


def generate_rent_plot(rent_data, university_name, axs):
    rent_row = rent_data.loc[rent_data['university'] == university_name]
    if len(rent_row) == 1:
        rent_row = rent_row.squeeze()
        rent_data_values = [rent_row[col] for col in ['fmr_0', 'fmr_1', 'fmr_2', 'fmr_3', 'fmr_4']]
        axs[0, 0].bar(["studio", "1 bedroom", "2 bedroom", "3 bedroom", "4 bedroom"], rent_data_values)
        axs[0, 0].set_title('Rent Data')
        axs[0, 0].set_ylabel("Monthly Rent in $")
    else:
        axs[0, 0].text(0.5, 0.5, 'Rent Data Not Available', ha='center', va='center')
    return axs

# Function to search for a university and visualize data
def search_university(university_name):
    result = college_data.loc[college_data['UniversityName'] == university_name]
    
    if len(result) == 0:
        return "University not found in college_data!"
    
    fig, axs = plt.subplots(2, 2, figsize=(20, 15))

    # rent data
    axs = generate_rent_plot(rent_data, university_name, axs)
    
    # Crime Data
    # Assuming the university's state is available in college_data under a column 'State'
    state = result.squeeze().get('STATE', None)
    if state:
        crime_row = crime_data.loc[crime_data['STATE'] == state]
        if len(crime_row) == 1:
            crime_row = crime_row.squeeze()
            years = [str(year) for year in range(2011, 2021)]
            crime_rates = [crime_row[year] for year in years]
            axs[1, 1].plot(years, crime_rates, marker='o')
            axs[1, 1].set_title('Violent Crime Rates per 100,000 inhabitants (2011–2020)')
            axs[1, 1].set_xlabel('Year')
            axs[1, 1].set_ylabel('Crime Rate')
        else:
            axs[1, 1].text(0.5, 0.5, 'Crime Data Not Available', ha='center', va='center')
    else:
        axs[1, 1].text(0.5, 0.5, 'State Information Not Available', ha='center', va='center')
    
  # Display the university image
    if university_name in university_images:
        img_url = university_images[university_name]
        try:
            img = Image.open(img_url)
        except Exception as e:
    # Display an error message when the image is not available
            print('Image Not Available')
    print(img)
    plt.tight_layout()
    return img, fig


# Gradio interface
iface = gr.Interface(
    fn=search_university,
    inputs=components.Dropdown(choices=list(college_data["UniversityName"]), label="University"),  # Updated
    outputs=[gr.Image(height=100, width=100), 'plot'],
    live=False,
    title='Beyond the Book',
    description='Enter the name of a university to visualize related data.'
)

if __name__ == "__main__":
    iface.launch()
