import logging
from flask import current_app, flash, Flask, redirect, render_template, request, url_for, send_file
from google.cloud import error_reporting, storage
#from markupsafe import Markup 
import google.cloud.logging
import os
import requests

url = 'https://amarrasproject2.free.beeceptor.com'
headers = {
    'Authorization': 'Bearer SOME-VALUE'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.text)
else:
    print(f"Request failed with status code: {response.status_code}")
    
# Initialize Flask app
app = Flask(__name__)


app.config.update(
    SECRET_KEY='your-secret-key',
    MAX_CONTENT_LENGTH=8 * 1024 * 1024,  # 8 MB max upload size
    ALLOWED_EXTENSIONS=set(['png', 'jpg', 'jpeg', 'gif'])
)

# Initialize Google Cloud Storage and Logging clients
client = google.cloud.logging.Client()
client.setup_logging()

#keep this outside of function
storage_client = storage.Client()

# Get Google Cloud Storage bucket name from environment
BUCKET_NAME = os.environ.get('GOOGLE_STORAGE_BUCKET') or 'imageupload-bucket'


# Google Cloud Storage Upload
def upload_image_file(img):
    """
    Upload the user-uploaded file to Google Cloud Storage 
    """
    if not img:
        return None

    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(img.filename)

    # Upload the file to the bucket
    blob.upload_from_file(img, content_type=img.content_type)

    # Make the blob publicly viewable and return the public URL
    #blob.make_public()
    #public_url = blob.public_url

    #current_app.logger.info(f'Uploaded file {img.filename} to {public_url}')
    return blob.name

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']



# Route to render image upload form and list images
@app.route('/')
def index():
    bucket = storage_client.bucket(BUCKET_NAME)
    blobs = bucket.list_blobs()
    image_urls = [blob.name for blob in blobs]

    return render_template('index.html', images=image_urls)

# Handle image uploads
@app.route('/upload', methods=['POST'])
def upload():
    # Check if the POST request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        # Upload the image to Cloud Storage
        image_url = upload_image_file(file)
        if image_url:
            flash(f'Image uploaded successfully: <a href="{image_url}">{image_url}</a>')
        return redirect(url_for('index'))

    flash('Invalid file type. Please upload PNG, JPG, JPEG, or GIF images.')
    return redirect(request.url)

@app.route('/images/<filename>')
def get_file(filename):
    bucket = storage_client.bucket(BUCKET_NAME)

    blob = bucket.blob(filename)
    blob.download_to_filename(filename)
    return send_file(filename)


# Error reporting
@app.errorhandler(500)
def server_error(e):
    client = error_reporting.Client()
    client.report_exception(http_context=error_reporting.build_flask_context(request))
    return f"An internal error occurred: <pre>{e}</pre>", 500

# Only used when running locally
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


