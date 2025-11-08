from buildpp import LibInterfacingForm

import pytest

from typing import List


class ListCover:
    _list : list

    def __init__(self,
                 vals : list = []):
        self._list = vals

    def __eq__(self,
               other : 'ListCover') -> bool:

        return sorted(self._list) == sorted(other._list)

    def deDuplicate(self) -> None:

        self._list = list(set(self._list))

    def add(self,
            vals : List[str]) -> None:

        self._list.extend(vals)


class ListCover2:

    def __init__(self,
                 vals : list = []):

        self._list = vals


class Test_LibInterfacingForm:
    def test_basic(self):

        testVar = LibInterfacingForm(ListCover)

        assert testVar.public == ListCover()
        assert testVar.private == ListCover()
        assert testVar.interface == ListCover()

    def test_constructInPlace(self):
        
        public = ListCover([1, 2, 4])
        private = ListCover(["foo", "kool", "kay"])
        interface = ListCover([9, 0])
        testVar = LibInterfacingForm(ListCover,
                                     public,
                                     private,
                                     interface)

        assert testVar.public == public
        assert testVar.private == private
        assert testVar.interface == interface

    def test_setters(self):

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

    def test_inheritPublic(self):

        parent = LibInterfacingForm(ListCover)
        child = LibInterfacingForm(ListCover)

        parent.public = ListCover([1, 5, 8, 6])
        parent.interface = ListCover([6, 7, 9])
        parent.private = ListCover([10, 11, 12])

        child.inheritPublic(parent)

        assert child.public == ListCover([1, 5, 8, 6, 7, 9])
        assert child.private == ListCover()
        assert child.interface == ListCover()

    def test_inheritPrivate(self):

        parent = LibInterfacingForm(ListCover)
        child = LibInterfacingForm(ListCover)

        parent.public = ListCover([1, 5, 8, 6])
        parent.interface = ListCover([6, 7, 9])
        parent.private = ListCover([10, 11, 12])

        child.inheritPrivate(parent)

        assert child.private == ListCover([1, 5, 8, 6, 7, 9])
        assert child.public == ListCover()
        assert child.interface == ListCover()

    def test_inheritInterface(self):

        parent = LibInterfacingForm(ListCover)
        child = LibInterfacingForm(ListCover)

        parent.public = ListCover([1, 5, 8, 6])
        parent.interface = ListCover([6, 7, 9])
        parent.private = ListCover([10, 11, 12])

        child.inheritInterface(parent)

        assert child.interface == ListCover([1, 5, 8, 6, 7, 9])
        assert child.private == ListCover()
        assert child.public == ListCover()

    def test_all(self):

        test = LibInterfacingForm(ListCover)

        test.public = ListCover([1, 2, 3, 4])
        test.private = ListCover([6, 7])
        test.interface = ListCover([6, 9])

        assert sorted(test.all()) == sorted([1, 2, 3, 4, 6, 7, 6, 9])

    def test_inheritTypeAssert(self):

        one = LibInterfacingForm(ListCover)
        two = LibInterfacingForm(ListCover2)

        with pytest.raises(AssertionError):
            one.inheritPublic(two)

        with pytest.raises(AssertionError):
            one.inheritPrivate(two)

        with pytest.raises(AssertionError):
            one.inheritInterface(two)

        with pytest.raises(AssertionError):
            one.inheritPublic(two)

        with pytest.raises(AssertionError):
            one.inheritPrivate(two)

        with pytest.raises(AssertionError):
            one.inheritInterface(two)

    def test_assignTypeAssert(self):

        one = LibInterfacingForm(ListCover)

        with pytest.raises(AssertionError):
            one.public = ListCover2()

        with pytest.raises(AssertionError):
            one.private = ListCover2()

        with pytest.raises(AssertionError):
            one.private = ListCover2()
