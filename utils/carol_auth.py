from dotenv import load_dotenv
from pycarol import Carol, PwdAuth
import os

load_dotenv()

def tenant_login(tenant=None):

    CAROLUSER = os.environ.get("CAROLUSER")
    CAROLPWD = os.environ.get("CAROLPWD")
    CAROLTENANT = tenant if tenant is not None else os.environ.get("CAROLTENANT")

    carol = Carol(auth=PwdAuth(CAROLUSER, CAROLPWD), organization='global', domain='admin')
    try: #mdmId
        tenant = carol.call_api(f'v3/admin/tenants/{CAROLTENANT}', 'GET')
    except: #mdmSubdomain
        tenant = carol.call_api(f'v3/tenants/domain/{CAROLTENANT}', 'GET')

    org = carol.call_api(f'v3/organizations/{tenant["mdmOrgId"]}', 'GET', extra_headers={'overriddentenantid': tenant['mdmId']})
    connector = carol.call_api(f'v3/connectors?pageSize=1', 'GET', extra_headers={'overriddentenantid': tenant['mdmId']})
    try:
        app = carol.call_api(f'v1/carolApps?pageSize=-1', 'GET', extra_headers={'overriddentenantid': tenant['mdmId']})
    except:
        app = carol.call_api(f'v1/tenantApps?pageSize=-1', 'GET', extra_headers={'overriddentenantid': tenant['mdmId']})

    if app['empty'] != True:
        carol = Carol(auth=PwdAuth(CAROLUSER, CAROLPWD), organization=org['mdmSubdomain'], domain=tenant['mdmSubdomain'], connector_id=connector['hits'][0]['mdmId'], app_name=app['hits'][0]['mdmName'])
        return (carol)
    else:
        raise Exception(f"No App on tenant {tenant['mdmSubdomain']}")

def org_login():

    CAROLUSER = os.environ.get("CAROLUSER")
    CAROLPWD = os.environ.get("CAROLPWD")
    CAROLTENANT = os.environ.get("CAROLTENANT")

    carol = Carol(auth=PwdAuth(CAROLUSER, CAROLPWD), organization='global', domain='admin')
    try: #mdmId
        tenant = carol.call_api(f'v3/admin/tenants/{CAROLTENANT}', 'GET')
    except: #mdmSubdomain
        tenant = carol.call_api(f'v3/tenants/domain/{CAROLTENANT}', 'GET')

    org = carol.call_api(f'v3/organizations/{tenant["mdmOrgId"]}', 'GET', extra_headers={'overriddentenantid': tenant['mdmId']})
    carol = Carol(auth=PwdAuth(CAROLUSER, CAROLPWD), organization=org['mdmSubdomain'], org_level=True)

    return (carol)