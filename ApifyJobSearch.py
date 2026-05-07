from apify_client import ApifyClient
from AdzunaJobService import AdzunaJobService as aSyncApiService
import aiohttp
import asyncio
from EmailSender import EmailSender as sender
from Constant import Constant as const
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
import os

class apifyjobsearch:
    
    api_key :str
    author_name = 'cheap_scraper/linkedin-job-scraper'
    actor_id : str
    aSyncApiService 
    def __init__(self):
        load_dotenv()
        self.aSyncApiService = aSyncApiService('{}')
        self.api_key = os.getenv('APIFY_API_KEY') 
        self.author_name = os.getenv(const.APIFY_ACTOR_ID) 
        #print('apify job search*******************8',self.api_key)
    
    
    def linkedinJobSearchAutor(self):
        try:
           

            # Initialize the ApifyClient with your API token
            client = ApifyClient(self.api_key)

            # Prepare the Actor input
            run_input = self.parse_data()

            # Run the Actor and wait for it to finish
            run = client.actor(self.actor_id).call(run_input=run_input)

            # Fetch and print Actor results from the run's dataset (if there are any)
            items = []
            for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                items.append(item)
            
            print('items***********',items)
        except Exception as e:
            print (f"error is {e}")
            
    def parse_data(self):
        
        return {"enrichCompanyData": False, "keyword": ["Salesforce Developer", "Salesforce Engineer", "Salesforce Consultant", "SFDC Developer"], "location": "India", "maxItems": 150, "publishedAt": "r86400", "resumeKeywords": [{"keyword": "Salesforce", "aliases": ["SFDC"]}, {"keyword": "Apex"}, {"keyword": "LWC"}, {"keyword": "SOQL"}, {"keyword": "Lightning"}], "saveOnlyUniqueItems": True, "startUrls": [{"url": "https://www.linkedin.com/jobs/search/?keywords=salesforce%20developer&location=India"}]};

    
    async def linkdinJobSearchDetails(self):
        
        end_point = f'https://api.apify.com/v2/acts/cheap_scraper~linkedin-job-scraper/run-sync-get-dataset-items?token={self.api_key}'
        payload = self.parse_data()
        try : 
            job_details = {}
            responses = await self.aSyncApiService.aiohttpPost(end_point , payload )  
            ''' 
            [
                    {
                        "jobId": "4406464434",
                        "jobTitle": "SF Architect - lifescience",
                        "location": "Pune City, Maharashtra, India",
                        "salaryInfo": [],
                        "postedTime": "19 hours ago",
                        "publishedAt": "2026-04-30T00:00:00.000Z",
                        "searchString": "Salesforce Consultant - India",
                        "jobUrl": "https://in.linkedin.com/jobs/view/sf-architect-lifescience-at-persistent-systems-4406464434?trk=public_jobs_topcard-title",
                        "companyName": "Persistent Systems",
                        "companyUrl": "https://in.linkedin.com/company/persistent-systems?trk=public_jobs_topcard-org-name",
                        "companyLogo": "https://media.licdn.com/dms/image/v2/D4D0BAQHC3yzoDWBD3Q/company-logo_100_100/B4DZzV.Y2BIwAQ-/0/1773116428185/persistent_systems_logo?e=2147483647&v=beta&t=onpHtprGZL-QUM-qRjoeSOgtv6Rd4uhpFK8l6Ucv3JY",
                        "jobDescription": "About Position: \n\n7+yrs Experience Salesforce developer with strong experience with apex, platform events, triggers, Visualforce, Lightning Web Components, security model, RESTful APIs, and declarative tools.\n\nRole: SF Architect - lifescience\nLocation: All location\nExperience: 8 to 16 years \nJob Type: Full Time Employment\n\nWhat You'll Do: \n\nThe End to End Solution Architect will own the overall solution integrity for a large, multi track Hub transformation program.\nThis role ensures that business outcomes, operational workflows, data, integrations, and platform capabilities come together into a cohesive, scalable, and differentiated solution.\nThis is not a domain siloed architect role. The expectation is a customer first, outcome driven mindset with accountability across CRM, portals, data, integrations, and operational impact.\nOwn the end to end solution architecture across Hub workflows, CRM, portals, data, analytics, and integrations\nTranslate business and operational outcomes (e.g., time to therapy, productivity, scalability) into solution designs\nAct as the single architectural thread across platform, UX, data, and delivery teams\nDrive architectural trade offs and resolve cross track dependencies\nEnsure solutions optimize for operational leverage, not just technical correctness\nPartner closely with Product Owners, Ops stakeholders, and delivery leadership\nGovern solution consistency while enabling configuration driven flexibility\nIdentify and mitigate architectural risks proactively Required Experience\n\nExpertise You'll Bring: \n\n12+ years of experience in enterprise solution or platform architecture\nStrong experience with workflow centric and CRM led platforms\nProven leadership on complex, multi system transformations\nDeep integration, data flow, and system of record design expertise\nAbility to influence senior stakeholders and operate in ambiguity\nRequired / Preferred Certifications Required (at least one):TOGAF Certification (Level 1 or Level 2)\nSalesforce Certified Technical Architect (CTA) or Salesforce Certified Application/System Architect (progress toward CTA acceptable)\nPreferred: SAFe Architect or SAFe Program Consultant (SPC) Healthcare or Life Sciencesspecific architecture certifications (where applicable)\n\nBenefits:\n\nCompetitive salary and benefits package\nCulture focused on talent development with quarterly growth opportunities and company-sponsored higher education and certifications\nOpportunity to work with cutting-edge technologies\nEmployee engagement initiatives such as project parties, flexible work hours, and Long Service awards\nAnnual health check-ups\nInsurance coverage: group term life, personal accident, and Mediclaim hospitalization for self, spouse, two children, and parents\n\nValues-Driven, People-Centric & Inclusive Work Environment:\n\nPersistent is dedicated to fostering diversity and inclusion in the workplace. We invite applications from all qualified individuals, including those with disabilities, and regardless of gender or gender preference. We welcome diverse candidates from all backgrounds.\n\nWe support hybrid work and flexible hours to fit diverse lifestyles.\nOur office is accessibility-friendly, with ergonomic setups and assistive technologies to support employees with physical disabilities.\nIf you are a person with disabilities and have specific requirements, please inform us during the application process or at any time during your employment\n\nLet's unleash your full potential at Persistent - persistent.com/careers\n\n\"Persistent is an Equal Opportunity Employer and prohibits discrimination and harassment of any kind.\"\nShow more Show less",
                        "applicationsCount": "Be among the first 25 applicants",
                        "contractType": "Full-time",
                        "experienceLevel": "Mid-Senior level",
                        "yearsOfExperience": [
                            {
                                "years": "12+",
                                "context": "in enterprise solution or platform architecture",
                                "lang": "en"
                            }
                        ],
                        "workType": "Engineering and Information Technology",
                        "sector": "IT Services and IT Consulting",
                        "posterFullName": "",
                        "posterProfileUrl": "",
                        "companyId": "5034",
                        "applyUrl": "https://in.linkedin.com/jobs/view/sf-architect-lifescience-at-persistent-systems-4406464434?trk=public_jobs_topcard-title",
                        "applyType": "EASY_APPLY",
                        "matchedKeywords": [
                            "Salesforce",
                            "Apex",
                            "Lightning"
                        ],
                        "unmatchedKeywords": [
                            "LWC",
                            "SOQL"
                        ],
                        "keywordMatchScorePercentage": 60
                    },
                    {
                        "jobId": "4407330887",
                        "jobTitle": "Business Analyst",
                        "location": "Bengaluru, Karnataka, India",
                        "salaryInfo": [],
                        "postedTime": "19 hours ago",
                        "publishedAt": "2026-04-30T00:00:00.000Z",
                        "searchString": "Salesforce Consultant - India",
                        "jobUrl": "https://in.linkedin.com/jobs/view/business-analyst-at-scoutit-4407330887?trk=public_jobs_topcard-title",
                        "companyName": "Scoutit",
                        "companyUrl": "https://in.linkedin.com/company/scoutit-in?trk=public_jobs_topcard-org-name",
                        "companyLogo": "https://media.licdn.com/dms/image/v2/D560BAQGbgOvn2002Gw/company-logo_100_100/B56Zl31VPfHQAQ-/0/1758652093991/scoutit_in_logo?e=2147483647&v=beta&t=dCA8DUthfJpCcZnA5TI0DZwlcXQ4SKkeic2EoHjTy5g",
                        "jobDescription": "We're looking for Business Analysts!\n\nResponsibilities\n\nGather and Analyze Requirements: Facilitate requirement workshops to gather and document business requirements, utilizing strong impact analysis and gap analysis abilities to ensure effective stakeholder management.\nMap Processes and Use Cases: Develop process and use case maps to analyze business cases and guide technical and vendor teams in delivering solutions that meet business needs.\nCommunicate with Stakeholders: Liaise between lines of business and the development team, articulating complex ideas clearly and persuasively to ensure seamless collaboration and solution delivery.\nManage Stakeholder Expectations: Effectively manage stakeholders and users throughout the project lifecycle, ensuring their needs are met and expectations are exceeded.\nGuide Technical Teams: Analyze business cases and provide guidance to technical teams to ensure solutions meet business requirements and are delivered on time.\n\n(*Note: This is a requirement for one of Scout's clients)\n\nSkills: business analysis,teams,business requirements,gap analysis \nShow more Show less",
                        "applicationsCount": "Be among the first 25 applicants",
                        "contractType": "Full-time",
                        "experienceLevel": "Entry level",
                        "yearsOfExperience": [],
                        "workType": "Research, Analyst, and Information Technology",
                        "sector": "Technology, Information and Internet",
                        "posterFullName": "",
                        "posterProfileUrl": "",
                        "companyId": "106321320",
                        "applyUrl": "https://in.linkedin.com/jobs/view/business-analyst-at-scoutit-4407330887?trk=public_jobs_topcard-title",
                        "applyType": "EASY_APPLY",
                        "matchedKeywords": [],
                        "unmatchedKeywords": [
                            "Salesforce",
                            "Apex",
                            "LWC",
                            "SOQL",
                            "Lightning"
                        ],
                        "keywordMatchScorePercentage": 0
                    },
                    {
                        "jobId": "4329027888",
                        "jobTitle": "Business Analyst",
                        "location": "Chennai, Tamil Nadu, India",
                        "salaryInfo": [],
                        "postedTime": "10 hours ago",
                        "publishedAt": "2026-04-30T00:00:00.000Z",
                        "searchString": "Salesforce Consultant - India",
                        "jobUrl": "https://in.linkedin.com/jobs/view/business-analyst-at-citi-4329027888?trk=public_jobs_topcard-title",
                        "companyName": "Citi",
                        "companyUrl": "https://www.linkedin.com/company/citi?trk=public_jobs_topcard-org-name",
                        "companyLogo": "https://media.licdn.com/dms/image/v2/D4E0BAQFgF4xtqyXBcg/company-logo_100_100/company-logo_100_100/0/1719257286385/citi_logo?e=2147483647&v=beta&t=E0LjmXX_MaMB3pwg6W_ragjyCPSpChEG51ham_xSNVc",
                        "jobDescription": "Job Description:\n\nRole Summary\n\nSeeking an experienced Business Analyst to define requirements, enhance processes, and support technology initiatives across Cards, Payments, or Retail Banking functions. The role involves partnering with business and technology teams to deliver efficient, compliant, and scalable solutions.\n\nKey Responsibilities\n\nGather, analyze, and document business and functional requirements (BRD, FRD, User Stories).\nTranslate business needs into clear system specifications and acceptance criteria.\nCollaborate with stakeholders, conduct workshops, and support Agile/Scrum ceremonies.\nAnalyze current processes, identify gaps, and recommend improvements or automation.\nPrepare process flows, reports, presentations, and support decision-making.\nCreate test plans, test cases, and support System Testing and UAT.\nTrack and resolve issues using tools like JIRA, Confluence, and collaborate with IT teams.\nAssess risks, ensure compliance, and maintain transparency in reporting.\nCandidates must be willing to work night shifts, with working hours beginning at 6:00 PM IST\n\nQualifications\n\n8–12 years of Business Analysis experience, preferably in Cards, Payments, or Retail Banking.\nStrong skills in data analysis and MS Office (Excel, PowerPoint).\nExperience with BA tools: JIRA, Confluence, Visio, process mapping, and documentation.\nStrong communication, analytical thinking, and stakeholder management abilities.\nBachelor’s degree or equivalent experience.\n\n------------------------------------------------------\n\nJob Family Group: \n\nTechnology\n\n------------------------------------------------------\n\nJob Family:\n\nBusiness Analysis / Client Services\n\n------------------------------------------------------\n\nTime Type:\n\n------------------------------------------------------\n\nMost Relevant Skills\n\nPlease see the requirements listed above.\n\n------------------------------------------------------\n\nOther Relevant Skills\n\nFor complementary skills, please see above and/or contact the recruiter.\n\n------------------------------------------------------\n\nCiti is an equal opportunity employer, and qualified candidates will receive consideration without regard to their race, color, religion, sex, sexual orientation, gender identity, national origin, disability, status as a protected veteran, or any other characteristic protected by law.\n\nIf you are a person with a disability and need a reasonable accommodation to use our search tools and/or apply for a career opportunity review Accessibility at Citi.\n\nView Citi’s EEO Policy Statement and the Know Your Rights poster. \nShow more Show less",
                        "applicationsCount": "Over 200 applicants",
                        "contractType": "Full-time",
                        "experienceLevel": "Not Applicable",
                        "yearsOfExperience": [
                            {
                                "years": "8-12",
                                "context": "Business Analysis experience, preferably in Cards, Payments, or Retail Banking",
                                "lang": "en"
                            }
                        ],
                        "workType": "Research, Analyst, and Information Technology",
                        "sector": "Banking, Financial Services, and Investment Banking",
                        "posterFullName": "",
                        "posterProfileUrl": "",
                        "companyId": "11448",
                        "applyUrl": "https://in.linkedin.com/jobs/view/business-analyst-at-citi-4329027888?trk=public_jobs_topcard-title",
                        "applyType": "EXTERNAL",
                        "matchedKeywords": [],
                        "unmatchedKeywords": [
                            "Salesforce",
                            "Apex",
                            "LWC",
                            "SOQL",
                            "Lightning"
                        ],
                        "keywordMatchScorePercentage": 0
                    }
                ]   #
        '''
            print('responses***********',responses[0])
            
            for eRes in responses:
                posted = eRes.get('postedTime').split() if eRes.get('postedTime') is not None else None
                publishedAt = eRes.get('publishedAt')
                isRecent = self.checkPublishDate(publishedAt)
                if posted is not None and int(posted[0]) <= 24 and isRecent:
                    job_detail = {
                                'App_Ext_Id__c': eRes.get('jobId'),
                                'Company_Name__c': eRes.get('companyName', {}),
                                'Title__c': eRes.get('title'),
                                'ReDirect_url__c': eRes.get('jobUrl'),
                                'Description__c': eRes.get('description'),
                                'location__c' : eRes.get('location'),
                                'ApplyUrl__c' : eRes.get('applyUrl'),
                                'publishedAt__c' : eRes.get('publishedAt')
                            }
                    job_details[eRes.get('jobId')]=  job_detail
            
            print('job_detail******************',len(job_details))
            
            if job_details:
                llmResList =  await self.aSyncApiService.fetchCompanyInfo(job_details)
                
                if llmResList:
                    for eRes in llmResList :
                        #print('eRes************',eRes) 
                        appId = eRes.get('application_id')
                        detail = job_details.get(appId)
                        if detail and detail.get('App_Ext_Id__c') == appId:
                            detail['Employee_Size__c'] = eRes.get('employee_size')
                            detail['Career_Email_Id__c'] = eRes.get('career_email_id')
                            detail['email_draft__c'] = eRes.get('email_draft')
                            detail['Email_Subject__c'] = eRes.get('email_subject')
                
                #sender().send_email(list(job_details.values()))
                self.aSyncApiService.convertIntoExcel(list(job_details.values()))
                self.aSyncApiService.insertIntoSf(list(job_details.values()))

        except Exception as err:
                print(f"An unexpected error occurred: {err}")
    
    
    def checkPublishDate(self, publishedAt):
        try:
           # 1. Setup IST Timezone
            IST = timezone(timedelta(hours=5, minutes=30))

            # 2. Convert the UTC string to IST Date
            published_at_utc = datetime.fromisoformat(publishedAt.replace("Z", "+00:00"))
            published_date_ist = published_at_utc.astimezone(IST).date()
            
            # 3. Get Today's Date in IST
            today_ist = datetime.now(IST).date()
            
            # 4. Compare the Published Date with Today's Date
            difference = (today_ist - published_date_ist).days
            
            if difference <= 4:
                return True   
                  
            return False
        
        except Exception as e:
            print(f"Error parsing published time: {e}")
            return False

async def main():      
    service = apifyjobsearch()
    await service.linkdinJobSearchDetails()


if __name__ == "__main__":
    asyncio.run(main())