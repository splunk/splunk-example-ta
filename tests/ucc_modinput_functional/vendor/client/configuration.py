from typing import Optional
from splunk_add_on_ucc_modinput_test.common import utils
from splunk_add_on_ucc_modinput_test.functional.vendor import (
    VendorConfigurationBase,
)


class Configuration(VendorConfigurationBase):
    def customize_configuration(self) -> None:
        self._api_key = utils.get_from_environment_variable(
            "MODINPUT_TEST_EXAMPLE_API_KEY_BASE64",
            string_function=utils.Base64.decode,
        )

    @property
    def api_key(self) -> Optional[str]:
        return self._api_key
