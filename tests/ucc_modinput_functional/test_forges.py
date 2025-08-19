from splunk_add_on_ucc_modinput_test.functional.decorators import (
    bootstrap,
    forge,
    attach,
)


def failing_forge(test_id: str):
    raise Exception(f"This is a failing forge for test {test_id}.")


# this test will fail
@bootstrap(forge(failing_forge))
def test_bootstrap() -> None:
    assert True


# this will not fail
@attach(forge(failing_forge))
def test_attach() -> None:
    assert True
