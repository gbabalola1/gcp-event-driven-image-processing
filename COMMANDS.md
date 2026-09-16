# Key Commands

These are the main commands used to build, deploy, configure and validate the project.

## Set the GCP project

```bash
gcloud config set project gbabse-event-image-2026
```

## Enable required APIs

```bash
gcloud services enable \
  run.googleapis.com \
  storage.googleapis.com \
  eventarc.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  logging.googleapis.com
```

## Deploy the Cloud Run application

From the application directory:

```bash
gcloud run deploy image-processor \
  --source . \
  --function process_image \
  --base-image python312 \
  --region=europe-west2 \
  --allow-unauthenticated
```

## Grant Cloud Storage object access

```bash
gcloud storage buckets add-iam-policy-binding \
  gs://gbabse-event-image-2026 \
  --member="serviceAccount:689643138964-compute@developer.gserviceaccount.com" \
  --role="roles/storage.objectUser"
```

## Create the Eventarc service identity

```bash
gcloud beta services identity create \
  --service=eventarc.googleapis.com \
  --project=gbabse-event-image-2026
```

## Create the Eventarc trigger

```bash
gcloud eventarc triggers create image-upload-trigger \
  --location=europe-west2 \
  --destination-run-service=image-processor \
  --destination-run-region=europe-west2 \
  --event-filters="type=google.cloud.storage.object.v1.finalized" \
  --event-filters="bucket=gbabse-event-image-2026" \
  --service-account=689643138964-compute@developer.gserviceaccount.com
```

## Upload a test image

```bash
gcloud storage cp test.jpg \
  gs://gbabse-event-image-2026/uploads/test-event.jpg
```

## Check bucket contents

```bash
gcloud storage ls gs://gbabse-event-image-2026/uploads/
gcloud storage ls gs://gbabse-event-image-2026/processed/
```

## Inspect the Eventarc trigger

```bash
gcloud eventarc triggers describe image-upload-trigger \
  --location=europe-west2
```

## View Cloud Run logs

```bash
gcloud run services logs read image-processor \
  --region=europe-west2 \
  --limit=50
```

## Useful validation

A successful test should show:

```text
Image upload event received: bucket=gbabse-event-image-2026 file=uploads/test-event.jpg
Image processed successfully: uploads/test-event.jpg -> processed/test-event.jpg
```

A second event for the processed object should be ignored:

```text
Ignoring file outside uploads/: processed/test-event.jpg
```

## Local Python validation

Syntax check:

```bash
python -m py_compile main.py
```

Import check:

```bash
python -c "import main; print('Application imported successfully')"
```
