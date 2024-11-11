ADDON_NAME = "Splunk_TA_Example"


def get_example_collection_key_name(input_name: str) -> str:
    # `input_name` is a string like "example://<input_name>".
    return input_name.split("/")[-1]
