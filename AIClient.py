from dotenv import load_dotenv
import os
from openai import OpenAI
from google import genai
import json

class AIClient:
    apikey: str 

    def __init__(self, env_var_name):
        try:
            print('inside the AI Client env_var_name ', env_var_name)
            load_dotenv()
            self.ApiKey = env_var_name
        except Exception as e:
            print(f"Error during initialization: {e}")

    @property
    def ApiKey(self):
        return self.apikey
    
    @ApiKey.setter
    def ApiKey(self, value):
        self.apikey = os.getenv(value)
        if self.apikey is None:
            # Fixed: raising a ValueError instead of just a string
            raise ValueError(f"Environment variable {value} not found. Please assign the value.")
        
    def openAiConnect(self):
        try:
            client = OpenAI(api_key=self.apikey)
            response = client.responses.create(
                model="gpt-5.5",
                input=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": "What teams are playing in this image?",
                            },
                            {
                                "type": "input_image",
                                "image_url": "https://api.nga.gov/iiif/a2e6da57-3cd1-4235-b20e-95dcaefed6c8/full/!800,800/0/default.jpg"
                            }
                        ]
                    }
                ]
            )
            print(response)
        except Exception as e:
            print(f"OpenAI Connection Error: {e}")
        
    def gemeniAiConnect(self, request):
        try:
            client = genai.Client(api_key=self.ApiKey)
            '''prompt = f"Could you please share the estimated total employee size of the company and, if available, the careers/contact email ID? Additionally, please include the corresponding application ID in the response for reference, : {request}"
            prompt += f" Also, a professional draft email tailored to the job description. " '''
            
            prompt = (
                f"Analyze the following job details: {request}. "
                "For each job, provide the following information in a valid JSON list format:\n"
                "1. 'App_Ext_Id__c': The ID provided in the request.\n"
                "2. 'Employee_Size__c': Estimated total employee count.\n"
                "3. 'Career_Email_Id__c': Best contact email for applications.\n"
                "4. 'Email_Draft__c': A professional, concise email draft applying for this role. "
                "5. 'Email_Subject__c': A professional email subject to be added based on job description."
                "The email must be from 'Vikranth Puvvadi' and tailored to the job description provided."
                "The email must include the skills like Salesforce Integrations (REST, Bulk, Composite, Metadata, GraphQL, SAP, OAuth 2.0, Platform Events, CDC, Streaming API, Named/External Credentials, Connected Apps), Apex & Asynchronous Processing (Triggers, Batch, Queueable, Scheduled, Future, Governor Limit Optimization, Bulkification), Lightning Architecture (LWC, LDS, Wire Adapters, LMS, ES6, Reusable Components), Automation & Service Cloud (Flows, Approval Processes, Omni-Channel, Case Management), Multi-Cloud Expertise (Sales, Service, Experience, Education, Revenue Clouds), Data Modeling & Security Architecture (Schema Design, Sharing Rules, Permission Sets, OWD, FLS), and Deployment/Data Tools (Git, Copado, Change Sets, Workbench, Data Loader)."
            )
            
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt,
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': {
                        'type': 'ARRAY',
                        'items': {
                            'type': 'OBJECT',
                            'properties': {
                                'App_Ext_Id__c': {'type': 'STRING'},
                                'Company_Name__c': {'type': 'STRING'},
                                'Employee_Size__c': {'type': 'STRING'},
                                'Career_Email_Id__c': {'type': 'STRING'},
                                'Email_Draft__c': {'type': 'STRING'},
                                'Email_Subject__c' : {'type': 'STRING'}
                            },
                            'required': ['App_Ext_Id__c', 'Company_Name__c', 'Employee_Size__c', 'Career_Email_Id__c', 'Email_Draft__c', 'Email_Subject__c']
                        }
                    }
                }
            )

            print('response.text******************', response.text)
            
            if response.text:
                res = json.loads(response.text)
                print('res******************', type(res))
                return res
                
        except json.JSONDecodeError as je:
            print(f"JSON Parsing Error: {je}")
        except Exception as e:
            print(f"Gemini Connection Error: {e}")
        
        return None
        
    def gemeniAiTokenCount(self):
        try:
            client = genai.Client(api_key=self.ApiKey)
            tokens = client.models.count_tokens(model='gemini-3-flash-preview', contents="Hello world")
            print(f"Cost: {tokens.total_tokens} tokens")
        except Exception as e:
            print(f"Error counting tokens: {e}")