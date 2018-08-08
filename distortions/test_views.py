# To run these, run `python manage.py test distortions.test_views`

from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.test import TestCase, TransactionTestCase
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


class TestAdd(TransactionTestCase):
    def test_newly_added_trap_appears_on_index(self):
        # act
        self.client.post(reverse('index'), {'trap_name': 'Catastrophising'})

        # assert
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'Catastrophising', html=True)

    def test_does_not_add_duplicate_mind_trap(self):
        # act
        self.client.post(reverse('index'), {'trap_name': 'Catastrophising'})
        self.client.post(reverse('index'), {'trap_name': 'Catastrophising'})

        # assert
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'Catastrophising', html=True, count=1)

    def test_redirects_to_index(self):
        # act
        response = self.client.post(reverse('index'), {'trap_name': 'Catastrophising'})

        # assert
        self.assertTrue(isinstance(response, HttpResponseRedirect))


class TestTrap(TestCase):
    def test_response_contains_trap_name(self):
        # arrange
        trap = TrapFactory(name='Generalising')
        trap.save()

        # act
        response = self.client.get(reverse('trap', args=[trap.id]))

        # assert
        self.assertContains(response, 'Generalising', html=True, count=1)

    def test_nonexistent_id_returns_not_found(self):
        # arrange
        trap = TrapFactory(name='Generalising')
        trap.save()

        # act
        response = self.client.get(reverse('trap', args=[trap.id + 3]))

        # assert
        self.assertTrue(isinstance(response, HttpResponseNotFound))

    def test_delete_redirects_back_to_index(self):
        # arrange
        trap1 = TrapFactory(name='Catastrophising')
        trap1.save()
        trap2 = TrapFactory(name='Generalising')
        trap2.save()

        # act
        response = self.client.delete(reverse('trap', args=[trap1.id]))

        # assert
        self.assertRedirects(response, reverse('index'))

    def test_delete_removes_trap(self):
        # arrange
        trap = TrapFactory(name='Generalising')
        trap.save()

        # act
        self.client.delete(reverse('trap', args=[trap.id]))

        # assert
        response = self.client.get(reverse('trap', args=[trap.id]))
        self.assertTrue(isinstance(response, HttpResponseNotFound))

    def test_delete_does_not_remove_other_traps(self):
        # arrange
        trap1 = TrapFactory(name='Catastrophising')
        trap1.save()
        trap2 = TrapFactory(name='Generalising')
        trap2.save()

        # act
        self.client.delete(reverse('trap', args=[trap1.id]))

        # assert
        response = self.client.get(reverse('trap', args=[trap2.id]))
        self.assertContains(response, 'Generalising')

    def test_delete_does_not_remove_other_from_index(self):
        # arrange
        trap1 = TrapFactory(name='Catastrophising')
        trap1.save()
        trap2 = TrapFactory(name='Generalising')
        trap2.save()

        # act
        self.client.delete(reverse('trap', args=[trap1.id]))

        # assert
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'Generalising')

    def test_deleting_nonexistent_trap_returns_404(self):
        # arrange
        trap = TrapFactory(name='Catastrophising')
        trap.save()

        # act
        response = self.client.delete(reverse('trap', args=[trap.id + 3]))

        # assert
        self.assertTrue(isinstance(response, HttpResponseNotFound))
