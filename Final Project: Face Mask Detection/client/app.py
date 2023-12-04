import streamlit as st
from datetime import datetime
import requests
import pandas as pd
from PIL import Image

img_file = st.file_uploader("Upload", type="png")
API_URL = "http://localhost:8000/image"

if img_file is not None:
    
    # Rename filename to current timestamp



    img_file.name = "inputs/" + datetime.now().isoformat().replace(":", "_") + ".png"

    ## Upload Image to S3 using presigned URL

    # Get presigned URL
    response = requests.get(API_URL+"/get-s3-upload-url?object_name="+img_file.name)
    if response.status_code != 200:
        st.write("Error getting presigned URL from S3")
        st.stop()
        
    presigned_post = response.json()

    # Upload image to S3
    files = {'file': (img_file.name, img_file)}
    upload_response = requests.post(presigned_post['url'], data=presigned_post['fields'], files=files)

    if upload_response.status_code == 204:
        st.write("Upload successful!")


        # Write image record to database
        image_record = {
            "fileName": img_file.name,
            "predicted": False,
            "is_correct": False
        }

        response = requests.post(API_URL+"/create-image-record", json=image_record)
        if response.status_code == 200:
            st.write("Image record created successfully! Predicting soon...")
        else:
            st.write("Image record creation failed. Please try again.")

    else:
        st.write("Upload failed. Please try again.")
        
    # change img_file to PIL.Image
    #img_file = Image.open(img_file).convert("RGB")

    # current_time = datetime.now() 
    # filename = current_time.isoformat().replace(":", "_")
    # img_file.name = filename

    # Display image
    # st.image(img_file)
    # mask_recognition(img_file)
    # st.image('output.png')