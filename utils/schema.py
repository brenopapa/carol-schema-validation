import pandas as pd
from pycarol import BQ

def carol_schema(carol):
    schema = carol.call_api(f'v3/staging?pageSize=-1', 'GET')['hits']
    return schema

def carol_compare(default, target):
    default = pd.DataFrame.from_dict(default)
    target = pd.DataFrame.from_dict(target)

        # for staging in default:
        # d = {
        #     'mdmStagingType': staging['mdmStagingType'], 
        #     'mdmCrosswalkTemplate': staging['mdmCrosswalkTemplate']['mdmCrossreference'],
        #     'mdmSchemaMapping': staging['mdmSchemaMapping']['mdmPropertyOrdering']
        #     }
        # default_df = pd.DataFrame(data=d)

    merged = pd.merge(default, target, on=["mdmStagingType"], how="left", indicator=True)

    return merged
 
def bigquery_schema(carol, connector):
    schema = BQ(carol).query(
        f''' SELECT 
                table_name, column_name
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE 1=1
            AND table_name like 'ingestion_stg_{connector}%'
            AND column_name not like 'mdm%'
            AND column_name not like '_ingestionDatetime'
        ''')
    return schema

def bigquery_compare(default, target):
    merged = pd.merge(default, target, on=["table_name", "column_name"], how="left", indicator=True)
    missing_fields = merged.query('_merge=="left_only"')
    missing_fields.drop("_merge", axis=1, inplace=True)
    missing_fields["event_date"] = pd.Timestamp.now()
    return missing_fields