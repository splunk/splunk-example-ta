import import_declare_test

from splunktaucclib.rest_handler.admin_external import AdminExternalHandler
from splunktaucclib.rest_handler.error import RestError


def _validate_api_key(api_key: str):
    # Some code to validate the API key.
    # Should return nothing if the configuration is valid.
    # Should raise an exception splunktaucclib.rest_handler.error.RestError if the configuration is not valid.
    if api_key != "super-secret-api-token":
        raise RestError(400, "API Key provided is not correct!")


class APIKeyValidator(AdminExternalHandler):
    def __init__(self, *args, **kwargs):
        AdminExternalHandler.__init__(self, *args, **kwargs)

    def handleList(self, confInfo):
        AdminExternalHandler.handleList(self, confInfo)

    def handleEdit(self, confInfo):
        _validate_api_key(
            self.payload.get("api_key"),
        )
        AdminExternalHandler.handleEdit(self, confInfo)

    def handleCreate(self, confInfo):
        _validate_api_key(
            self.payload.get("api_key"),
        )
        AdminExternalHandler.handleCreate(self, confInfo)

    def handleRemove(self, confInfo):
        AdminExternalHandler.handleRemove(self, confInfo)
