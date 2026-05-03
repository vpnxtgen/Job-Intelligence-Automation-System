from simple_salesforce import Salesforce as sf
from Constant import Constant as const
from dotenv import load_dotenv
import os

class SFDataService:
    def __init__(self):
        print('Initializing SFDataService...')
        # Initialize connection as None to avoid AttributeErrors
        self.connection = None 
        load_dotenv()  # Load environment variables from .env file
        
    def connect(self):
        """Establishes the connection to Salesforce."""
        username = os.getenv(const.SF_VIK_1)
        password = os.getenv(const.SF_PASS_1)
        security_token = os.getenv(const.SF_TOKEN_1)
        print("Attempting to connect to Salesforce..." + username)
        try:
            self.connection = sf(
                username=username, 
                password=password, 
                security_token=security_token
            )
            print("Connected to Salesforce successfully.")
        except Exception as e:
            print(f"Failed to connect: {e}")
        
    def upsertDataIntoSf(self, json_data):
        """Upserts data. Note: json_data should be a single dict for standard upsert."""
        # Ensure we have a connection before proceeding
        if not self.connection:
            self.connect()

        try:
            # simple-salesforce upsert returns a status code (e.g., 201 or 204)
            # and potentially a body, but it doesn't return a list to iterate over 
            # unless you are using the Bulk API.
            
            for record in json_data:
                ext_id = record.get('App_Ext_Id__c')
                sf_record = self.normalize_record(record)
                if not ext_id:
                    print("Skipping record with missing ID")
                    continue
                
                result = self.connection.Job_Details__c.upsert( f'App_Ext_Id__c/{ext_id}', sf_record)
                
            
            # For standard REST API upsert:
            # 201 = Created, 204 = Updated
            if 200 <= result <= 299:
                print(f"Upsert successful. Status Code: {result}")
            else:
                print(f"Upsert returned unexpected status: {result}")
                
        except Exception as e:
            print(f"Upsert failed: {e}")
    
    def normalize_record(self,record):
        return {
            'Company_Name__c': str(record.get('Company_Name__c') or ''),
            'Employee_Size__c': str(record.get('Employee_Size__c')),
            'Career_Email_Id__c': str(record.get('Career_Email_Id__c') or ''),
            'Email_Draft__c': str(record.get('Email_Draft__c')),
            'Email_Subject__c': str(record.get('Email_Subject__c')),
            'Title__c': str(record.get('Title__c')),
            'Location__c': str(record.get('Location__c') or ''),
            'ReDirect_url__c': str(record.get('ReDirect_url__c') or ''),
            'Description__c' : str(record.get('Description__c') or ''),
            'ApplyUrl__c': str(record.get('ApplyUrl__c') or '')
        }



#SFDataService().connect()