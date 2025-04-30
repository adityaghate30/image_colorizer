import streamlit as st
import numpy as np
from PIL import Image
import tempfile
import time
from colorizer import DeepLearningColorizer

# Set page config
st.set_page_config(page_title="Image Colorizer", layout="centered")

st.title("🎨 Black & White Image Colorizer")
st.write("Upload a black & white photo and see it in color using a deep learning model!")

uploaded_file = st.file_uploader("Choose a black & white image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open image
    image = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(image)

    st.image(image, caption="Original B/W Image", use_column_width=True)

    st.write("Colorizing... Please wait.")

    # Create colorizer instance
    colorizer = DeepLearningColorizer()

    # Colorize
    start_time = time.time()
    colorized_img = colorizer.colorize(img_np)
    end_time = time.time()

    st.image(colorized_img, caption="Colorized Image", use_column_width=True)
    st.success(f"Done! Colorization took {end_time - start_time:.2f} seconds.")

    # Optional: allow user to download
    result_image = Image.fromarray(colorized_img)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        result_image.save(tmp.name)
        st.download_button(
            label="📥 Download Colorized Image",
            data=open(tmp.name, "rb").read(),
            file_name="colorized.png",
            mime="image/png"
        )
