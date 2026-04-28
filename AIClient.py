from dotenv import load_dotenv
import os
from openai import OpenAI
from google import genai
import json

# key name to be used OPENAI_API_KEY  and GEMENI_API_KEY,GEMENI_AI_API_KEY_VIK_PUVV, GEMENI_STUDIO_API_VIK_PRAN

class AIClient:

    apikey :str 
    def __init__(self,env_var_name):
        print('inside the AI Client env_var_name ', env_var_name)
        load_dotenv()
        self.ApiKey =  env_var_name
    
    @property
    def ApiKey(self):
        return self.apikey
    
    @ApiKey.setter
    def ApiKey(self,value):
        self.apikey = os.getenv(value) 
        print('os.getenv(value)*************',self.apikey)
        
        if self.apikey is None:
            raise f"please assign the value for self.ApiKey"
        
    def openAiConnect(self):
        #client = OpenAI( api_key=os.environ.get(self.__apikey) )
        
        client = OpenAI(api_key = self.__apikey)
        
        # 2. Call the chat completions method
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
        
        # 3. Access the generated content
        print(response)
        
    def gemeniAiConnect(self, request):
        
        #print('request*******************',request)
        
        client = genai.Client(api_key=self.ApiKey)
        prompt = f"Could you please share the estimated total employee size of the company and, if available, the careers/contact email ID? Additionally, please include the corresponding application ID in the response for reference. : {request}"
        # Generate a simple text response
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
            config={
                'response_mime_type' : 'application/json',
                'response_schema' : {
                    'type' : 'ARRAY',
                    'items' : {
                        'type' : 'OBJECT',
                        'properties' : {
                            'application_id' : {'type': 'STRING'},
                            'company_name' : {'type': 'STRING'},
                            'employee_size' : {'type': 'STRING'},
                            'career_email_id' : {'type': 'STRING'}
                        },
                        'required': ['application_id', 'company_name', 'employee_size', 'career_email_id']
                    }
                }
            }
        )

        # Print the generated text
        print('response.text******************',response.text)
        
        if response.text is not None:
            res = json.loads(response.text)
            print('res******************',type(res))
            return res
        
        return None
        
    def gemeniAiTokenCount(self):
        client = genai.Client(api_key=self.ApiKey)
        tokens = client.models.count_tokens(model='gemini-3-flash-preview', contents="Hello world")
        print(f"Cost: {tokens.total_tokens} tokens")
        


       
    