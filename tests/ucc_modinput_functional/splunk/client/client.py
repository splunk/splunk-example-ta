from splunk_add_on_ucc_modinput_test.functional.decorators import (
    register_splunk_class,
)
from tests.ucc_modinput_functional.splunk.client.configuration import (
    Configuration,
)
from tests.ucc_modinput_functional.splunk.client._managed_client import (
    ManagedSplunkClient,
    SplunkApiError,
)
import swagger_client


@register_splunk_class(swagger_client, Configuration)
class SplunkClient(ManagedSplunkClient):
    # here you can add your custom Splunk client extension code
    pass
