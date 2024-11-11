import datetime
from datetime import timezone
import json
import logging
from typing import Optional

import import_declare_test

import example_utils

import requests
from solnlib import conf_manager, log
from solnlib.modular_input import checkpointer
from splunklib import modularinput as smi


ADDON_NAME = "Splunk_TA_Example"


def logger_for_input(input_name: str) -> logging.Logger:
    return log.Logs().get_logger(f"{ADDON_NAME.lower()}_{input_name}")


def get_account_api_key(session_key: str, account_name: str):
    cfm = conf_manager.ConfManager(
        session_key,
        ADDON_NAME,
        realm=f"__REST_CREDENTIAL__#{ADDON_NAME}#configs/conf-splunk_ta_example_account",
    )
    account_conf_file = cfm.get_conf("splunk_ta_example_account")
    return account_conf_file.get(account_name).get("api_key")


def get_data_from_api(
    logger: logging.Logger, api_key: str, checkpoint: Optional[str] = None
):
    # So far not used.
    del checkpoint
    logger.info("Getting data from an external API")

    def _call_api():
        response = requests.get(
            "http://server:5000/events",
            headers={
                "API-Key": api_key,
            },
            timeout=20,
        )
        response.raise_for_status()
        return response.json()

    for i in range(3):
        try:
            return _call_api()
        except requests.exceptions.HTTPError:
            logger.warning("Failed to get data from the API, retrying...")
    raise Exception("Failed to get data from the API")


def validate_input(definition: smi.ValidationDefinition):
    return


def stream_events(inputs: smi.InputDefinition, event_writer: smi.EventWriter):
    # inputs.inputs is a Python dictionary object like:
    # {
    #   "example://<input_name>": {
    #     "account": "<account_name>",
    #     "disabled": "0",
    #     "host": "$decideOnStartup",
    #     "index": "<index_name>",
    #     "interval": "<interval_value>",
    #     "python.version": "python3",
    #   },
    # }
    for input_name, input_item in inputs.inputs.items():
        normalized_input_name = input_name.split("/")[-1]
        logger = logger_for_input(normalized_input_name)
        try:
            session_key = inputs.metadata["session_key"]
            kvstore_checkpointer = checkpointer.KVStoreCheckpointer(
                "example_checkpointer",
                session_key,
                ADDON_NAME,
            )
            log_level = conf_manager.get_log_level(
                logger=logger,
                session_key=session_key,
                app_name=ADDON_NAME,
                conf_name="splunk_ta_example_settings",
            )
            logger.setLevel(log_level)
            log.modular_input_start(logger, normalized_input_name)
            api_key = get_account_api_key(session_key, input_item.get("account"))
            checkpointer_key_name = example_utils.get_example_collection_key_name(
                input_name
            )
            current_checkpoint = kvstore_checkpointer.get(checkpointer_key_name)
            data = get_data_from_api(logger, api_key, current_checkpoint)
            sourcetype = "example:events"
            for line in data:
                event_writer.write_event(
                    smi.Event(
                        data=json.dumps(line, ensure_ascii=False, default=str),
                        index=input_item.get("index"),
                        sourcetype=sourcetype,
                    )
                )
            new_checkpoint = (
                datetime.datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
            )
            kvstore_checkpointer.update(checkpointer_key_name, new_checkpoint)
            log.events_ingested(
                logger,
                input_name,
                sourcetype,
                len(data),
                input_item.get("index"),
                account=input_item.get("account"),
            )
            log.modular_input_end(logger, normalized_input_name)
        except Exception as e:
            log.log_exception(
                logger,
                e,
                "IngestionError",
                msg_before="Exception raised while ingesting data for demo_input: ",
            )
