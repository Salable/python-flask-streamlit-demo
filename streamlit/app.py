import pandas as pd
import streamlit as st
import io
import requests
import dotenv
import os

dotenv.load_dotenv()

api_base_url=os.environ.get("API_BASE_URL", "")

st.title("Welcome to LatLong")
user_input= st.text_area("Enter your city")
grantee_id=""

def is_not_licensed():
    st.error('You are not licensed!', icon="❌")
    if st.button("Get API key"):
        response = requests.post(api_base_url+"/purchase", json={}).json()
        if "error" in response:
            st.write(response["error"])
        else:
            grantee_id=response["grantee_id"]
            st.session_state["grantee_id"]=grantee_id
            st.experimental_rerun()

with st.sidebar:
    grantee_id=st.text_input("Enter your API key", value=st.session_state.get("grantee_id", ""))
    if grantee_id and grantee_id != "":
        print(grantee_id)
        is_licensed=requests.get(api_base_url+"/purchase?api_key="+grantee_id).json()["licensed"]
        if is_licensed:
            st.success('You are licensed!', icon="✅")
        else:
            is_not_licensed()
    else:
        is_not_licensed()

if user_input:
    response = requests.post(api_base_url+"/search", json={"query": user_input, "api_key": grantee_id}).json()
    print(response)
    if "error" in response:
        st.write(response["error"])
    else:
        try:
            csv_file = io.StringIO(response["response"])
            trees_df = pd.read_csv(csv_file)
            trees_df = trees_df.dropna(subset=["longitude", "latitude"])
            trees_df = trees_df.sample(n=1000, replace=True)
            st.map(trees_df)
        except:
            st.write("Sorry please try another query.")