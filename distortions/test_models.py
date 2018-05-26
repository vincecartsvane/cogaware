from django.test import TestCase

from .factories.model_factories import DistortionTypeFactory as DTFactory
from .models import DistortionType


class TestDistortionType(TestCase):
    def test_creates_one_distortion_type(self):
        # arrange
        DTFactory(name='test_distortion').save()

        # act/assert
        self.assertEqual(len(DistortionType.objects.all()), 1)

    def test_distortion_type_has_correct_name(self):
        # arrange
        DTFactory(name='test_distortion').save()

        # act/assert
        self.assertEqual(DistortionType.objects.get(id=1).name, 'test_distortion')
    def test_two_distortion_types_have_correct_names(self):
        # arrange
        DTFactory(name='test_distortion').save()
        DTFactory(name='other_test_distortion').save()

        # act/assert
        self.assertEqual(DistortionType.objects.get(id=1).name, 'test_distortion')
        self.assertEqual(DistortionType.objects.get(id=2).name, 'other_test_distortion')

    def test_adding_duplicate_name_raises_exception(self):
        # arrange
        DTFactory(name='test_distortion').save()

        # act/assert
        with self.assertRaises(Exception):
            DTFactory(name='test_distortion').save()
