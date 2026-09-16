# IAM Decisions

## Runtime identity

The Cloud Run service currently uses:

`689643138964-compute@developer.gserviceaccount.com`

This is the project's default Compute Engine service account.

## Cloud Storage access

The runtime service account was granted the bucket-level role:

`roles/storage.objectUser`

This was applied to:

`gs://gbabse-event-image-2026`

The role provides object-level permissions needed by the application to download the source image and upload the processed image.

Using a bucket-level role keeps the storage permission narrower than granting a broad project-level role to the application.

## Eventarc identity

The Eventarc trigger is configured to use the same runtime service account as its service account:

`689643138964-compute@developer.gserviceaccount.com`

The service account was granted the Eventarc event receiver permission required for event delivery. Google-managed service agents also require their platform-specific permissions for Eventarc and Pub/Sub operation.

## Permissions used during setup

The project required Google Cloud APIs for:

- Cloud Run
- Cloud Storage
- Eventarc
- Artifact Registry
- Cloud Build
- Cloud Logging

During Eventarc setup, the required Google-managed service-agent permissions were also configured.

## Current security considerations

The Cloud Run service was deployed with unauthenticated invocation to simplify the initial portfolio exercise. This is suitable for demonstrating the application, but it is not the preferred security model for a production event-processing service.

The current implementation also uses the default Compute Engine service account. Although the bucket permission was restricted to `roles/storage.objectUser`, a dedicated service account would provide clearer separation of duties.

## Production hardening

A production implementation should consider:

1. Create a dedicated service account for the image processor.
2. Grant only the required Cloud Storage object permissions on the required bucket or prefixes where supported by the chosen design.
3. Use authenticated Cloud Run invocation from Eventarc rather than public unauthenticated access.
4. Separate the Eventarc trigger identity from the Cloud Run runtime identity where appropriate.
5. Review IAM periodically and remove permissions that are no longer required.
6. Avoid granting broad project-level roles such as Editor to application runtime identities.
7. Use Terraform or another infrastructure-as-code approach so IAM changes are reviewable and repeatable.

## Portfolio lesson

The important IAM principle demonstrated by this project is **least privilege**: give an application the permissions it needs for its specific task rather than broad project-wide access. The project also documents where the current implementation can be hardened further rather than presenting a development configuration as production-ready.
