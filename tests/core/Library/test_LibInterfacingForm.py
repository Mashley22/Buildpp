from buildpp.library import LibInterfacingForm
from buildpp.utils import deDuplicateList


class ListCover:
    _list : list

    def __init__(self,
                 vals : list = []):
        self._list = vals

    def __eq__(self,
               other : 'ListCover') -> bool:

        return sorted(self._list) == sorted(other._list)

    def deDuplicate(self) -> None:

        self._list = deDuplicateList(self._list)


def test_LibInterfacingFrom_basic():

    testVar = LibInterfacingForm(ListCover)

    assert testVar.public == ListCover()
    assert testVar.private == ListCover()
    assert testVar.interface == ListCover()


def test_LibInterfacingForm_setters():

    testVar = LibInterfacingForm(ListCover)

    pub = ListCover([1, 2, 3, 4])
    priv = ListCover([9, 8, 0, 5, 3, 6])
    itf = ListCover(["a", "b", "c", "d"])

    testVar.public = pub
    testVar.private = priv
    testVar.interface = itf

    assert testVar.public == pub
    assert testVar.private == priv
    assert testVar.interface == itf


def test_LibInterfacingForm_inheritPublic():

    parent = LibInterfacingForm(ListCover)
    child = LibInterfacingForm(ListCover)

    parent.public = ListCover([1, 5, 8])
    parent.interface = ListCover([6, 7, 9])
    parent.private = ListCover([10, 11, 12])

    child.inheritPublic(parent)

    assert child.public == ListCover([1, 5, 8, 6, 7, 9])
    assert child.private == ListCover()
    assert child.interface == ListCover()


def test_LibInterfacingForm_inheritPrivate():

    parent = LibInterfacingForm(ListCover)
    child = LibInterfacingForm(ListCover)

    parent.public = ListCover([1, 5, 8])
    parent.interface = ListCover([6, 7, 9])
    parent.private = ListCover([10, 11, 12])

    child.inheritPublic(parent)

    assert child.private == ListCover([1, 5, 8, 6, 7, 9])
    assert child.public == ListCover()
    assert child.interface == ListCover()


def test_LibInterfacingForm_inheritInterface():

    parent = LibInterfacingForm(ListCover)
    child = LibInterfacingForm(ListCover)

    parent.public = ListCover([1, 5, 8])
    parent.interface = ListCover([6, 7, 9])
    parent.private = ListCover([10, 11, 12])

    child.inheritPublic(parent)

    assert child.interface == ListCover([1, 5, 8, 6, 7, 9])
    assert child.private == ListCover()
    assert child.public == ListCover()
