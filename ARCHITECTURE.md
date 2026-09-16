# Architecture

## Overview

This project implements a simple event-driven image-processing pipeline on Google Cloud.

```text
                    Object finalized
User ──upload──> Cloud Storage ─────────> Eventarc
                    uploads/                |
                                            v
                                      Cloud Run
                                   image-processor
                                            |
                                     Resize image
                                            |
                                            v
                                  Cloud Storage
                                   processed/
                                            |
                                            v
                                      Cloud Logging
```

## Event flow

1. A user or application uploads an image to `gs://gbabse-event-image-2026/uploads/`.
2. Cloud Storage emits an object-finalized event.
3. Eventarc receives the event and routes it to the `image-processor` Cloud Run service.
4. Cloud Run reads the event and extracts the bucket and object name.
5. The application checks that the object is inside `uploads/`.
6. The image is downloaded from Cloud Storage.
7. Pillow resizes the image so that its dimensions fit within 800 x 800 pixels while preserving aspect ratio.
8. The processed image is written to the `processed/` prefix.
9. Cloud Logging records the event and processing result.

## Event-loop protection

The same bucket contains both source and processed objects. Cloud Storage therefore produces an event when the processed object is created as well.

The application prevents reprocessing with:

```python
if not file_name.startswith("uploads/"):
    logging.info("Ignoring file outside uploads/: %s", file_name)
    return
```

This means an object such as `processed/test-event.jpg` is ignored rather than processed again.

## Why these services?

### Cloud Storage

Provides durable object storage for incoming and processed images. A folder-like prefix is used to separate source and output objects.

### Eventarc

Provides event routing without requiring a polling application. The trigger listens for `google.cloud.storage.object.v1.finalized` events for the project bucket.

### Cloud Run

Runs the Python image processor as a managed, serverless container. The service can scale based on incoming requests without managing virtual machines.

### Cloud Logging

Provides visibility into request handling, event receipt, successful processing and ignored objects.

## Trigger configuration

Trigger name: `image-upload-trigger`

Location: `europe-west2`

Destination: Cloud Run service `image-processor`

Event type: `google.cloud.storage.object.v1.finalized`

Bucket filter: `gbabse-event-image-2026`

## Design considerations

This is intentionally a small portfolio project. A production system could add authenticated invocation, a dedicated runtime service account, validation for file type and size, retry/dead-letter handling, monitoring and alerting, structured logging, and infrastructure-as-code with Terraform.
