from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
import requests
from requests.structures import CaseInsensitiveDict
from requests.exceptions import HTTPError
import logging
from .configs import NYPL_API_TOKEN


logger = logging.getLogger(__name__)


class nyplApiView(APIView):

	def __init__(self):
		super(nyplApiView, self).__init__()
		self.nypl_api_token = NYPL_API_TOKEN # keep in private
		self.custom_headers = CaseInsensitiveDict()
		self.custom_headers["Authorization"] = "Token token=\"%s\""%self.nypl_api_token
		self.similar_reading_limit = 10
		self.response = {"status": "error", "data": {}}
		self.data = {
			"reading_title":"",
			"reading_type":"",
			"reading_weblink":"",
			"collection_similar_captures":[]
		}
		self.NOT_FOUND = "not found"

	def get(self, request, title): # main GET call for this API
		return_response_data = self.return_response_data(title)
		return Response(return_response_data)

	def return_response_data(self, title):
		reading = self.search_in_nypl(title)
		try:
			if not reading: # Error happens when search for the title reading
				return self.response

			self.response["status"] = "success" # success in finding records
			if reading != self.NOT_FOUND: # check if this is a reading in the library
				self.data = {
					"reading_title":reading["title"],
					"reading_type":reading["typeOfResource"],
					"reading_weblink":reading["itemLink"],
					"collection_similar_captures":self.get_collections_items(reading["uuid"])
				}
				self.response = {"status": "success", "data":  self.data}
		except Exception as e:
			logger.error("Error when call api on get , error is %s"%str(e))
		return self.response

	def connect_to_nypl_apis(self, url): # connect to the NYPL APIs
		response = requests.get(url, headers=self.custom_headers)
		try:
			if response.status_code != requests.codes.ok:
				logger.error("Failed to call NYPL search API, status code %s"%str(response.status_code))
				return None

			res = response.json()
			if res:
				return res['nyplAPI']['response']
		except HTTPError as e:
			logger.error("Failed to call NYPL search API, HTTPError is %s"%str(e))
		except Exception as e:
			logger.error("Failed to call NYPL search API, error is %s"%str(e))
		return None

	def search_in_nypl(self, title): # call search NYPL API
		search_url = "http://api.repo.nypl.org/api/v2/items/search?field=title&q="+title
		response = self.connect_to_nypl_apis(search_url)

		if not response or "numResults" not in response or int(response["numResults"])<=0:
			logger.debug("No response readings from nypl search api %s"%str(search_url))
			return self.NOT_FOUND

		try:
			reading = response["result"][0] # return the first readding objectß
			logger.info("Returned searched readding %s" %str(reading))
			return reading
		except Exception as e:
			logger.error("Failed to call NYPL search API, error is %s"%str(e))
		return None

	def get_collections_items(self, reading_uuid): # call collection item NYPL API to return same collection captures
		reading_collection_captures = []
		url = "http://api.repo.nypl.org/api/v2/items/collection/"+reading_uuid
		response = self.connect_to_nypl_apis(url)

		if not response or "numResults" not in response or int(response["numResults"])<=0:
			logger.debug("No other readings in same collection from nypl collection api %s"%str(url))
			return None

		try:
			logger.info("Returned searched same collection readings %s" %str(response["capture"]))
			count = 0
			for capture in response["capture"]:
				if count < self.similar_reading_limit and capture["uuid"] != reading_uuid:
					count +=1
					reading_collection_captures.append({
						"title":capture["title"], 
						"type":capture["typeOfResource"], 
						"weblink":capture["itemLink"]})
		except Exception as e:
			logger.error("Failed to call NYPL collection API, error is %s"%str(e))
		return reading_collection_captures
