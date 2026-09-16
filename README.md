# GCP Event-Driven Image Processing

A hands-on Google Cloud project demonstrating an event-driven image-processing pipeline using Cloud Storage, Eventarc, Cloud Run, Python, Pillow, IAM and Cloud Logging.

## Architecture

```text
User
  |
  v
Cloud Storage (uploads/)
  |
  | Object finalized event
  v
Eventarc
  |
  v
Cloud Run: image-processor
  |
  | Resize image
  v
Cloud Storage (processed/)
  |
  v
Cloud Logging
```

## What the project does

When an image is uploaded to the `uploads/` folder of the Cloud Storage bucket, Eventarc detects the object-created event and invokes the Cloud Run service. The service downloads the image, resizes it to fit within 800 x 800 pixels, and writes the processed image to the `processed/` folder.

The application ignores objects outside `uploads/`. This prevents the processed output from causing an endless processing loop.

## Google Cloud services

- Cloud Storage: source and processed image storage
- Eventarc: event routing from Cloud Storage to Cloud Run
- Cloud Run: serverless image-processing application
- Artifact Registry / Cloud Build: container build and deployment support
- Cloud Logging: application and request logs
- IAM: service identity and least-privilege bucket access

## Project details

- GCP project: `GBABSE Event Image Processing`
- Project ID: `gbabse-event-image-2026`
- Region: `europe-west2`
- Bucket: `gs://gbabse-event-image-2026`
- Cloud Run service: `image-processor`
- Eventarc trigger: `image-upload-trigger`

## Application

The Cloud Run application is a Python CloudEvent handler using:

- `functions-framework`
- `google-cloud-storage`
- `Pillow`

The main handler receives a Cloud Storage finalized event, validates the object path, downloads the image, resizes it while preserving its aspect ratio, and uploads the result.

## IAM decisions

The Cloud Run runtime uses the project compute service account:

`689643138964-compute@developer.gserviceaccount.com`

Bucket access was granted with:

`roles/storage.objectUser`

This allows the service to work with objects in the bucket without granting it broader project-level permissions.

The Eventarc trigger also uses this service account. Eventarc-related service agents require Google-managed permissions to deliver events.

For a production implementation, a dedicated Cloud Run runtime service account and a dedicated Eventarc invocation identity would be preferable to the default compute service account. Public unauthenticated Cloud Run access should also be replaced with authenticated event delivery where appropriate.

See [IAM.md](IAM.md) for details.

## Validation

The pipeline was tested by uploading:

`uploads/test-event.jpg`

The expected output was created:

`processed/test-event.jpg`

Cloud Run logs confirmed both the event receipt and successful processing. A subsequent event for the processed object was ignored because it was outside the `uploads/` path.

## Key skills demonstrated

- Event-driven architecture
- Google Cloud Storage
- Eventarc
- Cloud Run
- Python and CloudEvents
- Image processing with Pillow
- IAM and service accounts
- Cloud Logging
- GCP CLI (`gcloud`)
- Troubleshooting and validation

## Documentation

- [Architecture](ARCHITECTURE.md)
- [IAM decisions](IAM.md)
- [Key commands](COMMANDS.md)
