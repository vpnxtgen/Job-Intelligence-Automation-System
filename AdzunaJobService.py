import json
from dataclasses import dataclass
from urllib.parse import urlencode
import requests
import pandas as pd
'''
 @Description : Adzure job service to get the job details from adzune api.
 
'''

@dataclass
class AdzureApiParam:
    category : str 
    max_days_old : str 
    what : str 
    where : str 
    sort_by : str
    country : str
    page : str 
    

    

class AdzunaJobService:
    
    __appId = '4caafcbc' 
    __apikey =  '56c1aeb4801d7f49e3bb39c38d56f270'
    def __init__(self,):
        print('Inside the Adzure job service constructor')
        
    def parse_data(self, paramjSON : str) -> AdzureApiParam :
        data = json.loads(paramjSON)
        print('data**********',data.get('category'))
        if data:
            return AdzureApiParam(
                category  = data.get('category','it-jobs'),
                max_days_old = data.get("max_days_old",2),
                what = data.get("what","salesforce developer"),
                where = data.get("where","Bengaluru OR Hyderabad"),
                sort_by = data.get("sort_by","date"),
                country= data.get("country","in"),
                page = data.get("page","1")
            )
    
    def job_search(self, json_data):
        if json_data:
            params = self.parse_data(json_data)
            
            base_url = f"https://api.adzuna.com/v1/api/jobs/{params.country}/search/{params.page}?"
            
            query_params = {
                "app_id" : self.__appId,
                "app_key" : self.__apikey,
                "category" : params.category,
                "max_days_old" : params.max_days_old,
                "what" : params.what,
                "where" : params.where,
                "sort_by" : params.sort_by
            }
            
            serviceQuery = base_url +urlencode(query_params)
            
            print('serviceQuery*******************',serviceQuery)
            
            response = requests.get(serviceQuery, timeout=10)
            
            if response.status_code == 200 :
                
                #print('response code****************',response.status_code)
                #print('response body****************',response.json())
                
                jsonRes =  response.json() 
                #print('response result****************',jsonRes.get('results'))
                job_details = []
                if jsonRes.get('results'):
                    for result in jsonRes.get('results'):
                        job_detail = dict();
                        job_detail['id'] = result.get('id')
                        company = result.get('company')
                        job_detail['company_name'] = company.get('display_name')
                        job_detail['title'] = result.get('title')
                        job_details.append(job_detail)
                        
                print('job_details*****************',job_details)
                
                #df = pd.json_normalize(jsonRes.get('results'))
                
                #df.to_excel('C:/Users/Cloud/Downloads/nested_output.xlsx', index=False)
                
                
        
    
service =  AdzunaJobService()

json_input = json_input = '''
{
  "category": "it-jobs",
  "max_days_old": 2,
  "what": "salesforce developer",
  "where": "Bengaluru OR Hyderabad",
  "sort_by": "date"
}
'''

service.job_search(json_input)
#print('params********************',params.category)
        



    

    