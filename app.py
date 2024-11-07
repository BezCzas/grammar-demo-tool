import streamlit as st
import openai
import os
from pydantic import BaseModel


# Ustaw klucz API OpenAI
api_key = os.getenv("OPENAI_API_KEY")

st.title("Aplikacja tłumacząca na bezczas")

client = openai.OpenAI(api_key=api_key)


# Wcztanie gramatyk
def load_files_to_dict(folder_path):
    files_dict = {}
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                files_dict[filename] = file.read()
    return files_dict

folder_path = 'system_prompts'
grammars = load_files_to_dict(folder_path)


# Wybór języka tłumaczenia
selected_grammar = st.selectbox("Wybierz gramatykę", grammars.keys())

# Pole tekstowe dla zdania do przetłumaczenia
zdanie_do_przetlumaczenia = st.text_area("Zdanie do przetłumaczenia", "")



class Translation(BaseModel):
    original_sentence: str
    timeless_sentence: str


# Przycisk "tłumacz"
if st.button("tłumacz"):
    if zdanie_do_przetlumaczenia.strip():
        odpowiedz = client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": grammars[selected_grammar]},
                {"role": "user", "content": zdanie_do_przetlumaczenia}
            ],
            response_format=Translation
        )
        przetlumaczone_zdanie = odpowiedz.choices[0].message.parsed.timeless_sentence
    else:
        przetlumaczone_zdanie = "Proszę wpisać zdanie do przetłumaczenia."
else:
    przetlumaczone_zdanie = ""

# Pole tekstowe dla przetłumaczonego zdania
st.text_area("Przetłumaczone zdanie", przetlumaczone_zdanie)