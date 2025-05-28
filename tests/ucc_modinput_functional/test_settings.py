import pytest
from typing import Dict, Tuple
from splunk_add_on_ucc_modinput_test.functional.decorators import (
    attach,
    forge,
)
from tests.ucc_modinput_functional.splunk.client import SplunkClient
from tests.ucc_modinput_functional.splunk.forges import (
    set_loglevel,
    try_to_configure_proxy,
)
from tests.ucc_modinput_functional.splunk.probes import (
    wait_for_loglevel,
)


@attach(forge(set_loglevel, probe=wait_for_loglevel, loglevel="CRITICAL"))
def test_valid_loglevel(splunk_client: SplunkClient, wait_for_loglevel: bool) -> None:
    assert wait_for_loglevel is True


@pytest.mark.parametrize(
    "overwrite,expected_error",
    [
        ({"proxy_url": "@#$%!*123"}, "Not matching the pattern: "),
        (
            {"proxy_port": "not-a-number"},
            "Bad Request -- Invalid format for integer value",
        ),
    ],
)
@attach(forge(try_to_configure_proxy))
def test_proxy_validators__invalid_params(
    error: str,
    overwrite: Tuple[Dict[str, str], str],
    expected_error: str,
) -> None:
    assert expected_error in error
