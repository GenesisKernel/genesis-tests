import unittest
import utils
import config
import json
import time
import funcs
import os


class Rollback1TestCase(unittest.TestCase):
    
    def call(self, name, data):
        resp = utils.call_contract(url, prKey, name, data, token)
        res = utils.txstatus(url, waitTx,
                       resp['hash'], token)
        return res
        
    def create_contract(self, data):
        code,name = utils.generate_name_and_code("")
        dataC = {}
        if data == "":
            dataC = {"Wallet": '',
                     "Value": code,
                     "Conditions": "ContractConditions(`MainCondition`)"}
        else:
            dataC = data
        res = self.call("NewContract", dataC)
        return name, code
        
    def create_ecosystem(self):
        data = {"Name": "Ecosys" + utils.generate_random_name()}
        res = self.call("NewEcosystem", data)
        
    def money_transfer(self):
        data = {"Recipient": "0005-2070-2000-0006-0200",
                "Amount": "1000"}
        res = self.call("MoneyTransfer", data)
        
        
    def edit_contract(self,contract, code):
        data2 = {"Id": funcs.get_contract_id(url, contract, token),
                 "Value": code,
                 "Conditions": "true",
                 "WalletId": "0005-2070-2000-0006-0200"}
        res = self.call("EditContract", data2)
        
    def activate_contract(self, name):
        data = {"Id": funcs.get_contract_id(url, name, token)}
        res = self.call("ActivateContract", data)
        
    def deactivate_contract(self, name):
        data = {"Id": funcs.get_contract_id(url, name, token)}
        res = self.call("DeactivateContract", data)
        
    def new_parameter(self):
        name = "Par_" + utils.generate_random_name()
        data = {"Name": name,
                "Value": "test", "Conditions": "true"}
        res = self.call("NewParameter", data)
        return name
    
    def edit_parameter(self, name):
        data = {"Id": funcs.get_parameter_id(url, name, token),
                "Value": "test_edited", "Conditions": "true"}
        res = self.call("EditParameter", data)
        
    def new_menu(self):
        name = "Menu_" + utils.generate_random_name()
        data = {"Name": name,
                "Value": "Item1", "Conditions": "true"}
        res = self.call("NewMenu", data)
        return name
    
    def edit_menu(self):
        dataEdit = {"Id": funcs.get_count(url, "menu", token),
                    "Value": "ItemEdited", "Conditions": "true"}
        res = self.call("EditMenu", dataEdit)
        
    def append_memu(self):
        count = funcs.get_count(url, "menu", token)
        dataEdit = {"Id": funcs.get_count(url, "menu", token),
                    "Value": "AppendedItem", "Conditions": "true"}
        res = self.call("AppendMenu", dataEdit)
        
    def new_page(self):
        data = {"Name": "Page_" + utils.generate_random_name(),
                "Value": "Hello page!",
                "Conditions": "true",
                "Menu": "default_menu"}
        res = self.call("NewPage", data)
        
    def edit_page(self):
        dataEdit = {"Id": funcs.get_count(url, "pages", token),
                    "Value": "Good by page!",
                    "Conditions": "true",
                    "Menu": "default_menu"}
        res = self.call("EditPage", dataEdit)
        
    def append_page(self):
        count = funcs.get_count(url, "pages", token)
        dataEdit = {"Id": funcs.get_count(url, "pages", token),
                    "Value": "Good by!",
                    "Conditions": "true",
                    "Menu": "default_menu"}
        res = self.call("AppendPage", dataEdit)
        
    def new_block(self):
        name = "Block_" + utils.generate_random_name()
        data = {"Name": name, "Value": "Hello page!",
                "Conditions": "true"}
        res = self.call("NewBlock", data)
        
    def edit_block(self):
        count = funcs.get_count(url, "blocks", token)
        dataEdit = {"Id": count, "Value": "Good by!",
                    "Conditions": "true"}
        res = self.call("EditBlock", dataEdit)
        
    def new_table(self):
        column = """[{"name":"MyName","type":"varchar",
        "index": "1","conditions":"true"}]"""
        permission = """{"insert": "false",
        "update" : "true","new_column": "true"}"""
        data = {"Name": "Tab_" + utils.generate_random_name(),
                "Columns": column,
                "Permissions": permission}
        res = self.call("NewTable", data)
        return data["Name"]

    def edit_table(self, name):
        column = """[{"name":"MyName","type":"varchar",
        "index": "1","conditions":"true"}]"""
        permission = """{"insert": "true",
        "update" : "true","new_column": "true"}"""
        dataEdit = {"Name": name,
                    "Columns": column,
                    "Permissions": permission}
        res = self.call("EditTable", dataEdit)

    def new_column(self, table):
        name = "Col_" + utils.generate_random_name()
        dataCol = {"TableName": table,
                   "Name": name,
                   "Type": "number",
                   "Index": "0",
                   "Permissions": "true"}
        res = self.call("NewColumn", dataCol)
        return name

    def edit_column(self, table, column):
        dataEdit = {"TableName": table, "Name": column,
                    "Permissions": "false"}
        res = self.call("EditColumn", dataEdit)

    def new_lang(self):
        name = "Lang_" + utils.generate_random_name()
        data = {"Name": name,
                "Trans": "{\"en\": \"false\", \"ru\" : \"true\"}"}
        res = self.call("NewLang", data)
        return name

    def edit_lang(self, name):
        dataEdit = {"Name": name,
                    "Trans": "{\"en\": \"true\", \"ru\" : \"true\"}"}
        res = self.call("EditLang", dataEdit)

    def new_sign(self):
        name = "Sign_" + utils.generate_random_name()
        value = "{ \"forsign\" :\"" + name
        value += "\" ,  \"field\" :  \"" + name
        value += "\" ,  \"title\": \"" + name
        value += "\", \"params\":[{\"name\": \"test\", \"text\": \"test\"}]}"
        data = {"Name": name,
                "Value": value,
                "Conditions": "true"}
        res = self.call("NewSign", data)
        return name

    def edit_sign(self, name):
        count = funcs.get_count(url, "signatures", token)
        valueE = "{ \"forsign\" :\"" + name
        valueE += "\" ,  \"field\" :  \"" + name
        valueE += "\" ,  \"title\": \"" + name
        valueE += "\", \"params\":[{\"name\": \"test\", \"text\": \"test\"}]}"
        dataEdit = {"Id": funcs.get_count(url, "signatures", token),
                   "Value": valueE,
                   "Conditions": "true"}
        res = self.call("EditSign", dataEdit)
        
    def test_rollback1(self):
        global url, prKey, token, waitTx
        self.conf = config.readMainConfig()
        url = self.conf["url"]
        prKey = self.conf['private_key']
        host = self.conf["dbHost"]
        db = self.conf["dbName"]
        login = self.conf["login"]
        pas = self.conf["pass"]
        waitTx = self.conf["time_wait_tx_in_block"]
        dbInformation = utils.getCountDBObjects(host, db, login, pas)
        file = os.path.join(os.getcwd(), "dbState.json")
        with open(file, 'w') as fconf:
            json.dump(dbInformation, fconf)
        lData = utils.login(url, prKey)
        token = lData["jwtToken"]
        self.create_ecosystem()
        self.money_transfer()
        contract,code = self.create_contract("")
        self.edit_contract(contract,code)
        self.activate_contract(contract)
        self.deactivate_contract(contract)
        param = self.new_parameter()
        self.edit_parameter(param)
        menu = self.new_menu()
        self.edit_menu()
        self.append_memu()
        self.new_page()
        self.edit_page()
        self.append_page()
        self.new_block()
        self.edit_block()
        table = self.new_table()
        self.edit_table(table)
        column = self.new_column(table)
        self.edit_column(table, column)
        lang = self.new_lang()
        self.edit_lang(lang)
        sign = self.new_sign()
        self.edit_sign(sign)
        time.sleep(20)
        
if __name__ == "__main__":
    unittest.main()
        