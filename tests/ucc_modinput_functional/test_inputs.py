import pytest  # noqa F401
from splunk_add_on_ucc_modinput_test.common import utils
from splunk_add_on_ucc_modinput_test.functional.decorators import (
    bootstrap,
    forge,
    forges,
)
from tests.ucc_modinput_functional.splunk.forges import (
    set_loglevel,
    account,
    another_account,
    account_input,
)
from tests.ucc_modinput_functional.splunk.probes import (
    wait_for_loglevel,
    account_input_events_ingested,
)
from tests.ucc_modinput_functional.splunk.client import SplunkClient
from tests.ucc_modinput_functional import defaults
import logging

logger = logging.getLogger("ucc-modinput-test")


@bootstrap(
    forge(
        set_loglevel,
        loglevel=defaults.TA_LOG_LEVEL_FOR_TESTS,
        probe=wait_for_loglevel,
    ),  # sequence matters - ta_logging will be executed before accounts
    forges(
        forge(account),
        forge(another_account),
    ),
    forges(
        forge(
            account_input,
            probe=account_input_events_ingested,
        ),
        # forge(
        #     another_account_base_input,
        #     # probe=probes.event_log_input_oauth_hourly_events_ingested,
        # ),
    ),
)
def test_inputs(splunk_client: SplunkClient, example_input_spl: str) -> None:
    search_result_details = splunk_client.search(searchquery=example_input_spl)
    assert (
        search_result_details.result_count != 0
    ), f"Following query returned 0 events: {example_input_spl}"

    logger.info(
        "test_inputs_loginhistory_clone done at "
        + utils.convert_to_utc(utils.get_epoch_timestamp())
    )
