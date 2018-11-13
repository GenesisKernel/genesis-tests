import requests
import json
import time
import os


from genesis_blockchain_tools.contract import Contract
from libs import api, db, tools, loger

wait = tools.read_config("test")["wait_tx_status"]
log = loger.create_loger(__name__)


def login(url, pr_key, role=0, ecosystem=1):
    token, uid = api.getuid(url)
    result = api.login(
        url=url,
        token=token,
        uid=uid,
        private_key=pr_key,
        role_id=role,
        ecosystem=ecosystem
    )
    return result


def call_contract(url, prKey, name, data, jvtToken, ecosystem=1):
    schema = api.contract(url, jvtToken, name)
    contract = Contract(schema=schema,
                        private_key=prKey,
                        ecosystem_id=ecosystem,
                        params=data)
    tx_bin_data = {'call1': contract.concat()}
    result = api.send_tx(url, jvtToken, tx_bin_data)
    if 'hashes' in result:
        return result['hashes']['call1']
    else:
        return result


def call_multi_contract(url, prKey, name, data, jvtToken, withData=True):
    full_bindata = {}
    i = 1
    for inf in data:
        if withData and inf['params']['Data'] == '[]':
            continue
        schema = api.contract(url, jvtToken, inf['contract'])
        contract = Contract(
            schema=schema,
            private_key=prKey,
            params=inf['params']
        )
        tx_bin_data = contract.concat()
        full_bindata.update({'call' + str(i): tx_bin_data})
        i += 1
    result = api.send_tx(url, jvtToken, full_bindata)
    return result


def tx_status(url, sleep_time, hsh, jvt_token):
    sec = 0
    while sec < sleep_time:
        time.sleep(1)
        resp = api.tx_status(url, jvt_token, hsh)
        jresp = resp['results'][hsh]
        if (len(jresp['blockid']) > 0 and 'errmsg' not in json.dumps(jresp)) or ('errmsg' in json.dumps(jresp)):
            break
        else:
            sec = sec + 1
    if 'errmsg' not in jresp and jresp['blockid'] == '':
        return {'blockid': None, 'result': None, 'error': None}
    if 'errmsg' not in jresp and int(jresp['blockid']) > 0:
        return {'blockid': int(jresp['blockid']), 'result': jresp['result'], 'error': None}
    else:
        return {'blockid': 0, 'error': jresp['errmsg']['error'], 'result': None}


def tx_status_multi(url, sleep_time, hshs, jvt_token):
    url_end = url + '/txstatus'
    allTxInBlocks = False
    sec = 0
    list = []
    for hash in hshs:
        list.append(hshs[hash])
    while sec < sleep_time:
        time.sleep(1)
        resp = requests.post(url_end, params={'data': json.dumps({'hashes': list})},
                             headers={'Authorization': jvt_token})
        jresp = resp.json()['results']
        for status in jresp.values():
            if (len(status['blockid']) > 0 and 'errmsg' not in json.dumps(status)):
                allTxInBlocks = True
            else:
                allTxInBlocks = False
        if allTxInBlocks:
            return jresp
        else:
            sec = sec + 1
    return jresp


def call_get_api(url, data, token):
    resp = requests.get(url, params=data,  headers={'Authorization': token})
    return resp.json()


def call_get_api_with_full_response(url, data, token):
    resp = requests.get(url, params=data,  headers={'Authorization': token})
    return resp


def call_post_api(url, data, token):
    resp = requests.post(url, data=data,  headers={'Authorization': token})
    return resp.json()


def get_count(url, name, token):
    res = api.list(url, token, name, limit=1)
    return res['count']


def get_list(url, type, token):
    count = get_count(url, type, token)
    res = api.list(url, token, type, limit=count)
    return res


def get_contract_id(url, name, token):
    res = api.contract(url, token, name)
    return res['tableid']


def get_object_id(url, name, object, token, ecosystem=1):
    id = None
    param_name = 'name'
    if object == 'members':
        param_name = 'member_name'
    res = get_list(url, object, token)
    for object in res['list']:
        if object[param_name] == name \
                and int(object['ecosystem']) == ecosystem:
            id = object['id']
            break
    return id


def get_object_name(url, id, object, token):
    name = None
    res = get_list(url, object, token)
    for object in res['list']:
        if object['id'] == id:
            name = object['name']
            break
    return name


def is_contract_activated(url, name, token):
    res = api.contract(url, token, name)
    return res['active']


def get_activated_wallet(url, name, token):
    res = api.contract(url, token, name)
    return res['walletid']


def get_parameter_id(url, name, token):
    res = api.ecosystemparam(url, token, name)
    return res['id']


def get_parameter_value(url, name, token):
    res = api.ecosystemparam(url, token, name)
    return res['value']


def get_sysparams_value(url, token, name):
    list = api.systemparams(url, token, name)
    return list['list'][0]['value']


def get_content(url, type, name, lang, app_id, token):
    res = api.content(url, token, type, name, lang, app_id)
    return res


def get_max_block_id(url, token):
    res = api.maxblockid(url, token)
    return res['max_block_id']

# limits


def is_count_tx_in_block(url, token, max_block_id, count_tx):
    block = max_block_id - 3
    while block < max_block_id:
        info = api.block(url, token, block)
        block += 1
        if int(info['tx_count']) > count_tx:
            log.error('Error in count_tx. Block ' + str(block) + ' has ' +
                      str(block['count_tx']) + ' transactions')
            return False
    return True


# api
def get_ecosys_tables(url, token):
    count = get_count(url, 'tables', token)
    tables = api.tables(url, token, limit=count)['list']
    list = []
    for table in tables:
        list.append(table['name'])
    return list


# system_contracts
def get_export_app_data(url, token, app_id, member_id):
    result = api.list(url, token, 'binaries')
    for item in result['list']:
        if item['name'] == 'export' \
                and item['app_id'] == str(app_id) \
                and item['member_id'] == str(member_id):
            return str(item['data'])
    return None

# system_contracts


def get_import_app_data(url, token, member_id):
    result = api.list(url, token, 'buffer_data')
    for item in result['list']:
        if item['key'] == 'import' \
                and item['member_id'] == str(member_id):
            return item['value']
    return None

# block_chain compare_nodes


def get_count_DB_objects(url, token):
    tables = {}
    list = api.tables(url, token, limit=1000)['list']
    for table in list:
        tables[table['name']] = table['count']
    return tables


def get_table_hashes(url, token, db_inf, ecos='1'):
    tables = {}
    list = api.tables(url, token, limit=1000)['list']
    for table in list:
        tables[table['name']] = db.get_table_hash(
            db_inf, ecos + '_' + table['name'])
    return tables


# done
def get_user_token_amounts(url, token):
    count = get_count(url, 'keys', token)
    keys = api.list(url, token, 'keys', limit=count)
    amounts = []
    for item in keys['list']:
        amounts.append(int(item['amount']))
    amounts.sort()
    return amounts


# cost
def get_balance_by_id(url, token, key_id, ecos=1):
    count = get_count(url, 'keys', token)
    keys = api.list(url, token, 'keys', limit=count)
    for item in keys['list']:
        if item['id'] == str(key_id) \
                and item['ecosystem'] == str(ecos):
            return item['amount']
    return None


# API
def is_wallet_created(url, token, id):
    count = get_count(url, 'keys', token)
    keys = api.list(url, token, 'keys', limit=count)
    for item in keys['list']:
        if item['id'] == str(id) \
                and int(item['amount']) == 1000000000000000000000:
            return True
    return False


# cost
def is_commission_in_history(url, token, id_from, id_to, summ):
    count = get_count(url, 'history', token)
    table = api.list(url, token, 'history', limit=count)
    for item in table['list']:
        if item['sender_id'] == str(id_from) \
                and item['recipient_id'] == str(id_to):
            if item['amount'] == str(summ):
                return True
    return False


def is_contract_present(url, token, name):
    ans = api.contract(url, token, name)
    if "error" not in ans:
        return True
    if ans['error'] == 'E_CONTRACT':
        return False
    else:
        return True


def imp_app(app_name, url, pr_key, token):
    log.info("Start install '" + app_name + "'")
    path = os.path.join(os.getcwd(), "fixtures", "basic", app_name + ".json")
    resp = call_contract(url, pr_key, "ImportUpload",
                         {'input_file': {'Path': path}}, token)
    res_import_upload = tx_status(url, wait, resp, token)
    if int(res_import_upload["blockid"]) > 0:
        founder_id = get_parameter_value(url, 'founder_account', token)
        bufer_data_list = get_list(url, 'buffer_data', token)['list']
        for item in bufer_data_list:
            if item['key'] == "import" and item['member_id'] == founder_id:
                import_app_data = json.loads(item['value'])['data']
                break
        contract_name = "Import"
        data = [{"contract": contract_name,
                 "params": import_app_data[i]} for i in range(len(import_app_data))]
        resp = call_multi_contract(url, pr_key, contract_name, data, token)
        time.sleep(wait)
        if "hashes" in resp:
            hashes = resp['hashes']
            result = tx_status_multi(url, wait, hashes, token)
            for status in result.values():
                log.debug(str(status))
                if int(status["blockid"]) < 1:
                    log.error("Import '" + app_name + "' is failed")
                    exit(1)
            log.info("App '" + app_name + "' successfully installed")


def get_load_blocks_time(url, token, max_block, wait_upating):
    sec = 1
    while sec < wait_upating:
        max_block_id1 = get_max_block_id(url, token)
        if max_block_id1 == max_block:
            print("Time: ", sec)
            return {"time": sec, "blocks": max_block_id1}
        else:
            sec = sec + 1
    return {"time": wait_upating + 1, "blocks": max_block_id1}
