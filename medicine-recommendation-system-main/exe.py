import streamlit as st
import pickle
import pandas as pd

# Load CSS styles
custom_css = """
<style>
/* New CSS styles */
body {
    background-color: #f0f2f6;
    font-family: Arial, sans-serif;
}

.login-container {
    max-width: 400px;
    margin: 100px auto;
    padding: 20px;
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.login-title {
    text-align: center;
    color: #333;
    font-size: 24px;
    margin-bottom: 30px;
}

.login-input {
    width: 100%;
    margin-bottom: 20px;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
}

.login-button {
    width: 100%;
    padding: 10px;
    background-color: #328188;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.login-button:hover {
    background-color: #307272;
}
</style>
"""

# Apply custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Login Page
st.title('Medicine Recommendation System - Login')

username = st.text_input('Username')
password = st.text_input('Password', type='password')

if st.button('Login'):
    if username == 'admin' and password == 'password':
        st.success('Logged in successfully!')
        st.write('Please proceed to the recommendation page.')
    else:
        st.error('Invalid username or password. Please try again.')

        # Don't proceed further until valid credentials are provided
        st.stop()

# Recommendation Page
st.title('Medicine Recommendation System')

# Load data
medicines_dict = pickle.load(open('medicine_dict.pkl', 'rb'))
medicines = pd.DataFrame(medicines_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(medicine):
    medicine_index = medicines[medicines['Drug_Name'] == medicine].index[0]
    distances = similarity[medicine_index]
    medicines_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_medicines = []
    for i in medicines_list:
        recommended_medicines.append(medicines.iloc[i[0]].Drug_Name)
    return recommended_medicines

# Recommendation Program
selected_medicine_name = st.selectbox(
    'Type your medicine name whose alternative is to be recommended',
    medicines['Drug_Name'].values)

if st.button('Recommend Medicine'):
    recommendations = recommend(selected_medicine_name)
    j = 1
    for i in recommendations:
        st.write(j, i)  # Recommended-drug-name
        st.write("Click here -> " + "https://pharmeasy.in/search/all?name=" + i)  # Recommended-drug purchase link from pharmeasy
        j += 1

# Image Load
from PIL import Image
image = Image.open('images/Medical.jpeg')
st.image(image, caption='Recommended Medicines')
