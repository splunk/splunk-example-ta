from splunk_add_on_ucc_modinput_test.functional.decorators import (
    register_vendor_class,
)
from splunk_add_on_ucc_modinput_test.functional.vendor import VendorClientBase
from tests.ucc_modinput_functional.vendor.client.configuration import (
    Configuration,
)


@register_vendor_class(Configuration)
class VendorClient(VendorClientBase):
    pass
