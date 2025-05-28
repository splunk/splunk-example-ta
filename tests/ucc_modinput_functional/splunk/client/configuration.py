from splunk_add_on_ucc_modinput_test.common import utils  # noqa
from splunk_add_on_ucc_modinput_test.functional.splunk import (
    SplunkConfigurationBase,
)


class Configuration(SplunkConfigurationBase):
    def customize_configuration(self) -> None:
        # to be implemented
        # self.encoded_prop = utils.get_from_environment_variable(
        #     "ENV_PROP_NAME1", string_function=utils.Base64.decode
        # )
        # self.not_encoded_prop = utils.get_from_environment_variable(
        #     "ENV_PROP_NAME2"
        # )
        pass
