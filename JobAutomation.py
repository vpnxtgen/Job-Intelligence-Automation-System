from AdzunaJobService import AdzunaJobService as AdznaService
from ApifyJobSearch import apifyjobsearch as ApifyService

class jobAutomation:
    def __init__(self, job_name):
        self.job_name = job_name
        self.adzuna_service = AdznaService()
        self.apify_service = ApifyService()
