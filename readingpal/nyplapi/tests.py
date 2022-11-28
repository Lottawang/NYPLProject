import unittest
from django.urls import reverse
from rest_framework.test import APIClient
from .views import nyplApiView


class nyplApiClassTest(unittest.TestCase):

    def setUp(self):
        self.client = APIClient()
        self.nyplApiViewObject = nyplApiView()
        self.NOT_FOUND = "not found"

    def test_api_endpoint(self):
        # test case for calling the API 
        url = reverse('search-with-similar', kwargs={"title":"summer"})
        response = self.client.get(url)
        res = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['status'], "success")

    def test_return_response_data(self):
        res = self.nyplApiViewObject.return_response_data("winter")
        self.assertEqual(res["status"], "success")

    def test_connect_to_nypl_apis(self):
        url = "http://api.repo.nypl.org/api/v2/items/search?field=title&q=summer"
        res = self.nyplApiViewObject.connect_to_nypl_apis(url)
        self.assertEqual(res["headers"]["status"], "success")

    def test_search_in_nypl(self):
        # test case for normal saved readings in library
        res = self.nyplApiViewObject.search_in_nypl("summer")
        self.assertEqual(res["uuid"], "8afc6586-988d-a28e-e040-e00a18067b76")

        # test case for a reading but not in the library
        res = self.nyplApiViewObject.search_in_nypl("dsfhdjsgfh dhf dhgfdh")
        self.assertEqual(res, self.NOT_FOUND)

    def test_get_collections_items(self):
        # test case for empty similar captures in the same collection
        res = self.nyplApiViewObject.get_collections_items("80d47102-a77f-5fc6-e040-e00a18065e1d")
        self.assertEqual(res, [])

        # test case for available captures in the same colleciton
        res = self.nyplApiViewObject.get_collections_items("8afc6586-988d-a28e-e040-e00a18067b76")
        self.assertEqual(res[0]["title"], "Logan House, Altoona.")


