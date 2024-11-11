import traceback

import import_declare_test

from solnlib import log
from solnlib.modular_input import checkpointer
from splunktaucclib.rest_handler.admin_external import AdminExternalHandler

import example_utils


class DeleteCheckpointRestHandler(AdminExternalHandler):
    def __init__(self, *args, **kwargs):
        AdminExternalHandler.__init__(self, *args, **kwargs)

    def handleList(self, confInfo):
        AdminExternalHandler.handleList(self, confInfo)

    def handleEdit(self, confInfo):
        AdminExternalHandler.handleEdit(self, confInfo)

    def handleCreate(self, confInfo):
        AdminExternalHandler.handleCreate(self, confInfo)

    def handleRemove(self, confInfo):
        log_filename = "example_delete_checkpoint"
        logger = log.Logs().get_logger(log_filename)
        session_key = self.getSessionKey()
        input_name = str(self.callerArgs.id)
        checkpointer_key_name = example_utils.get_example_collection_key_name(
            input_name
        )
        logger.info(f"Deleting the checkpoint for input '{input_name}'")
        try:
            kvstore_checkpointer = checkpointer.KVStoreCheckpointer(
                "example_checkpointer",
                session_key,
                example_utils.ADDON_NAME,
            )
            kvstore_checkpointer.delete(checkpointer_key_name)
        except Exception as e:
            log.log_exception(
                logger,
                e,
                "Checkpoint Error",
                msg_before=f"Error while deleting checkpoint for {input_name} input. {traceback.format_exc()}",
            )
        AdminExternalHandler.handleRemove(self, confInfo)
