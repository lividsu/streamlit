import streamlit as st
from streamlit_lottie import st_lottie
import requests
import numpy as np
import cv2
from PIL import Image, ImageEnhance


st.set_page_config(page_title="photo editor", page_icon=":squid:", layout="wide")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()



image = Image.open(r'PETLIBRO_LOGO_16-9.png')

col1, col2 = st.columns([0.8, 0.2])
with col1:               # To display the header text using css style
    st.markdown(""" 
    <style> .font {
    font-size:35px ; font-family: 'Gill Sans'; color: #00416B;} 
    </style> 
    """, unsafe_allow_html=True)
    st.markdown('<p class="font">Upload your photo here...</p>', unsafe_allow_html=True)
    
with col2:               # To display brand logo
    st.image(image,  width=150)

st.sidebar.markdown('<p class="font"> My First Photo Converter App</p>', unsafe_allow_html=True)

with st.sidebar.expander("About the App"):
    st.write("""
        Use this simple app to convert your favorite photo to a pencil sketch, a grayscale image or an image with blurring effect. \n \n For Petlibro.
        """
    )

uploaded_file = st.file_uploader("", type=['jpg', 'png', 'jpeg'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    col1, col2 = st.columns([0.5, 0.5])
    with col1:
        st.markdown('<p style="text-align: center;">Before</p>', unsafe_allow_html=True)
        st.image(image, width=300)
    with col2:
        st.markdown('<p style="text-align: center;">After</p>',unsafe_allow_html=True)
        filter = st.sidebar.radio('Covert your photo to:', ['Original','Gray Image','Black and White', 'Pencil Sketch', 'Blur Effect'])
        if filter == 'Gray Image':
                converted_img = np.array(image.convert('RGB'))
                gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
                st.image(gray_scale, width=300)
        elif filter == 'Black and White':
                converted_img = np.array(image.convert('RGB'))
                gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
                slider = st.sidebar.slider('Adjust the intensity', 1, 255, 127, step=1)
                (thresh, blackAndWhiteImage) = cv2.threshold(gray_scale, slider, 255, cv2.THRESH_BINARY)
                st.image(blackAndWhiteImage, width=300)
        elif filter == 'Pencil Sketch':
                converted_img = np.array(image.convert('RGB')) 
                gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
                inv_gray = 255 - gray_scale
                slider = st.sidebar.slider('Adjust the intensity', 25, 255, 125, step=2)
                blur_image = cv2.GaussianBlur(inv_gray, (slider,slider), 0, 0)
                sketch = cv2.divide(gray_scale, 255 - blur_image, scale=256)
                st.image(sketch, width=300) 
        elif filter == 'Blur Effect':
                converted_img = np.array(image.convert('RGB'))
                slider = st.sidebar.slider('Adjust the intensity', 5, 81, 33, step=2)
                converted_img = cv2.cvtColor(converted_img, cv2.COLOR_RGB2BGR)
                blur_image = cv2.GaussianBlur(converted_img, (slider,slider), 0, 0)
                st.image(blur_image, channels='BGR', width=300) 
        else: 
                st.image(image, width=300)


#Add a feedback section in the sidebar
st.sidebar.title(' ') #Used to create some space between the filter widget and the comments section
st.sidebar.markdown(' ') #Used to create some space between the filter widget and the comments section
st.sidebar.subheader('Please help us improve!')
with st.sidebar.form(key='columns_in_form',clear_on_submit=True): #set clear_on_submit=True so that the form will be reset/cleared once it's submitted
    rating=st.slider("Please rate the app", min_value=1, max_value=5, value=3,help='Drag the slider to rate the app. This is a 1-5 rating scale where 5 is the highest rating')
    text=st.text_input(label='Please leave your feedback here')
    submitted = st.form_submit_button('Submit')
    if submitted:
      st.write('Thanks for your feedback!')
      st.markdown('Your Rating:')
      st.markdown(rating)
      st.markdown('Your Feedback:')
      st.markdown(text)