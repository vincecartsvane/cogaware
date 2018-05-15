# To run these, run `python manage.py test distortions.test_views`

from django.test import TestCase
from django.urls import reverse


class TestIndex(TestCase):
    def test_returns_correct_string(self):
        # act
        response = self.client.get(reverse('index'))

        # assert
        self.assertContains(response, "Add your cognitive distortions here")
