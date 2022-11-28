from django.test import RequestFactory, TestCase
from .views import HomeView
from django.urls import reverse

class HomeViewTest(TestCase):
    def setUp(self):
        self.view = HomeView()
        self.request_factory = RequestFactory()

    def test_get_context_data(self):
        request = self.request_factory.get('/')
        view = HomeView()
        view.setup(request)
        context = view.get_context_data()
        self.assertEqual(context["error"], None)

    def test_get_reading_data(self):
        res = self.view.get_reading_data("summer")
        self.assertEqual(res["status"], "success")

    def test_get_on_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_post_on_home_page(self):
        response = self.client.post("/", {"title":"winter"})
        self.assertEqual(response.status_code, 200)
