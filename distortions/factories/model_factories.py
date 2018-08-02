# The "import as" syntax means that you can type Factory instead
# of DjangoModelFactory - it saves keystrokes :)
from factory.django import DjangoModelFactory as Factory
from factory import SubFactory

from distortions.models import CaughtDistortion, TrapType


class TrapTypeFactory(Factory):
    class Meta:
        model = TrapType


class CaughtDistortionFactory(Factory):
    class Meta:
        model = CaughtDistortion

    distortion_type = SubFactory(TrapTypeFactory)
