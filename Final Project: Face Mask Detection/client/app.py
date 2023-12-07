from time import sleep
import streamlit as st
from datetime import datetime
import requests
import pandas as pd
from PIL import Image

API_URL = "http://localhost:8000/image"

def update_image_record(image_record, is_correct):
    image_record["is_correct"] = is_correct
    requests.put(API_URL+"/update-image-record", json=image_record)
        

st.title("Face Mask Detection!")
img_file = st.file_uploader("Upload", type="png")
if img_file is not None:
    
    # Rename filename to current timestamp
    img_file.name = datetime.now().isoformat().replace(":", "_") + ".png"

    ## Upload Image to S3 using presigned URL

    # Get presigned URL
    response = requests.get(API_URL+"/get-s3-upload-url?object_name="+ "inputs/" + img_file.name)
    if response.status_code != 200:
        st.write("Error getting presigned URL from S3")
        st.stop()
        
    presigned_post = response.json()

    # Upload image to S3
    files = {'file': (  "inputs/" + img_file.name, img_file)}
    upload_response = requests.post(presigned_post['url'], data=presigned_post['fields'], files=files)

    if upload_response.status_code == 204:
        st.write("Upload successful!")


        # Write image record to database
        image_record = {
            "fileName": img_file.name,
            "predicted": False,
            "is_correct": False
        }

        #Create Image Record & make Prediction
        response = requests.post(API_URL+"/create-image-record", json=image_record)
        if response.status_code == 200 :
            st.write("Image record created successfully!")

            # Make prediction
            task_id = requests.post(API_URL+"/make-prediction", json=image_record).json()

            #  Exponential backoff on fetching prediction result
            max_retries = 5
            retries = 0

            while retries < max_retries:
                retries += 1
                response = requests.get(API_URL+"/get-prediction-result?fileName="+img_file.name + "&task_id=" + task_id)
                if response.status_code == 200:
                    result_info = response.json()
                    if result_info["done"]:
                        st.write("Prediction result ready!")
                        st.image(result_info["result_image_url"])
                        break
                sleep(2**retries)

        else:
            st.write("Image record creation failed. Please try again.")

    else:
        st.write("Upload failed. Please try again.")