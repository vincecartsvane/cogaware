from django.test import TestCase

from .factories.model_factories import DistortionTypeFactory as DTFactory
from .models import DistortionType


class TestDistortionType(TestCase):
    def test_creates_one_distortion_type(self):
        # arrange
        DTFactory(name='test_distortion').save()

        # act/assert
        self.assertEqual(len(DistortionType.objects.all()), 1)
