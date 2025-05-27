import streamlit as st
import pandas as pd
import cv2
import numpy as np
from streamlit_image_coordinates import streamlit_image_coordinates

# Load color dataset
@st.cache_data
def load_colors():
    return pd.read_csv("colors.csv")

df = load_colors()

def get_color_name(R, G, B):
    min_dist = float('inf')
    closest_name = "Unknown"
    for _, row in df.iterrows():
        d = np.sqrt((R - row["R"])**2 + (G - row["G"])**2 + (B - row["B"])**2)
        if d < min_dist:
            min_dist = d
            closest_name = row["color_name"]
    return closest_name

st.title("🎨 Click2Color – Click on the image, Get the color!")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Resize for display
    img_resized = cv2.resize(img, (600, 400))

    # This line both shows image and returns coords
    coords = streamlit_image_coordinates(img_resized, key="hover")

    # Do NOT use st.image again here

    if coords is not None:
        x, y = int(coords["x"]), int(coords["y"])
        if 0 <= x < img_resized.shape[1] and 0 <= y < img_resized.shape[0]:
            R, G, B = img_resized[y, x]
            color_name = get_color_name(R, G, B)

            st.markdown(f"### 🎯 Hovered Pixel cordinates ({x}, {y})")
            st.markdown(f"**Color Name:** `{color_name}`")
            st.markdown(f"**RGB Value:** ({R}, {G}, {B})")
            st.markdown(
                f'<div style="width:120px;height:60px;background-color:rgb({R},{G},{B});border:2px solid #000;border-radius:5px;"></div>',
                unsafe_allow_html=True
            )
