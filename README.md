# Image Upload App with Automated Captioning
This web application allows users to upload images, which are stored in Google Cloud Storage (GCS) and automatically captioned using the Gemini API. The app is deployed on Google Cloud Run for serverless and scalable infrastructure.

## Features
- Upload images and store them in GCS
- Auto-generate captions using Gemini API
- Display images with captions
- Scalable deployment using Cloud Run

## Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/image-upload-app.git
cd image-upload-app
```

2. Setup environment variables in .env file (This can also be done manually in GCP):
```bash
GOOGLE_CLOUD_PROJECT=your-google-cloud-project
GCS_BUCKET_NAME=your-gcs-bucket-name
GEMINI_API_KEY=your-gemini-api-key
```
The Gemini API key can be made in Google Studio: https://aistudio.google.com/app/apikey 

3. In terminal , install dependencies
```bash 
pip install -r requirements.txt
```

 # Usage
- After deployment, access the app via the provided URL.
- Upload images, stored in GCS and captioned using the Gemini API.
- View uploaded images and their auto-generated captions.


# Future Improvements
- improve UI
-  Create a login
-  imbed image into html with appropriate gemini caption
-  For HW3: show different traffic routes (with different backround color for HTML)
           -tRAFFIC SHOULDNT BE SPLIT EVENLY AND 2 VERSIONS SHOULD BE RUNNING IN PARALLEL, DO NOT IMPLEMENT SPLIT LOGIC IN YOU APP
   
