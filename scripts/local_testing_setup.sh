curl -k -X POST -u admin:Chang3d! --header "Content-Type: application/json" https://localhost:8089/servicesNS/-/Splunk_TA_Example/Splunk_TA_Example_account -d name=api_key -d api_key=super-secret-api-token

for i in $(seq 1 4);
do
    curl -k -X POST -u admin:Chang3d! --header "Content-Type: application/json" https://localhost:8089/servicesNS/-/Splunk_TA_Example/Splunk_TA_Example_example -d name=test_input_$i -d interval=20 -d index=main -d account=api_key
done
