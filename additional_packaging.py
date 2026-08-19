import os


def additional_packaging(addon_name: str) -> None:
    build_ui_script = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "scripts", "build_ui.sh"
    )
    if os.path.exists(build_ui_script):
        os.system(f"chmod +x {build_ui_script}")
        return_code = os.system(build_ui_script)
        if return_code != 0:
            os._exit(os.WEXITSTATUS(return_code))
