curl -X POST localhost:8080 \
   -H "Content-Type: application/cloudevents+json" \
   -d '{
        "specversion" : "1.0",
        "type" : "example.com.cloud.event",
        "source" : "https://example.com/cloudevents/pull",
        "subject" : "123",
        "id" : "A234-1234-1234",
        "time" : "2018-04-05T17:31:00Z",
        "data" : {"default" : "backofficeinsights", "target":"tenant4a9cb7c5de3c11ea9aaf22d41f2aff2f", "connector":"protheus_carol"}
}'