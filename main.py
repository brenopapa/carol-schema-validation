import utils.carol_auth as carol_auth
import utils.schema as schema
from utils.parser import PARSER

args = vars(PARSER.parse_args())

def run():

    default = carol_auth.tenant_login(args.get("default"))
    target = carol_auth.tenant_login(args.get("target"))
    
    #BQ COMPARISON
    default_bq_schema = schema.bigquery_schema(default, args.get("connector"))
    target_bq_schema = schema.bigquery_schema(target, args.get("connector"))
    
    print(schema.bigquery_compare(default_bq_schema, target_bq_schema))

    #CAROL COMPARISON
    default_carol_schema = schema.carol_schema(default, args.get("connector"))
    target_carol_schema = schema.carol_schema(target, args.get("connector"))

    print(schema.carol_compare(default_carol_schema, target_carol_schema))

if __name__ == "__main__":
    run()