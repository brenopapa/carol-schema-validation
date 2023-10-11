import utils.carol_auth as carol_auth
import utils.schema as schema
from utils.parser import PARSER

args = vars(PARSER.parse_args())

def run():


    default = carol_auth.tenant_login(args.get("default"))
    target = carol_auth.tenant_login(args.get("target"))
    
    # BQ COMPARISON
    try:
        print(f'Getting BQ schemas for {args.get("default")} and {args.get("target")}... \n')
        default_bq_schema = schema.bigquery_schema(default, args.get("connector"))
        target_bq_schema = schema.bigquery_schema(target, args.get("connector"))
        print('Success!!! \n')
    except Exception as e:
        raise(e)
    try:
        print(f'BQ Fields on {args.get("default")} not present in {args.get("target")}: \n')
        print(schema.bigquery_compare(default_bq_schema, target_bq_schema))
    except Exception as e:
        raise(e)
    
    # CAROL COMPARISON
    try:
        print(f'Getting CAROL PKs (crosswalks) for {args.get("default")} and {args.get("target")}... \n')
        default_carol_schema = schema.carol_schema(default, args.get("connector"))
        target_carol_schema = schema.carol_schema(target, args.get("connector"))
        print('Success!!! \n')
    except Exception as e:
        raise(e)
    try:
        print(f'Divergent PKs (crosswalks): \n')
        print(schema.carol_compare(default_carol_schema, target_carol_schema))
    except Exception as e:
        raise(e)
if __name__ == "__main__":
    run()