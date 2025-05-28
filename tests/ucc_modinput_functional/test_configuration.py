import pytest  # noqa F401

from splunk_add_on_ucc_modinput_test.functional.decorators import (
    bootstrap,
    forge,
    forges,
)
from tests.ucc_modinput_functional.splunk.client import SplunkClient
from tests.ucc_modinput_functional.splunk.forges import (
    set_loglevel,
    account,
    another_account,
    another_account_index,
)
from tests.ucc_modinput_functional.splunk.probes import (
    wait_for_loglevel,
)
from tests.ucc_modinput_functional import defaults


@bootstrap(
    # each forge will be executed just once,
    # no matter how many times appears in tests
    forge(
        set_loglevel,
        loglevel=defaults.TA_LOG_LEVEL_FOR_TESTS,
        probe=wait_for_loglevel,
    )
)
def test_ta_logging(splunk_client: SplunkClient) -> None:
    assert (
        splunk_client.get_settings_logging()["loglevel"]
        == defaults.TA_LOG_LEVEL_FOR_TESTS
    )


@bootstrap(
    forge(
        set_loglevel,
        loglevel=defaults.TA_LOG_LEVEL_FOR_TESTS,
        probe=wait_for_loglevel,
    ),  # sequence matters - ta_logging will be executed before accounts
    forges(  # there is parallel execution within forges
        forge(account),
        forge(another_account),
    ),
)
def test_accounts(
    splunk_client: SplunkClient,
    # vendor_client,    # you may want to refer to it in most real-life cases
    account_config_name: str,
    another_account_config_name: str,
) -> None:
    actual_account = splunk_client.get_account(account_config_name)
    assert actual_account is not None
    assert actual_account["api_key"] == defaults.ENCRYPTED_VALUE

    actual_another_account = splunk_client.get_account(another_account_config_name)
    assert actual_another_account is not None
    assert actual_another_account["api_key"] == defaults.ENCRYPTED_VALUE


@bootstrap(
    forge(
        set_loglevel,
        loglevel=defaults.TA_LOG_LEVEL_FOR_TESTS,
        probe=wait_for_loglevel,
    ),  # sequence matters - ta_logging will be executed before accounts
    forges(
        forge(another_account_index),
        # the test framework creates session specific index that can be used
        # if more indexes are needed, they can be created as well
    ),
)
def test_indexes(splunk_client: SplunkClient, another_account_index_name: str) -> None:
    splk_config = splunk_client.splunk_configuration
    actual_index = splk_config.get_index(
        another_account_index_name, client_service=splk_config.service
    )
    assert actual_index is not None
    assert actual_index.name == another_account_index_name
