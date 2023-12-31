import pandas as pd
from pycarol import BQ

pd.set_option('display.max_columns', None) 
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None) 
pd.set_option('display.max_colwidth', None)

def carol_schema(carol, connector):
    schema = carol.call_api(f'v3/staging?pageSize=-1', 'GET')['hits']
    if connector != '':
        connector = carol.call_api(f'v3/connectors/name/{connector}', 'GET')['mdmId']
        for staging in schema:
            if staging['mdmConnectorId'] != connector:
                del schema[schema.index(staging)]
    return schema
 
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

def carol_compare(default, target):
    default = pd.DataFrame.from_dict(default)
    target = pd.DataFrame.from_dict(target)
    result = pd.DataFrame(columns=["table_name","default_pk","target_pk"])

    for index, staging in default.iterrows():
        default_staging = staging['mdmStagingType']
        default_pk = staging['mdmCrosswalkTemplate']
        target_pk = target[target['mdmStagingType'] == default_staging]['mdmCrosswalkTemplate']

        if len(target_pk) == 0: target_pk = 'table not found'
        else: target_pk = target_pk.item()

        if target_pk != default_pk:
            divergence = pd.DataFrame(
                                    {"table_name": default_staging, 
                                     "default_pk": default_pk, 
                                     "target_pk": target_pk}
                                     , columns=["table_name","default_pk","target_pk"]
                                     )
            result = pd.concat([result, divergence], ignore_index=True)
    return result.reset_index(drop=True)

def bigquery_compare(default, target):
    merged = pd.merge(default, target, on=["table_name", "column_name"], how="left", indicator=True)
    missing_fields = merged.query('_merge=="left_only"')
    missing_fields.drop("_merge", axis=1, inplace=True)
    missing_fields["event_date"] = pd.Timestamp.now()
    return missing_fields.reset_index(drop=True)

def pk_mdmId_lookup(carol, target, connector):
    target = pd.DataFrame.from_dict(target)
    lookupquery = ''
    for index, staging in target.iterrows():
        table_name = staging['mdmStagingType']
        fields_list = staging['mdmCrosswalkTemplate']['mdmCrossreference'][next(iter(staging['mdmCrosswalkTemplate']['mdmCrossreference']))]
        lookupquery = lookupquery + f''' 
        SELECT * FROM (
            SELECT 'stg_{connector}_{table_name}', TRUE 
            FROM (
                SELECT {', '.join(fields_list)}, count(mdmId) as qtd
                    FROM stg_{connector}_{table_name} 
                GROUP BY {', '.join(fields_list)}
            ) WHERE qtd > 1 LIMIT 1 
        )
        UNION ALL'''
    result = BQ(carol).query(lookupquery[:-len('UNION ALL')])
    if result.empty:
        return "No Duplicates!"
    else:
        return result