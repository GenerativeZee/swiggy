import streamlit as st
import requests

st.title("Personal Assistant Bot...")

user_query = st.text_input("Enter your request:")

if st.button("Submit"):
    if user_query.strip() == "":
        st.warning("Please enter a query.")
    else:
        url = "http://127.0.0.1:9090/response"
        payload = {"query": user_query}
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                st.success("API Response:")
                st.json(response.json())  # Nicely formatted JSON!
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Error connecting to API: {e}")
