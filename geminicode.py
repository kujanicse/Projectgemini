import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configure Google Gemini API directly with the key
genai.configure(api_key="AIzaSyCTNVm8USN7GhJ2obW4nTmIniCqPFIup9E")

# Function to interact with Google Gemini Pro Vision API and get response
def get_gemini_response(input_text, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, image[0], prompt])
    return response.text

# Function to prepare uploaded image for processing
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        return None

# Initialize Streamlit app
st.set_page_config(page_title="Animal Species Detection")

# Main content
st.header("Animal Species Detection")
input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me this animal")

input_prompt = """
You are an expert in animal species identification, and you need to provide detailed information about the species depicted in the image.

Please use the following details to describe the identified species:

1. *Common Name:* [Common name of the species]
2. *Scientific Name:scription:* [Brief * [Scientific name of the species]
3. *Dedescription of the species, including its physical characteristics, habitat, behavior, and any distinctive features]
4. *Range:* [Geographical range where the species is commonly found, including continents, countries, or specific ecosystems]
5. *Conservation Status:* [Conservation status of the species, indicating whether it is endangered, vulnerable, or of least concern according to organizations like the IUCN]
6. *Ecological Role:* [Discussion of the ecological role of the species within its habitat or ecosystem, such as its position in the food chain, interactions with other species, or contributions to ecosystem services]
7. *Interesting Facts:* [Any interesting or unique facts about the species that may capture the user's attention and deepen their understanding of its significance]

Feel free to include additional images or videos of the species in its natural habitat to enhance the user's learning experience.
"""

# If submit button is clicked
if submit:
    image_data = input_image_setup(uploaded_file)
    if image_data is not None:
        response = get_gemini_response(input_text, image_data, input_prompt)

        # Check if the response indicates a failure to detect an animal
        if "No animal detected" in response:
            st.warning("Please upload a valid image containing an animal.")
        else:
            # Add border around output
            st.markdown('<style>div.Widget.row-widget.stRadio > div{flex-direction:column;}</style>', unsafe_allow_html=True)
            st.subheader("The Response is")
            st.markdown(response)