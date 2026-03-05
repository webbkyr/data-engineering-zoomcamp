import dlt
from dlt.sources.rest_api import RESTAPIConfig, rest_api_resources


@dlt.source
def nyc_taxi_source(page_size: int = 1000):
    """
    REST API source for NYC taxi data using dlt's generic REST API source.

    The API returns a simple JSON array and supports page-number pagination.
    Pagination stops automatically when an empty page ([]) is returned.
    """
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api",
            "paginator": {
                "type": "page_number",
                "page_param": "page",
                "base_page": 1,
                # The API does not return a total page count; stop on empty page.
                "total_path": None,
                "stop_after_empty_page": True,
            },
        },
        "resources": [
            {
                "name": "nyc_taxi_trips",
                "endpoint": {
                    "path": "",
                    "data_selector": "$",
                    "params": {"limit": page_size},
                },
            }
        ],
    }

    # Yield dlt resources constructed from the declarative configuration.
    yield from rest_api_resources(config)


def run() -> None:
    """
    Run the NYC taxi REST API pipeline.
    """
    pipeline = dlt.pipeline(
        pipeline_name="taxi_pipeline",
        destination="duckdb",
        dataset_name="nyc_taxi_data",
        progress="log",
    )

    load_info = pipeline.run(nyc_taxi_source())
    print(load_info)


if __name__ == "__main__":
    run()
