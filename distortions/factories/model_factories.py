# The "import as" syntax means that you can type Factory instead
# of DjangoModelFactory - it saves keystrokes :)
from factory.django import DjangoModelFactory as Factory
from factory import SubFactory

from distortions.models import TrapLog, TrapType


class TrapTypeFactory(Factory):
    class Meta:
        model = TrapType


class TrapLogFactory(Factory):
    class Meta:
        model = TrapLog

    trap_type = SubFactory(TrapTypeFactory)
