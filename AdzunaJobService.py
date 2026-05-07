import json
from dotenv import load_dotenv
import os
import httpx
import asyncio
import aiohttp
from dataclasses import dataclass
from urllib.parse import urlencode
import requests
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from AIClient import AIClient as AIAgent # Commented out as per original context
from Constant import Constant as const
from EmailSender import EmailSender as sender
from SfDataService import SFDataService as sfData



# ADZUNE_APP_ID AND ADZUNE_API_KEY , GoogleAppPassword_Vik_Puv
@dataclass
class AdzureApiParam:
    category: str 
    max_days_old: str 
    what: str 
    where: str 
    sort_by: str
    country: str
    page: str 
    

class AdzunaJobService:
    __appId : str
    __apikey : str
    _search_data = str

    def __init__(self, data : str):
        print('Inside the Adzure job service constructor')
        load_dotenv()
        self.__appId = os.getenv(const.ADZUNE_APP_ID)
        self.__apikey = os.getenv(const.ADZUNE_API_KEY)
        self._search_data = data
        
    def parse_data(self, paramjSON: str) -> AdzureApiParam:
        try:
            data = json.loads(paramjSON)
            if not data:
                raise ValueError("JSON input is empty")
            
            return AdzureApiParam(
                category=data.get('category', 'it-jobs'),
                max_days_old=data.get("max_days_old", 2),
                what=data.get("what", "salesforce developer"),
                where=data.get("where", "Bengaluru OR Hyderabad"),
                sort_by=data.get("sort_by", "date"),
                country=data.get("country", "in"),
                page=data.get("page", "1")
            )
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format provided - {e}")
            return None
        except Exception as e:
            print(f"Error occurred during parsing: {e}")
            return None
    
    async def job_search(self, pageRange):
        params = self.parse_data(self._search_data)
        if not params:
            print("Job search aborted due to invalid parameters.")
            return
        if pageRange is None:
            raise ValueError('Please assign the pageRange Value')
        async with aiohttp.ClientSession() as session:
            tasks = []
            try: 
                results : list = []
                for i in range(1,pageRange):
                        base_url = f"https://api.adzuna.com/v1/api/jobs/{params.country}/search/{i}?"
                        query_params = {
                            "app_id": self.__appId,
                            "app_key": self.__apikey,
                            "category": params.category,
                            "max_days_old": params.max_days_old,
                            "what": params.what,
                            "where": params.where,
                            "sort_by": params.sort_by
                        }
                    
                        serviceQuery = base_url + urlencode(query_params)
                        #print(f'Fetching jobs from: {serviceQuery}')
                        tasks.append(session.get(serviceQuery))
                    # Use a try block for the network request
                        #response = await client.get(serviceQuery, timeout=10)
                        
                        # Check for HTTP errors (4xx or 5xx)
                        #response.raise_for_status() 
                results = await self.aiohttpGet(tasks)  #await asyncio.gather(*tasks, return_exceptions=True)     
                adzure_job_details = {}
                job_details = []
                

                try:
                    print('results************', len(results))
                    for result in results:
                    # Using a nested try to ensure one bad record doesn't crash the loop
                        job_detail = {
                            'App_Ext_Id__c': result.get('id'),
                            'Company_Name__c': result.get('company', {}).get('display_name'),
                            'Title__c': result.get('title'),
                            'ReDirect_url__c': result.get('redirect_url'),
                            'Description__c': result.get('description'),
                            'location__c' : result.get('location','Bengalore'),
                            'ApplyUrl__c' : result.get('applyUrl','https://www.google.com/search'),
                            'publishedAt__c' : result.get('created',None)
                        }
                        # Store as {id: data} as per your original structure
                        adzure_job_details[result.get('id')] = job_detail
                        job_details.append(job_detail)
                        
                    #print('job_detail*******************',len(job_detail))
                    if job_details:
                        llmResList =  await self.fetchCompanyInfo(job_details)
                        #print('llmResList************',llmResList[0:3])
                        if llmResList:
                            for eRes in llmResList :
                                #print('eRes************',eRes) 
                                appId = eRes.get('App_Ext_Id__c')
                                detail = adzure_job_details.get(appId)
                                if detail and detail.get('App_Ext_Id__c') == appId:
                                    detail['Employee_Size__c'] = eRes.get('Employee_Size__c')
                                    detail['Career_Email_Id__c'] = eRes.get('Career_Email_Id__c')
                                    detail['Email_Draft__c'] = eRes.get('Email_Draft__c')
                                    detail['Email_Subject__c'] = eRes.get('Email_Subject__c')
                            
                            #sender().send_email(list(adzure_job_details.values()))       
                            self.convertIntoExcel(list(adzure_job_details.values()))
                            self.insertIntoSf(list(adzure_job_details.values()))    
                            
                               
                except Exception as e:
                    print(f"Skipping a result due to format error: {e}")

                print(f'Successfully retrieved {len(adzure_job_details)} jobs.')
                #print(f'Successfully retrieved {adzure_job_details} jobs.')
                return adzure_job_details

            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
            except requests.exceptions.ConnectionError:
                print("Error: Could not connect to the Adzuna API. Check your internet.")
            except requests.exceptions.Timeout:
                print("Error: The request timed out.")
            except Exception as err:
                print(f"An unexpected error occurred: {err}")
                                
    async def aiohttpGet(self, tasks):
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_results = []

        for response in responses:
            if isinstance(response, Exception):
                print(f"Request failed: {response}")
                continue

            async with response:
                if response.status == 200:
                    jsonRes = await response.json()
                    all_results.extend(jsonRes.get('results', []))
                else:
                    print(f"Error {response.status} from API")

        return all_results
    
    async def aiohttpPost(self, baseUrl , payload):
        print('baseUrl******************')
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(baseUrl, json=payload) as response:
                    response.raise_for_status()
                    return await response.json()

        except aiohttp.ClientError as e:
            print("HTTP Error:", e)
        except Exception as e:
            print("Unexpected error:", e)
        
            
    async def fetchCompanyInfo(self, job_details):
        
        if job_details is None:
            raise ValueError("in the methood fetchCompanyInfo, job_details is empty.") 
        #GEMENI_AI_API_KEY_VIK_PUVV
        # GEMENI_API_KEY
        response = AIAgent(const.GEMENI_API_KEY).gemeniAiConnect(job_details) 
        print('response+++++++++++++++++++++',response)  
            
        if response is None or len(response) == 0:
            raise ValueError(f"Response is empty from the llm, please check the connection")        
                #pd.json_normalize(jsonRes.get('results'))
                #df.to_excel('C:/Users/Cloud/Downloads/nested_output.xlsx', index=False
        return response
    
    def convertIntoExcel(self, final_json):
        file_path = 'C:/Users/Cloud/Downloads/job_search_details.xlsx'

        if final_json:
            df = pd.DataFrame(final_json)

            try:
                # Append to existing file
                with pd.ExcelWriter(file_path, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                    df.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)
            except FileNotFoundError:
                # If file doesn't exist, create new
                df.to_excel(file_path, index=False)
    
    def insertIntoSf(self, json_data):
        try:
            print('inside the insertIntoSf method******************')
            sfDataService = sfData()
            sfDataService.connect()
            sfDataService.upsertDataIntoSf(json_data)
        except Exception as e:
            print(f"Error inserting into Salesforce: {e}")
    
async def main():
    # Execution
    json_input = '''
    {
    "category": "it-jobs",
    "max_days_old": 2,
    "what": "salesforce+developer",
    "where": "Bengaluru OR Hyderabad",
    "sort_by": "date"
    }
    '''
    service = AdzunaJobService(json_input)
    companyInfo = await service.job_search(2)
#print(f'companyInfo************* {companyInfo}')


if __name__ == "__main__":
    asyncio.run(main())