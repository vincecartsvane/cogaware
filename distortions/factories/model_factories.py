# The "import as" syntax means that you can type Factory instead
# of DjangoModelFactory - it saves keystrokes :)
from factory.django import DjangoModelFactory as Factory
from factory import SubFactory

from distortions.models import IdentifiedTrap, TrapType


class TrapTypeFactory(Factory):
    class Meta:
        model = TrapType


class IdentifiedTrapFactory(Factory):
    class Meta:
        model = IdentifiedTrap

    distortion_type = SubFactory(TrapTypeFactory)
