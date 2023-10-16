import functions_framework
from cloudevents.http.event import CloudEvent
# from utils.parser import PARSER

import utils.carol_auth as carol_auth
import utils.schema as schema

# args = vars(PARSER.parse_args())

@functions_framework.cloud_event
def run(cloud_event: CloudEvent) -> None:
    print(f"Received event with ID: {cloud_event['id']} and data {cloud_event.data}")
    print(f"default is {cloud_event.data['default']} and target is {cloud_event.data['target']}")

    default = carol_auth.tenant_login(cloud_event.data['default'])
    target = carol_auth.tenant_login(cloud_event.data['target'])
    
    # BQ COMPARISON
    try:
        print(f"Getting BQ schemas for {cloud_event.data['default']} and {cloud_event.data['target']}... \n")
        default_bq_schema = schema.bigquery_schema(default, cloud_event.data['connector'])
        target_bq_schema = schema.bigquery_schema(target, cloud_event.data['connector'])
        print("Success!!! \n")
    except Exception as e:
        raise(e)
    try:
        print(f"BQ Fields on {cloud_event.data['default']} not present in {cloud_event.data['target']}: \n")
        print(schema.bigquery_compare(default_bq_schema, target_bq_schema))
    except Exception as e:
        raise(e)
    
    # CAROL COMPARISON
    try:
        print(f"Getting CAROL PKs (crosswalks) for {cloud_event.data['default']} and {cloud_event.data['target']}... \n")
        default_carol_schema = schema.carol_schema(default, cloud_event.data['connector'])
        target_carol_schema = schema.carol_schema(target, cloud_event.data['connector'])
        print("Success!!! \n")
    except Exception as e:
        raise(e)
    try:
        print(f"Divergent PKs (crosswalks): \n")
        print(schema.carol_compare(default_carol_schema, target_carol_schema))
    except Exception as e:
        raise(e)
if __name__ == "__main__":
    run()