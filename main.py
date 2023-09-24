from gradio import components, gradio
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.backends.backend_agg import FigureCanvasAgg
import openai
from dotenv import load_dotenv
import os
from io import BytesIO

# Load all the CSV files from the 'data' folder
college_data = pd.read_csv('data/college_data.csv')
rent_data = pd.read_csv('data/big_10_rent.csv')
cost_of_living_data = pd.read_csv('data/cost-of-living-database.csv')
transportation_data = pd.read_csv('data/transportation.csv')
crime_data = pd.read_csv('data/crime_data.csv')
tuition_data = pd.read_csv('data/tution_data.csv')

load_dotenv()
openai.api_key = os.environ.get("OPEN_AI_KEY")

# Dictionary to map university names to image URLs (update with actual image URLs)
university_images = {
    "University of Wisconsin-Madison": "images/Madison.jpg",
    "Ohio State University": "images/ohio-state-buckeyes4939.jpg",
    "Pennsylvania State University. Main Campus": "images/penn-state-shield.jpg",
    "Northwestern University": "images/Northwestern-Wildcats-Logo-1981.png",
    "Michigan State University": "images/Michigan State University.jpg",
    "Indiana University-Bloomington": "images/trident-tab-promo.jpg",
    "Purdue University": "images/emblem-Purdue-University.jpg",
    "Rutgers at New Brunswick": "images/rutgers.png",
    "University of Illinois-Urbana-Champaign": "images/shit state.jpg",
    "University of Iowa": "images/Tigerhawk-gold on black@2x.png",
    "University of Maryland": "images/Maryland-Terrapins-Logo.jpg",
    "University of Michigan": "images/U-M_Logo-Hex.png",
    "University of Minnesota": "images/University of Minnesota.jpg",
    "University of Nebraska": "images/University of Nebraska.jpg",
       
    
}

def fig_to_img(fig):
    """Converts a matplotlib figure object into an image in memory."""
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.5)
    buf.seek(0)
    img = Image.open(buf)
    return img

def generate_tuition_plot(university_name):
    fancy_colors = ['orange', 'red', 'darkred', 'orangered']
    fig, ax = plt.subplots(figsize=(5, 4))
    
    tuition_row = tuition_data.loc[tuition_data['INSTNM'] == university_name]
    if len(tuition_row) == 1:
        tuition_row = tuition_row.squeeze()
        tuition_in = tuition_row['TUITIONFEE_IN']
        tuition_out = tuition_row['TUITIONFEE_OUT']
        ax.bar(['In-State', 'Out-of-State'], [tuition_in, tuition_out], color=fancy_colors[1])
        ax.set_title('Tuition Fees')
        ax.set_ylabel('Cost ($)')
    else:
        ax.text(0.5, 0.5, 'Tuition Data Not Available', ha='center', va='center')
    return fig_to_img(fig)

def generate_spending_plot(university_name):
    fig, ax = plt.subplots(figsize=(5, 4))
    
    result = college_data.loc[college_data['UniversityName'] == university_name]
    room_cost = result['RoomCost'].values[0]
    book_cost = result['BookCost'].values[0]
    personal_spending = result['PersonalSpending'].values[0]
    
    sizes = [room_cost, book_cost, personal_spending]
    labels = [f'Room Cost: ${room_cost}', f'Book Cost: ${book_cost}', f'Personal Spending: ${personal_spending}']
    colors = ['#FFDAB9', '#FFA500', '#FF6B6B']
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    ax.set_title('Distribution of Expenses for College Students')
    return fig_to_img(fig)

def generate_crime_plot(university_name):
    fancy_colors = ['orange', 'red', 'darkred', 'orangered']
    fig, ax = plt.subplots(figsize=(5, 4))
    
    result = college_data.loc[college_data['UniversityName'] == university_name]
    state = result.squeeze().get('STATE', None)
    if state:
        crime_row = crime_data.loc[crime_data['STATE'] == state]
        if len(crime_row) == 1:
            crime_row = crime_row.squeeze()
            years = [str(year) for year in range(2011, 2021)]
            crime_rates = [crime_row[year] for year in years]
            ax.plot(years, crime_rates, marker='o', color=fancy_colors[2])
            ax.set_title('Violent Crime Rates per 100,000 inhabitants (2011–2020)')
            ax.set_xlabel('Year')
            ax.set_ylabel('Crime Rate')
        else:
            ax.text(0.5, 0.5, 'Crime Data Not Available', ha='center', va='center')
    else:
        ax.text(0.5, 0.5, 'State Information Not Available', ha='center', va='center')
    return fig_to_img(fig)

def generate_rent_plot(university_name):
    fancy_colors = ['orange', 'red', 'darkred', 'orangered']
    fig, ax = plt.subplots(figsize=(5, 4))
    rent_row = rent_data.loc[rent_data['university'] == university_name]
    if len(rent_row) == 1:
        rent_row = rent_row.squeeze()
        rent_data_values = [rent_row[col] for col in ['fmr_0', 'fmr_1', 'fmr_2', 'fmr_3', 'fmr_4']]
        ax.bar(["studio", "1 bedroom", "2 bedroom", "3 bedroom", "4 bedroom"], rent_data_values, color=fancy_colors[0])
        ax.set_title('Rent Data')
        ax.set_ylabel("Monthly Rent in $")
    else:
        ax.text(0.5, 0.5, 'Rent Data Not Available', ha='center', va='center')
    return fig_to_img(fig)
    # Function to search for a university and visualize data

dropdown_style = {
    "description_width": "initial",
    "border": "1px solid #E2E2E2",
    "border-radius": "10px",
    "padding": "10px",
}

# Inject some custom CSS for better styling
custom_css = """
    .gradio h2 {
        font-size: 1.5em;
        color: darkblue;
        margin-bottom: 0.5em;
    }
    .gr-interface-description {
        font-style: italic;
        margin-top: 0;
    }
    .gr-dropdown {
        border: 1px solid #E2E2E2 !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
"""

placeholder_image_url = "https://miro.medium.com/v2/resize:fit:2000/format:webp/1*MW9c_tBvDwobDfSAqeR45w.png"

def get_university_image_url(university_name):
    # Get the university image URL from the dictionary or use the placeholder image URL
    return university_images.get(university_name, placeholder_image_url)


with gradio.Blocks() as iface:
    with components.Column():
        components.HTML(
            """
            <h1 style="text-align:center; font-size:55px;">Beyond The Book 📚</h1>
            """
        )
        with components.Row():
            with components.Column():
                university_input = components.Dropdown(choices=list(college_data["UniversityName"]), label="Select a University")
                
                rent_output = components.Image(width=800, show_label=False, show_download_button=False)
                tuition_output = components.Image(width=800, show_label=False, show_download_button=False)
                spending_output = components.Image(width=800, show_label=False, show_download_button=False)
                crime_output = components.Image(width=800, show_label=False, show_download_button=False)
                
                def combined_fn(university_name):
                    rent_img = generate_rent_plot(university_name)
                    tuition_img = generate_tuition_plot(university_name)
                    spending_img = generate_spending_plot(university_name)
                    crime_img = generate_crime_plot(university_name)
                     # Get the university image URL
                    university_image_url = get_university_image_url(university_name)
                    
                    
                    return university_image_url, rent_img, tuition_img, spending_img, crime_img,   # Include university image URL 
                        
                gradio.Interface(
                    fn=combined_fn,
                    inputs=university_input,
                    outputs=[components.Image(width=200, height=200, show_label=False, show_download_button=False), rent_output, tuition_output, spending_output, crime_output],  # Add an Image component for the university image
                    live=False,
                    theme='default',
                    css=custom_css,
                    allow_flagging="never"
                )
            with components.Column():
                chatbot = components.Chatbot(show_label=False, scale=2)
                msg = components.Textbox(label="Chat Box")
                clear = components.ClearButton([msg, chatbot])
                def respond(message, chat_history):
                    # Initialize with a system message
                    messages = [{"role": "system", "content": "You are a helpful assistant."}]
                    
                    # Append user's and assistant's previous messages
                    for m in chat_history:
                        user_msg, assistant_msg = m
                        messages.append({"role": "user", "content": user_msg})
                        messages.append({"role": "assistant", "content": assistant_msg})
                        
                    # Append the current user's message
                    messages.append({"role": "user", "content": message})
                    
                    # Get a response from the Chat GPT API
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages,
                        stop=None,
                        n=1,
                        max_tokens=100
                    )
                    
                    bot_message = response.choices[0].message['content'].strip()
                    chat_history.append((message, bot_message))
                    return "", chat_history
                msg.submit(respond, [msg, chatbot], [msg, chatbot])


"""
iface = gr.Interface(
    fn=search_university,
    outputs=gr.Image(width=800, show_label=False, show_download_button=False),  # adjust dimensions as needed
    inputs=components.Dropdown(
        choices=list(college_data["UniversityName"]), 
        label="Select a University"),
    live=False,
    title='Beyond the Book 🎓',
    description='Visualize data related to different universities. Select a university to get started.',
    theme='default',
    css=custom_css,
    allow_flagging="never"
)
"""

if __name__ == "__main__":
    iface.launch()
