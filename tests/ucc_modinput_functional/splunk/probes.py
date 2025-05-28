import time
from typing import Generator, Dict, Optional
from tests.ucc_modinput_functional.splunk.client import SplunkClient
from tests.ucc_modinput_functional.defaults import (
    PROBE_PROXY_CHECK_INTERVAL,
    PROBE_PROXY_CHECK_TIMEOUT,
    PROBE_LOGLEVEL_CHECK_INTERVAL,
    PROBE_LOGLEVEL_CHECK_TIMEOUT,
)
from splunk_add_on_ucc_modinput_test.common import utils
import logging

logger = logging.getLogger("ucc-modinput-test")


def same_proxy_configs(
    proxy1: Dict[str, object],
    proxy2: Dict[str, object],
    ignore_password: bool = True,
) -> bool:
    """
    Compare two proxy configurations, ignoring properties that are not
    configured (None).

    By default, the comparison ignores the 'proxy_password' property as it
    is returned sanitized by the API.

    Args:
        proxy1 (Dict[str, object]): The first proxy configuration to compare.
        proxy2 (Dict[str, object]): The second proxy configuration to compare.
        ignore_password (bool, optional): Whether to ignore 'proxy_password'
            property in the comparison. Defaults to True.

    Returns:
        bool: True if the proxy configurations are the same, otherwise False.
    """

    proxy1 = {k: v for k, v in proxy1.items() if v is not None}
    proxy2 = {k: v for k, v in proxy2.items() if v is not None}
    if ignore_password:
        proxy1.pop("proxy_password", None)
        proxy2.pop("proxy_password", None)

    res = proxy1 == proxy2
    logger.debug(f"same_proxy_configs: {res}\n\tproxy1: {proxy1}\n\tproxy2: {proxy2}")

    return res


def wait_for_proxy(
    splunk_client: SplunkClient,
    expected_proxy: Dict[str, object],
    error: Optional[str] = None,
) -> Generator[int, None, bool]:
    """
    Waits for the Splunk proxy configuration to match the expected value.

    This function repeatedly checks the Splunk proxy configuration until it
    matches the expected value provided in the `expected_proxy` argument or
    until the timeout expires. If the `error` argument is not None, the
    function returns immediately with a status of False.

    Args:
        splunk_client (SplunkClient): The Splunk client to use for checking
            the proxy settings.
        expected_proxy (Dict[str, object]): The expected proxy configuration
            to match against.
        error (Optional[str]): An error message indicating that the proxy
            setting API call failed. If not None, the function returns False.

    Yields:
        int: The interval in seconds after which the probe should be invoked
            again if the verification was not successful.

    Returns:
        bool: True if the proxy configuration matches the expected value
            within the timeout period, False otherwise.
    """

    if error is not None:
        return False

    start = time.time()
    expire = time.time() + PROBE_PROXY_CHECK_TIMEOUT
    while time.time() < expire:
        proxy = splunk_client.get_settings_proxy()
        if same_proxy_configs(expected_proxy, proxy):
            logger.debug(
                f"probe wait_for_proxy successful after {time.time() - start} "
                "seconds"
            )
            return True
        logger.debug(f"probe wait_for_proxy failed after {time.time() - start} seconds")
        yield PROBE_PROXY_CHECK_INTERVAL

    logger.debug(
        "probe wait_for_proxy expired with failed status after "
        f"{time.time() - start} seconds"
    )

    return False


def wait_for_loglevel(
    splunk_client: SplunkClient,
    expected_loglevel: str,
    error: Optional[str] = None,
) -> Generator[int, None, bool]:
    """
    Probe generator method that repeatedly checks TA log level configuration
    until it matches the expected_loglevel or the probe time expires.

    Args:
        splunk_client (SplunkClient): The Splunk client instance.
        expected_loglevel (str): The expected log level to wait for.
        error (Optional[str], optional): Error message if the API call setting
            log level failed. Defaults to None.

    Yields:
        int: Interval after which the probe should be invoked again if the
            verification was not successful.

    Returns:
        bool: True if the log level matches expected value, False otherwise.
    """
    if error is not None:
        return False

    start = time.time()
    expire = start + PROBE_LOGLEVEL_CHECK_TIMEOUT
    while time.time() < expire:
        loglevel = splunk_client.get_settings_logging().get("loglevel")
        if loglevel == expected_loglevel:
            logger.debug(
                "probe wait_for_loglevel successful after "
                f"{time.time() - start} seconds"
            )
            return True
        logger.debug(
            f"probe wait_for_loglevel failed after {time.time() - start} " "seconds"
        )
        yield PROBE_LOGLEVEL_CHECK_INTERVAL

    logger.debug(
        "probe wait_for_loglevel expired with failed status after "
        f"{time.time() - start} seconds"
    )
    return False


def events_ingested(
    splunk_client: SplunkClient, probe_spl: str, probes_wait_time: int = 10
) -> Generator[int, None, None]:
    start_time = utils.get_epoch_timestamp()
    utils.logger.debug(f"started at {start_time}")
    utils.logger.debug(probe_spl)
    while True:
        search = splunk_client.search(searchquery=probe_spl)
        if search.result_count != 0:
            break
        utils.logger.debug(
            f"failed, let's wait another {probes_wait_time} \
                seconds and try again"
        )
        yield probes_wait_time

    utils.logger.debug(
        "successfully finished after "
        f"{utils.get_epoch_timestamp()-start_time} seconds"
    )


def account_input_events_ingested(
    splunk_client: SplunkClient, example_input_spl: str
) -> Generator[int, None, None]:
    yield from events_ingested(splunk_client, example_input_spl)
