# streamlit run C:\Users\bapti\OneDrive\Python\secret_santa\main.py

import streamlit as st
import json
from variables.people import people
from core.functions.distribution import get_assignments, get_givers
import datetime

seed = datetime.datetime.now().year

# seed = 42
try:
    st.image("secret_santa.jpg")
except:
    pass
st.write(f"# Père Noël secret des Monney {datetime.datetime.now().year}🎅")

with st.form("my_form"):
    secret_code = st.text_input(
        "Entrez votre code (attention aux majuscules et minuscules) : "
    )
    # Every form must have a submit button.
    submitted = st.form_submit_button("Valider le code")
    if submitted:

        if secret_code not in get_givers(seed=seed).values():
            st.write("Code invalide, réessayez.")
        else:
            st.write(
                f"## Vous êtes le père Nöel pour : {get_assignments(secret_code, seed=seed)}"
            )

if secret_code == "IAMSANTA":

    with open("output.txt", "w") as f:
        json.dump(get_givers(seed=seed), f, indent=4)
    with open("output.txt", "rb") as file:

        st.download_button(
            label="Télécharger le fichier des attributions",
            data=file,
            file_name="secret_santa_attributions.json",
            mime="text/plain",
        )
