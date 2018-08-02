from django.test import TestCase

from .factories.model_factories import TrapTypeFactory as TrapFactory
from .models import TrapType


class TestTrapType(TestCase):
    def test_creates_one_distortion_type(self):
        # arrange/act
        TrapFactory(name='test_distortion').save()

        # assert
        self.assertEqual(len(TrapType.objects.all()), 1)

    def test_distortion_type_has_correct_name(self):
        # arrange/act
        TrapFactory(name='test_distortion').save()

        # assert
        self.assertEqual(TrapType.objects.first().name, 'test_distortion')

    def test_two_distortion_types_have_correct_names(self):
        # arrange/act
        TrapFactory(name='test_distortion').save()
        TrapFactory(name='other_test_distortion').save()

        # assert
        names = [o.name for o in TrapType.objects.all()]
        self.assertEqual(len(names), 2)
        self.assertIn('test_distortion', names)
        self.assertIn('other_test_distortion', names)

    def test_adding_duplicate_name_raises_exception(self):
        # arrange
        TrapFactory(name='test_distortion').save()

        # act/assert
        with self.assertRaises(Exception):
            TrapFactory(name='test_distortion').save()

    def test_blank_description_field_is_allowed(self):
        # arrange/act
        TrapFactory(name='test_distortion').save()

        # assert
        self.assertEqual(TrapType.objects.first().description, None)

    def test_non_blank_description_field(self):
        # arrange/act
        TrapFactory(name='test_distortion', description='This is not an actual cognitive distortion').save()

        # assert
        self.assertEqual(
            TrapType.objects.first().description,
            'This is not an actual cognitive distortion')
