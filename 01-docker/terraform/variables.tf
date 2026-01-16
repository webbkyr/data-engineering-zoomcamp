variable "project" {
  default     = "daring-pier-447713-j0"
  description = "Project"
}

variable "location" {
  default     = "US"
  description = "Project location"
}

variable "bg_dataset_name" {
  default     = "demo_daring_pier_dataset"
  description = "My BigQuery dataset name"
}

variable "gcs_bucket_name" {
  default     = "demo-daring-pier-20260115"
  description = "Storage bucket name"
}


variable "gcs_storage_class" {
  default     = "STANDARD"
  description = "Bucket storage class"
}
