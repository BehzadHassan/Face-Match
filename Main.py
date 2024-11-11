import glob
import tempfile
from FaceNetMatch import MatchFaces
import streamlit as st
from PIL import Image
import os

# Set page config
st.set_page_config(page_title="AI Face Match", page_icon="🧑‍🦳", layout="wide")

# Header
st.title("AI Face Match")
st.subheader("Match faces from your directory with the uploaded query image.")

# ---- Sidebar ----
st.sidebar.title("Upload & Configure")
st.sidebar.write("Upload your query image and specify the directory containing the images to compare against.")
query_img_path = st.sidebar.file_uploader("Upload Query Image", type=["jpg", "png"])
image_dir = st.sidebar.text_input("Enter Directory Path for Images")
start_button = st.sidebar.button("Start Matching")


# Helper Function to display matched images in a grid
def display_images_in_grid(image_paths):
    num_images = len(image_paths)

    if num_images == 0:
        st.warning("No images found in the provided list.")
        return

    # Set number of columns
    num_columns = min(4, num_images)
    num_rows = (num_images + num_columns - 1) // num_columns  # Ceiling division

    # Create a grid layout for the images
    for row in range(num_rows):
        cols = st.columns(num_columns)
        for col in range(num_columns):
            index = row * num_columns + col
            if index < num_images:
                img_path = image_paths[index]
                if os.path.exists(img_path):  # Check if the image file exists
                    img = Image.open(img_path)
                    img = img.resize((200, 200))  # Resize images for consistency
                    with cols[col]:
                        st.image(img, caption=os.path.basename(img_path), use_container_width=True)
                else:
                    with cols[col]:
                        st.warning(f"Image not found: {img_path}")


# Function to display the query image and matched images
def display_images(query_img_path, image_dir):
    query_image = Image.open(query_img_path)

    # Get all image files in the directory
    image_files = glob.glob(os.path.join(image_dir, "*.jpg")) + glob.glob(os.path.join(image_dir, "*.png"))

    query_image = query_image.resize((400, 400))  # Resize query image for consistency
    col1, col2 = st.columns(2)

    # Display query image
    with col1:
        st.image(query_image, caption="Query Image", use_container_width=True)

    matched = []
    with col2:
        placeholder = st.empty()  # Placeholder for images from the directory

        # Loop through images in the directory and match faces
        for image_file in image_files:
            img = Image.open(image_file)
            img = img.resize((400, 400))  # Resize images to match the query image size

            placeholder.image(img, caption=os.path.basename(image_file), use_container_width=True)

            # If a match is found, add to the matched list
            if MatchFaces(query_img_path, image_file):
                matched.append(image_file)

    # Display matched faces
    st.subheader("Matched Faces")
    if matched:
        display_images_in_grid(matched)
    else:
        st.warning("No matches found. Try uploading a different image or using a better quality image.")


# Main logic for handling the Streamlit UI
if query_img_path and image_dir and start_button:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
        query_img_path_temp = temp_file.name
        query_img = Image.open(query_img_path)
        query_img.save(query_img_path_temp)

    display_images(query_img_path_temp, image_dir)

else:
    st.sidebar.warning("Please upload a query image and provide a directory path containing images.")
