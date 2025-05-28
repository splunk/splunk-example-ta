1. Make sure there is no Splunk running on your workstation that exposes standard ports

2. Run following script:
```console
./scripts/run_locally.sh
```
Splunk and vendor product will be setup as docker containers: splunk-example-ta and server-example-ta respectively. Splunk container exposes standard ports and have `admin` user defined with `Chang3d!` as password

3. Make sure ucc-test-modinput is installed
```console
ucc-test-modinput --version
```

4. Export environment variables for:

    1. Splunk

    ```console
    export MODINPUT_TEST_SPLUNK_HOST=localhost
    export MODINPUT_TEST_SPLUNK_PORT=8089
    export MODINPUT_TEST_SPLUNK_USERNAME=admin
    export MODINPUT_TEST_SPLUNK_PASSWORD_BASE64=$(ucc-test-modinput base64encode -s 'Chang3d!')
    ```

    2. vendor product

    ```console
    export MODINPUT_TEST_EXAMPLE_API_KEY_BASE64=$(ucc-test-modinput base64encode -s 'super-secret-api-token')
    ```

5. Run ucc-test-modinput to generate add-on SDK
```console
ucc-test-modinput gen
```

6. Run tests
```console
pytest tests/ucc_modinput_functional/
```