import os
from os import path


def additional_packaging(addon_name: str) -> None:
    # It fixes https://github.com/splunk/splunk-example-ta/actions/runs/11767701819/job/32776693866?pr=2.
    file_to_remove = f"output/{addon_name}/lib/__pycache__/socks.cpython-37.pyc"
    if path.exists(file_to_remove):
        os.remove(file_to_remove)

    build_ui_script = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "scripts", "build_ui.sh"
    )
    if path.exists(build_ui_script):
        os.system(f"chmod +x {build_ui_script}")
        return_code = os.system(build_ui_script)
        if return_code != 0:
            os._exit(os.WEXITSTATUS(return_code))
