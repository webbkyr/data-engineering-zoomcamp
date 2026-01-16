terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.16.0"
    }
  }
}

provider "google" {
  project = var.project
  region  = "us-central1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  storage_class = var.gcs_storage_class

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
  dataset_id = var.bg_dataset_name
}
