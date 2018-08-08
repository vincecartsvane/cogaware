from django.test import TestCase

from .factories.model_factories import TrapTypeFactory as TrapFactory
from .models import TrapType


class TestTrapType(TestCase):
    def test_creates_one_trap_type(self):
        # arrange/act
        TrapFactory(name='test_trap').save()

        # assert
        self.assertEqual(len(TrapType.objects.all()), 1)

    def test_trap_type_has_correct_name(self):
        # arrange/act
        TrapFactory(name='test_trap').save()

        # assert
        self.assertEqual(TrapType.objects.first().name, 'test_trap')

    def test_two_trap_types_have_correct_names(self):
        # arrange/act
        TrapFactory(name='test_trap').save()
        TrapFactory(name='other_test_trap').save()

        # assert
        names = [o.name for o in TrapType.objects.all()]
        self.assertEqual(len(names), 2)
        self.assertIn('test_trap', names)
        self.assertIn('other_test_trap', names)

    def test_adding_duplicate_name_raises_exception(self):
        # arrange
        TrapFactory(name='test_trap').save()

        # act/assert
        with self.assertRaises(Exception):
            TrapFactory(name='test_trap').save()

    def test_blank_description_field_is_allowed(self):
        # arrange/act
        TrapFactory(name='test_trap').save()

        # assert
        self.assertEqual(TrapType.objects.first().description, None)

    def test_non_blank_description_field(self):
        # arrange/act
        TrapFactory(name='test_trap', description='This is not an actual mind trap').save()

        # assert
        self.assertEqual(
            TrapType.objects.first().description,
            'This is not an actual mind trap')
