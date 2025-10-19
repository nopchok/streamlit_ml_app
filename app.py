import streamlit as st
import pandas as pd
import os
import zipfile
import requests
import shutil

st.title("📦 Kaggle Dataset Loader")

# User input for Kaggle URL
url = st.text_input("Enter Kaggle dataset download URL (API format):")

if st.button("Download and Load Dataset"):
    if url:
        try:
            zip_path = "dataset.zip"
            extract_path = "dataset"

            # 🧹 Step 0: Clean up old folder if exists
            if os.path.exists(extract_path):
                shutil.rmtree(extract_path)

            # Step 1: Download file
            st.info("📥 Downloading dataset...")
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, stream=True)
            with open(zip_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

            # Step 2: Unzip
            st.info("📂 Extracting files...")
            os.makedirs(extract_path, exist_ok=True)
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_path)

            # Step 3: Find and read CSV file
            csv_files = [f for f in os.listdir(extract_path) if f.endswith(".csv")]
            if not csv_files:
                st.error("No CSV file found in the dataset.")
            else:
                file_path = os.path.join(extract_path, csv_files[0])
                df = pd.read_csv(file_path, header=None)
                st.success("✅ Dataset loaded successfully!")
                st.write("### Preview (first 100 rows):")
                st.dataframe(df.head(100))


            # Optional cleanup: delete zip file
            os.remove(zip_path)

        except Exception as e:
            st.error(f"⚠️ Error: {e}")
    else:
        st.warning("Please enter a valid Kaggle dataset URL.")
