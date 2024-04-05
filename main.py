import streamlit as st
from openai import OpenAI
import tempfile
import os
import pydub

# Function to convert text to speech, modified to explicitly use an API key
def text_to_speech(api_key, text: str, model, voice):
    # Initialize the OpenAI client with the provided API key
    client = OpenAI(api_key=api_key)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
        speech_file_path = tmpfile.name
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=text
        )
        # Stream the audio response to file
        response.stream_to_file(speech_file_path)

        # Return the path to the audio file
        return speech_file_path

def convert_audio_format(input_path, output_path, format):
    audio = pydub.AudioSegment.from_mp3(input_path)
    audio.export(output_path, format=format)

# Streamlit UI setup
st.title("🔊 Text to Speech Converter 📝")
#st.image("https://www.piecex.com/product_image/20190625044028-00000544-image2.png")
st.markdown("""
This app converts text to speech using OpenAI's tts-1 or tts-1-hd model.
Please enter your OpenAI API key on sidebar. **Do not share your API key with others.**
""")

# Input for OpenAI API key
api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

# Select box for model selection
model = st.sidebar.selectbox("Select Model", ["tts-1", "tts-1-hd"])

# Select box for voice selection
voice = st.sidebar.selectbox("Select Voice", ["alloy", "echo", "fable", "onyx", "nova", "shimmer"])

# Select box for format selection
format = st.sidebar.selectbox("Select Format", ["mp3", "opus", "aac", "flac", "wav"])

# Text input from user
user_input = st.text_area("Enter text to convert to speech", "Hello, welcome to our text to speech converter!")

if st.button("Convert"):
    if not api_key:
        st.error("API key is required to convert text to speech.")
    else:
        with st.spinner("Converting text to speech..."):
            try:
                mp3_speech_path = text_to_speech(api_key, user_input, model, voice)

                if format != "mp3":
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{format}") as tmpfile:
                        convert_audio_format(mp3_speech_path, tmpfile.name, format)
                        speech_path = tmpfile.name
                    os.remove(mp3_speech_path)
                else:
                    speech_path = mp3_speech_path

                # Display a link to download the audio file
                st.audio(open(speech_path, 'rb'), format=format)
                st.markdown(f'[Download {format.upper()} file]({speech_path})', unsafe_allow_html=True)

                # Clean up: delete the temporary file after use
                os.remove(speech_path)
            except Exception as e:
                st.error(f"An error occurred: {e}")


# Set a background image
def set_background_image():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://images.pexels.com/photos/4097159/pexels-photo-4097159.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1);
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_background_image()

# Set a background image for the sidebar
sidebar_background_image = '''
<style>
[data-testid="stSidebar"] {
    background-image: url("https://www.pexels.com/photo/abstract-background-with-green-smear-of-paint-6423446/");
    background-size: cover;
}
</style>
'''

st.sidebar.markdown(sidebar_background_image, unsafe_allow_html=True)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


