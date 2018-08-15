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
        self.assertContains(response, 'Catastrophising')

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
        self.assertContains(response, 'Catastrophising')
        self.assertContains(response, 'Generalising')


class TestIndexTrapList(TestCase):
    def setUp(self):
        trap = TrapFactory(name='Catastrophising')
        trap.save()
        self.trap_id = trap.id

    def test_contains_button_link_to_trap(self):
        # act
        response = self.client.get(reverse('index'))

        # assert
        self.assertContains(
            response,
            '<button type="submit" class="btn btn-primary">Show</button>',
            html=True)

    def test_contains_button_to_delete_trap(self):
        # act
        response = self.client.get(reverse('index'))

        # assert
        self.assertContains(
            response,
            '<button type="submit" class="btn btn-primary" onclick="delete_trap(%d)">Delete</button>' % (self.trap_id,),
            html=True)


class TestAdd(TransactionTestCase):
    def test_newly_added_trap_appears_on_index(self):
        # act
        self.client.post(reverse('index'), {'trap_name': 'Catastrophising'})

        # assert
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'Catastrophising')

    def test_does_not_add_duplicate_mind_trap(self):
        # act
        self.client.post(reverse('index'), {'trap_name': 'Catastrophising'})
        self.client.post(reverse('index'), {'trap_name': 'Catastrophising'})

        # assert
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'Catastrophising', count=1)

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

    def test_shows_trap_description_if_present(self):
        # arrange
        trap = TrapFactory(
            name='Catastrophising',
            description='Viewing the situation as far worse than it is')
        trap.save()

        # act
        response = self.client.get(reverse('trap', args=[trap.id]))

        # assert
        self.assertContains(response,
                            'Viewing the situation as far worse than it is')

    def test_does_not_show_description_if_none(self):
        # arrange
        trap = TrapFactory(name='Catastrophising')
        trap.save()

        # act
        response = self.client.get(reverse('trap', args=[trap.id]))

        # assert
        self.assertNotContains(response, 'None')

    def test_shows_add_description_button_if_no_description(self):
        # arrange
        trap = TrapFactory(name='Catastrophising')
        trap.save()

        # act
        response = self.client.get(reverse('trap', args=[trap.id]))

        # assert
        self.assertContains(response, '<button type="submit" class="btn btn-primary">Add description</button>', html=True)

    def test_shows_edit_description_button_if_description_present(self):
        # arrange
        trap = TrapFactory(
            name='Catastrophising',
            description='Viewing the situation as far worse than it is')
        trap.save()

        # act
        response = self.client.get(reverse('trap', args=[trap.id]))

        # assert
        self.assertContains(response, '<button type="submit" class="btn btn-primary">Edit description</button>', html=True)

    def test_description_is_shown_as_editable_textarea(self):
        # arrange
        trap = TrapFactory(
            name='Catastrophising',
            description='Catastrophe!')
        trap.save()

        # act
        response = self.client.get(reverse('trap', args=[trap.id]))

        # assert
        self.assertContains(
            response,
            '<textarea name="description" form="desc_form">Catastrophe!</textarea>',
            html=True)

    def test_does_not_show_add_description_button_if_description_present(self):
        # arrange
        trap = TrapFactory(
            name='Catastrophising',
            description='Viewing the situation as far worse than it is')
        trap.save()

        # act
        response = self.client.get(reverse('trap', args=[trap.id]))

        # assert
        self.assertNotContains(response, '<button type="submit" class="btn btn-primary">Add description</button>', html=True)

    def test_post_adds_description(self):
        trap = TrapFactory(name='Personalisation')
        trap.save()

        # act
        self.client.post(reverse('trap', args=[trap.id]),
                         {'description': 'Taking everything personally'})

        # assert
        response = self.client.get(reverse('trap', args=[trap.id]))
        self.assertContains(response, 'Taking everything personally')

    def test_post_redirects_back_to_trap_page(self):
        trap = TrapFactory(name='Personalisation')
        trap.save()

        # act
        response = self.client.post(
            reverse('trap', args=[trap.id]),
            {'description': 'Taking everything personally'})

        # assert
        self.assertRedirects(response, reverse('trap', args=[trap.id]))

    def test_post_overwrites_description(self):
        trap = TrapFactory(name='Personalisation', description='blah')
        trap.save()

        # act
        self.client.post(reverse('trap', args=[trap.id]),
                         {'description': 'Taking everything personally'})

        # assert
        response = self.client.get(reverse('trap', args=[trap.id]))
        self.assertContains(response, 'Taking everything personally')
        self.assertNotContains(response, 'blah')

    def test_blank_description_clears_description(self):
        trap = TrapFactory(name='Personalisation', description='blah')
        trap.save()

        # act
        self.client.post(reverse('trap', args=[trap.id]),
                         {'description': ''})

        # assert
        response = self.client.get(reverse('trap', args=[trap.id]))
        self.assertNotContains(response, 'blah')
        self.assertContains(response, '<button type="submit" class="btn btn-primary">Add description</button>', html=True)

    def test_has_link_back_to_index_page(self):
        trap = TrapFactory(name='Personalisation', description='blah')
        trap.save()

        # act
        self.client.get(reverse('trap', args=[trap.id]))

        # assert
        response = self.client.get(reverse('trap', args=[trap.id]))
        self.assertContains(
            response,
            '<form action="/traps/"><button type="submit" class="btn btn-primary" >Back</button></form>',
            html=True)
