import os
from os import path


def additional_packaging(addon_name: str) -> None:
    # It fixes https://github.com/splunk/splunk-example-ta/actions/runs/11767701819/job/32776693866?pr=2.
    file_to_remove = f"output/{addon_name}/lib/__pycache__/socks.cpython-37.pyc"
    if path.exists(file_to_remove):
        os.remove(file_to_remove)
