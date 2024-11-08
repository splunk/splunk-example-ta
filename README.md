# Splunk_TA_Example

## Build and run `server`

```bash
docker build -t server server/; docker run -p 5000:5000 server
```

Test the server by running the following command:

```bash
curl -H "API-Key: super-secret-api-token" localhost:5000/events
```
