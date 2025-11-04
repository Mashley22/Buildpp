from buildpp.versions import Version, VersionComponentNumMismatchErr
import pytest


def test_Version_default():

    test = Version()  # noqa


def test_Version_single():

    for i in range(0, 50):
        test = Version(f"{i}")
        assert test._version[0] == i


def test_Version_double():

    for i in range(0, 50):
        for j in range(0, 100):
            test = Version(f"{i}.{j}")
            assert test._version[0] == i
            assert test._version[1] == j


def test_Version_eq():

    assert Version("5") == Version("5")
    assert Version("99.89") == Version("99.89")
    assert Version("9.1.0") == Version("9.1.0")

    with pytest.raises(VersionComponentNumMismatchErr):
        Version("4") == Version("6.1")


def test_Version_lt():

    assert Version("4") < Version("5")
    assert Version("4.1") < Version("5.0")
    assert Version("0.98.1") < Version("1.5.0")

    with pytest.raises(VersionComponentNumMismatchErr):
        Version("4") < Version("6.1")


def test_Version_le():

    assert Version("6") <= Version("7")
    assert Version("4.1") <= Version("7.0")
    assert Version("0.99.5") <= Version("0.99.6")

    assert Version("5") <= Version("5")
    assert Version("99.89") <= Version("99.89")
    assert Version("9.1.0") <= Version("9.1.0")

    with pytest.raises(VersionComponentNumMismatchErr):
        Version("6") <= Version("6.1")


def test_Version_gt():

    assert Version("7") > Version("5")
    assert Version("9.1") > Version("5.0")
    assert Version("4.98.1") > Version("1.5.0")

    with pytest.raises(VersionComponentNumMismatchErr):
        Version("9.98") > Version("4")


def test_Version_ge():

    assert Version("7") >= Version("5")
    assert Version("9.1") >= Version("5.0")
    assert Version("4.98.1") >= Version("1.5.0")

    assert Version("6") >= Version("6")
    assert Version("6.7") >= Version("6.7")
    assert Version("4.2.0") >= Version("4.2.0")

    with pytest.raises(VersionComponentNumMismatchErr):
        Version("9.98") >= Version("4")
