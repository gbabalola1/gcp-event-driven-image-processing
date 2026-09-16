import logging
from io import BytesIO

import functions_framework
from google.cloud import storage
from PIL import Image

logging.basicConfig(level=logging.INFO)
storage_client = storage.Client()


@functions_framework.cloud_event
def process_image(cloud_event):
    data = cloud_event.data

    bucket_name = data["bucket"]
    file_name = data["name"]

    logging.info(
        "Image upload event received: bucket=%s file=%s",
        bucket_name,
        file_name,
    )

    # Only process source images. This prevents an event loop when the
    # processed object is written back to the same bucket.
    if not file_name.startswith("uploads/"):
        logging.info("Ignoring file outside uploads/: %s", file_name)
        return

    bucket = storage_client.bucket(bucket_name)
    source_blob = bucket.blob(file_name)
    image_bytes = source_blob.download_as_bytes()

    image = Image.open(BytesIO(image_bytes))
    image.thumbnail((800, 800))

    output = BytesIO()
    image.save(output, format=image.format)
    output.seek(0)

    processed_name = file_name.replace("uploads/", "processed/", 1)
    processed_blob = bucket.blob(processed_name)
    processed_blob.upload_from_file(
        output,
        content_type=source_blob.content_type,
    )

    logging.info(
        "Image processed successfully: %s -> %s",
        file_name,
        processed_name,
    )
