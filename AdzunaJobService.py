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
                        print(f'Fetching jobs from: {serviceQuery}')
                        tasks.append(session.get(serviceQuery))
                    # Use a try block for the network request
                        #response = await client.get(serviceQuery, timeout=10)
                        
                        # Check for HTTP errors (4xx or 5xx)
                        #response.raise_for_status() 
                responses = await asyncio.gather(*tasks, return_exceptions=True)

                adzure_job_details = {}
                job_details = []
                
                for response in responses:
                    if isinstance(response, Exception):
                        print(f"Request failed: {response}")
                        continue
                    
                    async with response:
                        if response.status == 200:
                            jsonRes = await response.json() 
                            results.extend(jsonRes.get('results', []))
                        else : 
                            print(f"Error {response.status} from API")

                try:
                    print('results************', len(results))
                    for result in results:
                    # Using a nested try to ensure one bad record doesn't crash the loop
                        job_detail = {
                            'id': result.get('id'),
                            'company_name': result.get('company', {}).get('display_name'),
                            'title': result.get('title'),
                            'redirect_url': result.get('redirect_url'),
                            'description': result.get('description')
                        }
                        # Store as {id: data} as per your original structure
                        adzure_job_details[result.get('id')] = job_detail
                        job_details.append(job_detail)
                        
                    #print('job_detail*******************',len(job_detail))
                    if job_details:
                        llmResList =  await self.fetchCompanyInfo(job_details)
                        #print('llmResList************',llmResList)
                        if llmResList:
                        
                            for eRes in llmResList :
                                #print('eRes************',eRes) 
                                appId = eRes.get('application_id')
                                detail = adzure_job_details.get(appId)
                                if detail and detail.get('id') == appId:
                                    detail['employee_size'] = eRes.get('employee_size')
                                    detail['career_email_id'] = eRes.get('career_email_id')
                                    detail['email_draft'] = eRes.get('email_draft')
                                    
                            self.convertIntoExcel(list(adzure_job_details.values()))
                               
                except Exception as e:
                    print(f"Skipping a result due to format error: {e}")

                print(f'Successfully retrieved {len(adzure_job_details)} jobs.')
                print(f'Successfully retrieved {adzure_job_details} jobs.')
                return adzure_job_details

            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
            except requests.exceptions.ConnectionError:
                print("Error: Could not connect to the Adzuna API. Check your internet.")
            except requests.exceptions.Timeout:
                print("Error: The request timed out.")
            except Exception as err:
                print(f"An unexpected error occurred: {err}")
            
    async def fetchCompanyInfo(self, job_details):
        
        if job_details is None:
            raise ValueError("in the methood fetchCompanyInfo, job_details is empty.") 
        #GEMENI_AI_API_KEY_VIK_PUVV
        # GEMENI_API_KEY
        response = AIAgent(const.GEMENI_STUDIO_API_VIK_PRAN).gemeniAiConnect(job_details) 
        print('response+++++++++++++++++++++',response)  
            
        if response is None or len(response) == 0:
            raise ValueError(f"Response is empty from the llm, please check the connection")        
                #pd.json_normalize(jsonRes.get('results'))
                #df.to_excel('C:/Users/Cloud/Downloads/nested_output.xlsx', index=False
        return response
    
    def convertIntoExcel(self, final_json):
        # "C:\Users\Cloud\Downloads\ConsolidatedSheet27th1.xlsx"
        if final_json:
            df = pd.DataFrame(final_json)
            df.to_excel('C:/Users/Cloud/Downloads/job_search_details.xlsx', index=False)


class emailMessage:
    
    def __int__(self):
        print('email automation')
        
    def sendEmail(self):
        pass
             
            
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