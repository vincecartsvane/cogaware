# To run these, run `python manage.py test distortions.test_views`

from django.test import TestCase
from django.urls import reverse

from .factories.model_factories import TrapTypeFactory as TrapFactory

class TestIndex(TestCase):
    def test_contains_string_for_adding_new_mind_traps(self):
        # act
        response = self.client.get(reverse('index'))

        # assert
        self.assertContains(response, "Add a new mind trap here:")

    def test_contains_string_for_identifying_existing_mind_traps(self):
        # act
        response = self.client.get(reverse('index'))

        # assert
        self.assertContains(response, "Log your mind traps:")

    def test_contains_add_trap_button(self):
        # act
        response = self.client.get(reverse('index'))

        # assert
        self.assertContains(response, '<button type="submit" class="btn btn-primary">Add mind trap</button>', html=True)

    def test_contains_trap_from_database(self):
        # arrange
        TrapFactory(name='Catastrophising').save()

        # act
        response = self.client.get(reverse('index'))

        # assert
        self.assertContains(response, 'Catastrophising', html=True)

    def test_does_not_contain_trap_when_not_in_database(self):
        # act
        response = self.client.get(reverse('index'))

        # assert
        self.assertNotContains(response, 'Catastrophising', html=True)

    def test_contains_multiple_traps_from_database(self):
        # arrange
        TrapFactory(name='Catastrophising').save()
        TrapFactory(name='Generalising').save()

        # act
        response = self.client.get(reverse('index'))

        # assert
        self.assertContains(response, 'Catastrophising', html=True)
        self.assertContains(response, 'Generalising', html=True)


class TestAdd(TestCase):
    def test_newly_added_trap_appears_on_index(self):
        # act
        self.client.post(reverse('index'), {'trap_name': 'Catastrophising'})

        # assert
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'Catastrophising', html=True)
