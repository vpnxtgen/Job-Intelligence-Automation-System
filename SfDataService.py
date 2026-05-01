from simple_salesforce import Salesforce as sf
from Constant import Constant as const

class SFDataService:
    sfConnect 
    def __init__(self):
        print('inside the sf data')
        
    
    def sfConnect(self):
        self.sfConnect = sf(username= const.SF_VIK_1, password = const.SF_PASS_1 , security_token = const.SF_TOKEN_1)
        
    def upsertDataIntoSf(self,json_data):
        try:
            results = self.sfConnect.Job_Details__c.upsert(json_data, 'App_Ext_Id__c') 
           
           # 4. Handle Results
            for i, res in enumerate(results):
                if res['success']:
                    # 'created' will be True if it's a new record, False if updated
                    status = "Created" if res['created'] else "Updated"
                    print(f"Record {i}: {status} success.")
                else:
                    print(f"Record {i}: Error - {res['errors']}")
        
        except Exception as e:
            print(f"Upsert failed: {e}")