# To run these, run `python manage.py test distortions.test_views`

from django.test import TestCase
from django.urls import reverse


class TestIndex(TestCase):
    def test_returns_correct_string(self):
        # act
        response = self.client.get(reverse('index'))

        # assert
        self.assertContains(response, "Add your mind traps here")

    def test_contains_add_trap_button(self):
        # act
        response = self.client.get(reverse('index'))

        # assert
        self.assertContains(response, '<button type="submit" class="btn btn-primary">Add mind trap</button>', html=True)
