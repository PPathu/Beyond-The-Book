import gradio as gr
from gradio import components  # Import the components
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.backends.backend_agg import FigureCanvasAgg
import openai
from dotenv import load_dotenv
import os

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


def generate_rent_plot(rent_data, university_name, axs):
    rent_row = rent_data.loc[rent_data['university'] == university_name]
    fancy_colors = ['orange', 'red', 'darkred', 'orangered']
    if len(rent_row) == 1:
        rent_row = rent_row.squeeze()
        rent_data_values = [rent_row[col] for col in ['fmr_0', 'fmr_1', 'fmr_2', 'fmr_3', 'fmr_4']]
        axs[0, 0].bar(["studio", "1 bedroom", "2 bedroom", "3 bedroom", "4 bedroom"], rent_data_values, color=fancy_colors[0])
        axs[0, 0].set_title('Rent Data')
        axs[0, 0].set_ylabel("Monthly Rent in $")
    else:
        axs[0, 0].text(0.5, 0.5, 'Rent Data Not Available', ha='center', va='center')
    return axs

# Function to search for a university and visualize data
def search_university(university_name):
    fancy_colors = ['orange', 'red', 'darkred', 'orangered']

    result = college_data.loc[college_data['UniversityName'] == university_name]
    
    if len(result) == 0:
        return "University not found in college_data!"
    
    fig, axs = plt.subplots(2, 2, figsize=(20, 15))

    #fig, axs = plt.subplots(2, 2, figsize=(15, 10))

    # rent data
    axs = generate_rent_plot(rent_data, university_name, axs)
    
    # Tuition Data
    tuition_row = tuition_data.loc[tuition_data['INSTNM'] == university_name]
    if len(tuition_row) == 1:
        tuition_row = tuition_row.squeeze()
        tuition_in = tuition_row['TUITIONFEE_IN']
        tuition_out = tuition_row['TUITIONFEE_OUT']
        axs[0, 1].bar(['In-State', 'Out-of-State'], [tuition_in, tuition_out], color=fancy_colors[1])
        axs[0, 1].set_title('Tuition Fees')
        axs[0, 1].set_ylabel('Cost ($)')
        for i, v in enumerate([tuition_in, tuition_out]):
            axs[0, 1].text(i, v + 500, "$" + str(v), color='black', ha='center')
    else:
        axs[0, 1].text(0.5, 0.5, 'Tuition Data Not Available', ha='center', va='center')

    # Spending Data 
    room_cost = result['RoomCost'].values[0]
    book_cost = result['BookCost'].values[0]
    personal_spending = result['PersonalSpending'].values[0]
    total_spending = room_cost + book_cost + personal_spending

    sizes = [room_cost, book_cost, personal_spending]
    labels = [f'Room Cost: ${room_cost}', f'Book Cost: ${book_cost}', f'Personal Spending: ${personal_spending}']
    colors = ['#FFDAB9', '#FFA500', '#FF6B6B']
    axs[1, 0].pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    axs[1, 0].set_title('Distribution of Expenses for College Students')


    # Crime Data
    # Assuming the university's state is available in college_data under a column 'State'
    state = result.squeeze().get('STATE', None)
    if state:
        crime_row = crime_data.loc[crime_data['STATE'] == state]
        if len(crime_row) == 1:
            crime_row = crime_row.squeeze()
            years = [str(year) for year in range(2011, 2021)]
            crime_rates = [crime_row[year] for year in years]
            axs[1, 1].plot(years, crime_rates, marker='o', color=fancy_colors[2])
            axs[1, 1].set_title('Violent Crime Rates per 100,000 inhabitants (2011–2020)')
            axs[1, 1].set_xlabel('Year')
            axs[1, 1].set_ylabel('Crime Rate')
        else:
            axs[1, 1].text(0.5, 0.5, 'Crime Data Not Available', ha='center', va='center')
    else:
        axs[1, 1].text(0.5, 0.5, 'State Information Not Available', ha='center', va='center')
    
    plt.tight_layout()

    # Convert the Matplotlib figure to a PIL Image
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    s, (width, height) = canvas.print_to_buffer()
    plot_image = Image.frombytes("RGBA", (width, height), s)

    # Display the university image on top of the plot
    if university_name in university_images:
        img_url = university_images[university_name]
        logo_img = Image.open(img_url)
        
        # Resize the logo to a smaller size
        logo_img = logo_img.resize((int(width/3), int((width/3) * logo_img.height / logo_img.width)))
        
        combined_img = Image.new("RGBA", (width, logo_img.height + plot_image.height))
        combined_img.paste(logo_img, (int((width - logo_img.width) / 2), 0))
        combined_img.paste(plot_image, (0, logo_img.height))
        return combined_img
    else:
        return plot_image

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

with gr.Blocks() as iface:
    with gr.Column():
        gr.HTML(
            """
            <h1 style="text-align:center">Beyond the Book</h1>
            """
        )
        with gr.Row():
            with gr.Column():
                """
                university = components.Dropdown(
                    choices=list(college_data["UniversityName"]), 
                    label="Select a University"
                )
                submit_button = components.Button()
                """
                gr.Interface(
                    fn=search_university,
                    outputs=gr.Image(width=800, show_label=False, show_download_button=False),  # adjust dimensions as needed
                    inputs=components.Dropdown(
                        choices=list(college_data["UniversityName"]), 
                        label="Select a University"),
                    live=False,
                    #title='Beyond the Book 🎓',
                    #description='Visualize data related to different universities. Select a university to get started.',
                    theme='default',
                    css=custom_css,
                    allow_flagging="never"
                )

            with gr.Column():
                chatbot = components.Chatbot(show_label=False)
                msg = components.Textbox()
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
