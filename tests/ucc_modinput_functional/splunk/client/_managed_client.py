# fmt: off

"""
Note:
    This file is under the control of the ucc-test-modinput CLI tool and must
    not be modified manually by developers. If an extension is needed or a
    method needs to be redefined, it should be done in a separate file.
"""

import json
from typing import Any, Dict, List, Optional
from splunk_add_on_ucc_modinput_test.functional.splunk.client import (
    SplunkClientBase,
)
from swagger_client.rest import ApiException
import logging

logger = logging.getLogger("ucc-modinput-test")


class SplunkApiError(Exception):
    def __init__(self, error: ApiException):
        self.api_exception = error

    @property
    def status(self) -> int:
        return int(self.api_exception.status)

    @property
    def reason(self) -> str:
        return self.api_exception.reason

    @property
    def body(self) -> bytes:
        return self.api_exception.body

    @property
    def json(self) -> Optional[Dict[str, Any]]:
        try:
            return json.loads(self.api_exception.body)
        except json.JSONDecodeError:
            return None

    @property
    def error_message(self) -> Optional[str]:
        json_body = self.json
        if json_body:
            return json_body.get("messages", [{}])[0].get("text")
        return None


class ManagedSplunkClient(SplunkClientBase):
    _OUTPUT_MODE = "json"

    def get_account_list(self) -> List[Any]:
        try:
            kwargs = dict(output_mode=self._OUTPUT_MODE)
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            response = (
                self.ta_api.splunk_ta_example_account_get(
                    **kwargs
                )
            )
            logger.debug(
                f"TA API splunk_ta_example_account_get response: {response}"
            )

            return response.to_dict().get("entry", [])

        except ApiException as e:
            logger.error(
                "Exception when calling TA API splunk_ta_example_account_get:"
                f" {e}"
            )
            raise SplunkApiError(e) from e

    def delete_account(self, name: str) -> None:
        try:
            kwargs = dict(name=name, output_mode=self._OUTPUT_MODE)
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            response = (
                self.ta_api.splunk_ta_example_account_name_delete(
                    **kwargs
                )
            )
            logger.debug(
                f"TA API splunk_ta_example_account_name_delete response: {response}"  # noqa: E501
            )

            return None

        except ApiException as e:
            logger.error(
                "Exception when calling TA API splunk_ta_example_account_name_delete:"  # noqa: E501
                f" {e}"
            )
            raise SplunkApiError(e) from e

    def get_account(self, name: str) -> Dict[str, Any]:
        try:
            kwargs = dict(name=name, output_mode=self._OUTPUT_MODE)
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            response = (
                self.ta_api.splunk_ta_example_account_name_get(
                    **kwargs
                )
            )
            logger.debug(
                f"TA API splunk_ta_example_account_name_get response: {response}"  # noqa: E501
            )

            return response.to_dict().get("entry", [{}])[0].get("content")

        except ApiException as e:
            logger.error(
                "Exception when calling TA API splunk_ta_example_account_name_get:"  # noqa: E501
                f" {e}"
            )
            raise SplunkApiError(e) from e

    def update_account(self, name: str, api_key: Optional[str] = None) -> Dict[str, Any]:  # noqa: E501
        try:
            kwargs = dict(output_mode=self._OUTPUT_MODE, name=name, api_key=api_key)  # noqa: E501
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            response = (
                self.ta_api.splunk_ta_example_account_name_post(
                    **kwargs
                )
            )
            logger.debug(
                f"TA API splunk_ta_example_account_name_post response: {response}"  # noqa: E501
            )

            return response.to_dict().get("entry", [{}])[0].get("content")

        except ApiException as e:
            logger.error(
                "Exception when calling TA API splunk_ta_example_account_name_post:"  # noqa: E501
                f" {e}"
            )
            raise SplunkApiError(e) from e

    def create_account(self, name: Optional[str] = None, api_key: Optional[str] = None) -> Dict[str, Any]:  # noqa: E501
        try:
            kwargs = dict(output_mode=self._OUTPUT_MODE, name=name, api_key=api_key)  # noqa: E501
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            response = (
                self.ta_api.splunk_ta_example_account_post(
                    **kwargs
                )
            )
            logger.debug(
                f"TA API splunk_ta_example_account_post response: {response}"
            )

            return response.to_dict().get("entry", [{}])[0].get("content")

        except ApiException as e:
            logger.error(
                "Exception when calling TA API splunk_ta_example_account_post:"
                f" {e}"
            )
            raise SplunkApiError(e) from e

    def get_example_list(self) -> List[Any]:
        try:
            kwargs = dict(output_mode=self._OUTPUT_MODE)
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            response = (
                self.ta_api.splunk_ta_example_example_get(
                    **kwargs
                )
            )
            logger.debug(
                f"TA API splunk_ta_example_example_get response: {response}"
            )

            return response.to_dict().get("entry", [])

        except ApiException as e:
            logger.error(
                "Exception when calling TA API splunk_ta_example_example_get:"
                f" {e}"
            )
            raise SplunkApiError(e) from e

    def delete_example(self, name: str) -> None:
        try:
            kwargs = dict(name=name, output_mode=self._OUTPUT_MODE)
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            response = (
                self.ta_api.splunk_ta_example_example_name_delete(
                    **kwargs
                )
            )
            logger.debug(
                f"TA API splunk_ta_example_example_name_delete response: {response}"  # noqa: E501
            )

            return None

        except ApiException as e:
            logger.error(
                "Exception when calling TA API splunk_ta_example_example_name_delete:"  # noqa: E501
                f" {e}"
            )
            raise SplunkApiError(e) from e

    def get_example(self, name: str) -> Dict[str, Any]:
        try:
            kwargs = dict(name=name, output_mode=self._OUTPUT_MODE)
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            response = (
                self.ta_api.splunk_ta_example_example_name_get(
                    **kwargs
                )
            )
            logger.debug(
                f"TA API splunk_ta_example_example_name_get response: {response}"  # noqa: E501
            )

            return response.to_dict().get("entry", [{}])[0].get("content")

        except ApiException as e:
            logger.error(
                "Exception when calling TA API splunk_ta_example_example_name_get:"  # noqa: E501
                f" {e}"
            )
            raise SplunkApiError(e) from e

    def update_example(
        self,
        name: str,
        interval: Optional[str] = None,
        index: Optional[str] = None,
        account: Optional[str] = None,
        fetch_from: Optional[str] = None,
        start_from: Optional[str] = None,
        disabled: Optional[str] = None,
    ) -> Dict[str, Any]:
        try:
            kwargs = dict(
                output_mode=self._OUTPUT_MODE,
                name=name,
                interval=interval,
                index=index,
                account=account,
                fetch_from=fetch_from,
                start_from=start_from,
                disabled=disabled,
            )
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            response = (
                self.ta_api.splunk_ta_example_example_name_post(
                    **kwargs
                )
            )
            logger.debug(
                f"TA API splunk_ta_example_example_name_post response: {response}"  # noqa: E501
            )

            return response.to_dict().get("entry", [{}])[0].get("content")

        except ApiException as e:
            logger.error(
                "Exception when calling TA API splunk_ta_example_example_name_post:"  # noqa: E501
                f" {e}"
            )
            raise SplunkApiError(e) from e

    def create_example(
        self,
        name: Optional[str] = None,
        interval: Optional[str] = None,
        index: Optional[str] = None,
        account: Optional[str] = None,
        fetch_from: Optional[str] = None,
        start_from: Optional[str] = None,
    ) -> Dict[str, Any]:
        try:
            kwargs = dict(
                output_mode=self._OUTPUT_MODE,
                name=name,
                interval=interval,
                index=index,
                account=account,
                fetch_from=fetch_from,
                start_from=start_from,
            )
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            response = (
                self.ta_api.splunk_ta_example_example_post(
                    **kwargs
                )
            )
            logger.debug(
                f"TA API splunk_ta_example_example_post response: {response}"
            )

            return response.to_dict().get("entry", [{}])[0].get("content")

        except ApiException as e:
            logger.error(
                "Exception when calling TA API splunk_ta_example_example_post:"
                f" {e}"
            )
            raise SplunkApiError(e) from e

    def get_settings_advanced_inputs(self) -> Dict[str, Any]:
        try:
            kwargs = dict(output_mode=self._OUTPUT_MODE)
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            response = (
                self.ta_api.splunk_ta_example_settings_advanced_inputs_get(
                    **kwargs
                )
            )
            logger.debug(
                f"TA API splunk_ta_example_settings_advanced_inputs_get response: {response}"  # noqa: E501
            )

            return response.to_dict().get("entry", [{}])[0].get("content")

        except ApiException as e:
            logger.error(
                "Exception when calling TA API splunk_ta_example_settings_advanced_inputs_get:"  # noqa: E501
                f" {e}"
            )
            raise SplunkApiError(e) from e

    def update_settings_advanced_inputs(self) -> Dict[str, Any]:
        try:
            kwargs = dict(output_mode=self._OUTPUT_MODE)
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            response = (
                self.ta_api.splunk_ta_example_settings_advanced_inputs_post(
                    **kwargs
                )
            )
            logger.debug(
                f"TA API splunk_ta_example_settings_advanced_inputs_post response: {response}"  # noqa: E501
            )

            return response.to_dict().get("entry", [{}])[0].get("content")

        except ApiException as e:
            logger.error(
                "Exception when calling TA API splunk_ta_example_settings_advanced_inputs_post:"  # noqa: E501
                f" {e}"
            )
            raise SplunkApiError(e) from e

    def get_settings_logging(self) -> Dict[str, Any]:
        try:
            kwargs = dict(output_mode=self._OUTPUT_MODE)
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            response = (
                self.ta_api.splunk_ta_example_settings_logging_get(
                    **kwargs
                )
            )
            logger.debug(
                f"TA API splunk_ta_example_settings_logging_get response: {response}"  # noqa: E501
            )

            return response.to_dict().get("entry", [{}])[0].get("content")

        except ApiException as e:
            logger.error(
                "Exception when calling TA API splunk_ta_example_settings_logging_get:"  # noqa: E501
                f" {e}"
            )
            raise SplunkApiError(e) from e

    def update_settings_logging(self, loglevel: Optional[str] = None) -> Dict[str, Any]:  # noqa: E501
        try:
            kwargs = dict(output_mode=self._OUTPUT_MODE, loglevel=loglevel)
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            response = (
                self.ta_api.splunk_ta_example_settings_logging_post(
                    **kwargs
                )
            )
            logger.debug(
                f"TA API splunk_ta_example_settings_logging_post response: {response}"  # noqa: E501
            )

            return response.to_dict().get("entry", [{}])[0].get("content")

        except ApiException as e:
            logger.error(
                "Exception when calling TA API splunk_ta_example_settings_logging_post:"  # noqa: E501
                f" {e}"
            )
            raise SplunkApiError(e) from e

    def get_settings_proxy(self) -> Dict[str, Any]:
        try:
            kwargs = dict(output_mode=self._OUTPUT_MODE)
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            response = (
                self.ta_api.splunk_ta_example_settings_proxy_get(
                    **kwargs
                )
            )
            logger.debug(
                f"TA API splunk_ta_example_settings_proxy_get response: {response}"  # noqa: E501
            )

            return response.to_dict().get("entry", [{}])[0].get("content")

        except ApiException as e:
            logger.error(
                "Exception when calling TA API splunk_ta_example_settings_proxy_get:"  # noqa: E501
                f" {e}"
            )
            raise SplunkApiError(e) from e

    def update_settings_proxy(
        self,
        proxy_enabled: Optional[str] = None,
        proxy_type: Optional[str] = None,
        proxy_url: Optional[str] = None,
        proxy_port: Optional[str] = None,
        proxy_username: Optional[str] = None,
        proxy_password: Optional[str] = None,
        proxy_rdns: Optional[str] = None,
    ) -> Dict[str, Any]:
        try:
            kwargs = dict(
                output_mode=self._OUTPUT_MODE,
                proxy_enabled=proxy_enabled,
                proxy_type=proxy_type,
                proxy_url=proxy_url,
                proxy_port=proxy_port,
                proxy_username=proxy_username,
                proxy_password=proxy_password,
                proxy_rdns=proxy_rdns,
            )
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            response = (
                self.ta_api.splunk_ta_example_settings_proxy_post(
                    **kwargs
                )
            )
            logger.debug(
                f"TA API splunk_ta_example_settings_proxy_post response: {response}"  # noqa: E501
            )

            return response.to_dict().get("entry", [{}])[0].get("content")

        except ApiException as e:
            logger.error(
                "Exception when calling TA API splunk_ta_example_settings_proxy_post:"  # noqa: E501
                f" {e}"
            )
            raise SplunkApiError(e) from e
# fmt: on
