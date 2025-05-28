from typing import Dict, Generator, List
from tests.ucc_modinput_functional import defaults
from tests.ucc_modinput_functional.splunk.client import (
    SplunkClient,
    SplunkApiError,
)
from tests.ucc_modinput_functional.vendor.client import VendorClient
from splunk_add_on_ucc_modinput_test.common import utils


def try_to_set_loglevel(
    splunk_client: SplunkClient, loglevel: str
) -> Generator[Dict[str, object], None, None]:
    """
    Forge method that tries to configure TA log level using an incorrect
    unsupported log level value. The goal is to collect the error message
    provided by the TA and pass it to the corresponding test method for
    validation. Forges pass values to tests, probes, and forges by storing
    key-value pairs in the test artifactory, achieved by yielding key-value
    pairs in the form of a dictionary. In addition to the error message,
    the forge yields the expected log level value used by a probe to ensure
    the desired log level value was indeed applied to the TA's configuration.

    Args:
        splunk_client (SplunkClient): The Splunk client instance.
        loglevel (str): The log level to set.

    Yields:
        Dict[str, object]: A dictionary containing the expected log level
        and any error message encountered.
    """
    error = None
    old_loglevel = splunk_client.get_settings_logging().get("loglevel")
    assert (
        old_loglevel != loglevel
    ), f"Invalid initial conditions: loglevel is already set to {loglevel}"

    try:
        splunk_client.update_settings_logging(loglevel)
    except ValueError as e:
        error = str(e)

    yield dict(expected_loglevel=loglevel, error=error)

    # teardown
    if error is None:
        splunk_client.update_settings_logging(old_loglevel)


def set_loglevel(
    splunk_client: SplunkClient, loglevel: str
) -> Generator[Dict[str, object], None, None]:
    """
    Forge method that configures TA log level and passes it to the
    artifactory to be used by a probe to ensure the desired loglevel
    value is applied to TA's configuration.

    This method does not catch and pass any error messages. Instead,
    API exceptions cause a forge crash handled by the framework and
    turned into a corresponding test fast fail.

    Args:
        splunk_client (SplunkClient): The Splunk client instance.
        loglevel (str): The desired log level to set.

    Yields:
        Dict[str, object]: A dictionary containing the expected log level.

    Teardown:
        Resets the log level to its original value after the test.
    """
    old_loglevel = splunk_client.get_settings_logging().get("loglevel")

    splunk_client.update_settings_logging(loglevel)

    yield dict(
        expected_loglevel=loglevel,
    )

    # teardown
    splunk_client.update_settings_logging(old_loglevel)


def try_to_configure_proxy(
    splunk_client: SplunkClient,
    exclude: List[str] = [],
    overwrite: Dict[str, object] = {},
) -> Generator[Dict[str, object], None, None]:
    """
    Forge method that tries to configure TA proxy using incorrect/unsupported
    proxy configuration.

    Default proxy_config contains values that should pass API endpoint
    validation. However, the exclude and overwrite arguments allow deleting
    and/or modifying configuration values to fail validation and provoke the
    expected error message.

    The goal is to collect the error message and status_code provided by the
    TA API endpoint and pass it to the corresponding test method for
    validation. Forges pass values to tests, probes, and forges by storing
    key-value pairs in the test artifactory, achieved by yielding key-value
    pairs in the form of a dictionary.

    In addition to the error message and status_code, the forge yields the
    expected proxy configuration used by a probe to ensure that the desired
    proxy settings are indeed applied to TA's configuration.

    At the teardown section, it only disables the configured proxy. This is
    done instead of restoring the previous configuration to avoid restoring
    a non-configured proxy state that always fails as some proxy fields are
    mandatory.

    Args:
        splunk_client (SplunkClient): The Splunk client instance.
        exclude (List[str], optional): List of proxy configuration fields to
            exclude. Defaults to [].
        overwrite (Dict[str, object], optional): Dictionary of proxy
            configuration fields to overwrite. Defaults to {}.

    Yields:
        Dict[str, object]: A dictionary containing the expected proxy
        configuration, error message, and status code.
    """

    error, status_code = None, None
    proxy_configs: Dict[str, object] = {
        "proxy_enabled": "0",
        "proxy_port": "3128",
        "proxy_rdns": "1",
        "proxy_type": "http",
        "proxy_url": "localhost",
        "proxy_username": "some_user_name",
        "proxy_password": "some_password",
    }

    for field_name in exclude:
        proxy_configs.pop(field_name, None)

    proxy_configs.update(overwrite)

    try:
        splunk_client.update_settings_proxy(**proxy_configs)
    except SplunkApiError as e:
        error = e.error_message
        status_code = e.status
        utils.logger.error(f"proxy error: {status_code},  {e.error_message}")

    yield dict(
        expected_proxy=proxy_configs,
        error=error,
        status_code=status_code,
    )

    # teardown
    if error is None:
        proxy_configs["proxy_enabled"] = "0"
        splunk_client.update_settings_proxy(**proxy_configs)


def configure_proxy(
    splunk_client: SplunkClient,
    proxy_configs: Dict[str, str],
) -> Generator[Dict[str, object], None, None]:
    """
    Configures the TA proxy settings for a Splunk client and ensures the
    desired proxy settings are applied to the TA's configuration.

    This function updates the proxy settings using the provided configurations
    and yields the expected proxy settings. It does not handle any exceptions
    internally; any API exceptions will cause the forge to crash, which is
    handled by the framework and results in a corresponding test fast fail.

    During the teardown phase, the function disables the configured proxy
    instead of restoring the previous configuration. This approach avoids
    restoring a non-configured proxy state, which always fails as some proxy
    fields are mandatory.

    Args:
        splunk_client (SplunkClient): The Splunk client to configure.
        proxy_configs (Dict[str, str]): The proxy configuration settings.

    Yields:
        Dict[str, object]: A dictionary containing the expected proxy settings.
    """
    splunk_client.update_settings_proxy(**proxy_configs)

    yield dict(
        expected_proxy=proxy_configs,
    )

    # teardown
    proxy_configs["proxy_enabled"] = "0"
    splunk_client.update_settings_proxy(**proxy_configs)


def configure_socks5_proxy(
    splunk_client: SplunkClient, valid: bool = True
) -> Generator[Dict[str, object], None, None]:
    """
    Forge method that prepares socks5 proxy configuration while using
    configure_proxy forge for actual proxy update.

    Based on test requirements, this forge can create a proxy with valid and
    invalid credentials. By default, it configures the proxy with valid
    credentials. A proxy with invalid credentials can be useful for tests
    checking how the TA handles incorrectly configured proxies and what error
    logs it creates to let users quickly detect the issue.

    Args:
        splunk_client (SplunkClient): The Splunk client instance.
        valid (bool, optional): Flag to determine if the proxy should be
            configured with valid credentials. Defaults to True.

    Yields:
        Generator[Dict[str, object], None, None]: A generator yielding the
        proxy configuration dictionary.
    """
    proxy_configs = {
        "proxy_enabled": "1",
        "proxy_port": "1080",
        "proxy_rdns": "1",
        "proxy_type": "socks5",
        "proxy_url": splunk_client.config.proxy_http_url,
    }

    if valid:
        proxy_configs.update(
            {
                "proxy_password": splunk_client.config.proxy_socks5_password,
                "proxy_username": splunk_client.config.proxy_socks5_username,
            }
        )
    else:
        proxy_configs.update(
            {
                "proxy_password": "invalid-proxy-password",
                "proxy_username": "invalid-proxy-username",
            }
        )

    yield from configure_proxy(splunk_client, proxy_configs)


def configure_http_proxy(
    splunk_client: SplunkClient, valid: bool = True
) -> Generator[Dict[str, object], None, None]:
    """
    Forge method that prepares http proxy configuration while using
    configure_proxy forge for actual proxy update.

    Based on test requirements, this forge can create a proxy with valid
    and invalid credentials. By default, it configures the proxy with valid
    credentials.

    A proxy with invalid credentials can be useful for tests checking how
    the TA handles incorrectly configured proxies and what error logs it
    creates to let users quickly detect the issue.

    Args:
        splunk_client (SplunkClient): The Splunk client instance.
        valid (bool): Flag indicating whether to configure the proxy with
                      valid credentials. Defaults to True.

    Yields:
        Generator[Dict[str, object], None, None]: A generator yielding the
        proxy configuration dictionary.
    """
    proxy_configs = {
        "proxy_enabled": "1",
        "proxy_port": "3128",
        "proxy_rdns": "1",
        "proxy_type": "http",
        "proxy_url": splunk_client.config.proxy_http_url,
    }

    if valid:
        proxy_configs.update(
            {
                "proxy_password": splunk_client.config.proxy_http_password,
                "proxy_username": splunk_client.config.proxy_http_username,
            }
        )
    else:
        proxy_configs.update(
            {
                "proxy_password": "invalid-proxy-password",
                "proxy_username": "invalid-proxy-username",
            }
        )

    yield from configure_proxy(splunk_client, proxy_configs)


def _account_config(name: str, vendor_client: VendorClient) -> Dict[str, str]:
    return {
        "name": name,
        "api_key": vendor_client.config.api_key,
    }


def account(
    splunk_client: SplunkClient,
    vendor_client: VendorClient,
) -> Generator[Dict[str, str], None, None]:
    account_config = _account_config("ExampleAccount", vendor_client)
    splunk_client.create_account(**account_config)
    yield dict(
        account_config_name=account_config["name"]
    )  # yielded from forges dict key will be available as global variable
    # you can use in your tests to refer to yielded dict value


def another_account(
    splunk_client: SplunkClient,
    vendor_client: VendorClient,
) -> Generator[Dict[str, str], None, None]:
    account_config = _account_config("AnotherExampleAccount", vendor_client)
    splunk_client.create_account(**account_config)
    yield dict(another_account_config_name=account_config["name"])


def another_account_index(
    splunk_client: SplunkClient,
) -> Generator[Dict[str, str], None, None]:
    index_name = f"idx_mit_another_account_{utils.Common().sufix}"
    splk_conf = splunk_client.splunk_configuration
    splk_conf.create_index(
        index_name,
        splk_conf.service,
        is_cloud=splk_conf.is_cloud,
        acs_stack=splk_conf._acs_stack,
        acs_server=splk_conf.acs_server,
        splunk_token=splk_conf.token,
    )
    yield {"another_account_index_name": index_name}


def _account_input(
    splunk_client: SplunkClient,
    test_id: str,
    *,
    name: str,
    index: str,
    account: str,
    input_spl_name: str,
) -> Generator[Dict[str, str], None, None]:
    start_time = utils.get_epoch_timestamp()
    name += f"_{test_id}"
    splunk_client.create_example(name, defaults.INPUT_INTERVAL, index, account)
    input_spl = (
        f'search index={index} source="example://{name}" ' f"| where _time>{start_time}"
    )
    # Take raw event into account when constructing the SPL; as an example:
    # extractions should be tested with pytest-splunk-addon
    yield {input_spl_name: input_spl}
    splunk_client.update_example(name, None, None, None, None, None, True)


def account_input(
    splunk_client: SplunkClient,
    # vendor_client: VendorClient,
    test_id: str,
    account_config_name: str,
) -> Generator[Dict[str, str], None, None]:
    yield from _account_input(
        splunk_client=splunk_client,
        test_id=test_id,
        name="ExampleInput",
        index=splunk_client.splunk_configuration.dedicated_index.name,
        account=account_config_name,
        input_spl_name="example_input_spl",
    )
