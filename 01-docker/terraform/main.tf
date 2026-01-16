terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.16.0"
    }
  }
}

provider "google" {
  project = "daring-pier-447713-j0"
  region  = "us-central1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "demo-daring-pier-20260115"
  location      = "US"
  storage_class = "STANDARD"

  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_storage_bucket_object" "default" {
  name         = "test-object"
  source       = "/workspaces/data-engineering-zoomcamp/01-docker/test/file1.txt"
  content_type = "text/plain"
  bucket       = google_storage_bucket.demo-bucket.id
}

resource "google_bigquery_dataset" "demo-dataset" {
  dataset_id = "demo_daring_pier_dataset"
}