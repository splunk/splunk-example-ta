# Splunk_TA_Example

This is an example TA for Splunk that demonstrates how to use the modular input framework to collect data from an API and send it to Splunk.

## Frameworks and tools used

* UCC - https://github.com/splunk/addonfactory-ucc-generator
* PSA - https://github.com/splunk/pytest-splunk-addon

## API

The API is a simple Flask app that returns a list of events.

## Build and package TA

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
ucc-gen build
ucc-gen package --path output/Splunk_TA_Example
```

## Build and run Splunk and `server`

```bash
./scripts/run_locally.sh
```

## Notable PRs

* Custom REST handlers - https://github.com/splunk/splunk-example-ta/pull/4
* Add KVStore checkpoint for modular input - https://github.com/splunk/splunk-example-ta/pull/5
* Delete KVStore checkpoint when input is deleted - https://github.com/splunk/splunk-example-ta/pull/6
