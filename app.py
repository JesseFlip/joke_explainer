import streamlit as st
from openai import OpenAI
import os

# Access the API key from the environment variable
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Check if the API key is available
if not OPENAI_API_KEY:
    st.error("OpenAI API key not found. Please set it as an environment variable.")
    st.stop()

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize session state for explanations
if "initial_explanation" not in st.session_state:
    st.session_state["initial_explanation"] = None
if "detailed_explanation" not in st.session_state:
    st.session_state["detailed_explanation"] = None
if "show_more_button" not in st.session_state:
    st.session_state["show_more_button"] = False

# Dictionary to store languages with their symbols and translations
translations = {
    "English (🇺🇸)": {"submit": "Explain Joke", "more": "Tell me more"},
    "Spanish (🇪🇸)": {"submit": "Explicar el Chiste", "more": "Cuéntame más"},
    "French (🇫🇷)": {"submit": "Expliquer la Blague", "more": "Dis-m'en plus"},
    "German (🇩🇪)": {"submit": "Witz Erklären", "more": "Erzähl mir mehr"},
    "Italian (🇮🇹)": {"submit": "Spiega la Battuta", "more": "Raccontami di più"},
    "Portuguese (🇵🇹)": {"submit": "Explicar a Piada", "more": "Conte-me mais"},
    "Chinese (🇨🇳)": {"submit": "解释笑话", "more": "告诉我更多"},
    "Japanese (🇯🇵)": {"submit": "ジョークを説明する", "more": "もっと教えて"},
    # Add even more languages with their symbols and translations as needed
}

st.title("Joke Explainer")

joke_text = st.text_area("Paste your joke here:")

selected_language_with_symbol = st.selectbox(
    "Select the language for the explanation:",
    list(translations.keys()),
)

# Extract the language name without the symbol for the prompt
selected_language = selected_language_with_symbol.split(" ")[0]

if st.button(translations[selected_language_with_symbol]["submit"]):
    if joke_text:
        try:
            prompt = f"Explain this joke in {selected_language}: {joke_text}"
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # You can choose a different model
                messages=[{"role": "user", "content": prompt}],
            )
            st.session_state["initial_explanation"] = response.choices[0].message.content
            st.session_state["detailed_explanation"] = None  # Reset detailed explanation
            st.session_state["show_more_button"] = True # Show the 'Tell me more' button

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please paste a joke in the text box.")

if st.session_state["initial_explanation"]:
    st.subheader("Explanation:")
    st.write(st.session_state["initial_explanation"])

    if st.session_state["show_more_button"]:
        if st.button(translations[selected_language_with_symbol]["more"]):
            if joke_text:
                try:
                    prompt_more = f"Explain this joke in more detail in {selected_language}: {joke_text}. Expand on the nuances and cultural context if applicable."
                    response_more = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt_more}],
                    )
                    st.session_state["detailed_explanation"] = response_more.choices[0].message.content
                except Exception as e:
                    st.error(f"An error occurred while fetching more details: {e}")
            else:
                st.warning("Please paste a joke in the text box.")

if st.session_state["detailed_explanation"]:
    st.subheader("More Detailed Explanation:")
    st.write(st.session_state["detailed_explanation"])