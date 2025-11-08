from buildpp import (
    new_Library,
    SourcesList,
    IncludeDirsList,
    CompileDefinitionsList,
    CompilerFlagsList,
    Version,
    LibType
)

import pytest


class Test_Library:

    def test_name(self):

        libName = "Insert funny name here"
        test = new_Library(libName)

        assert test.name == libName

    class Test_libType:
        def test_basic(self):

            test = new_Library("type")

            assert test.libType is not None  # the lib type needs to be assigned even at default

            test.setLibType(LibType.SHARED)

            assert test.libType == LibType.SHARED

            test.setLibType(LibType.STATIC)

            assert test.libType == LibType.STATIC

        def test_TypeError(self):

            test = new_Library("type")

            errVals = ["STATIC", "SHARED", [], 6]

            for ele in errVals:
                with pytest.raises(AssertionError):
                    test.setLibType(ele)

# ____________________SOURCES____________________
    class Test_sources:
        def test_basic(self):

            test = new_Library("sources")

            sources = SourcesList(["a", "b", "c"])

            test.sources = sources

            assert test.sources.sources == sources.sources

        def test_TypeError(self):

            test = new_Library("sources")

            errVals = [6, [], "foo"]

            for ele in errVals:
                with pytest.raises(AssertionError):
                    test.sources = ele

# ____________________VERSION____________________
    class Test_version:
        def test_basic(self):

            test = new_Library("version")
            testVersion = Version("0.0.6.4")

            test.version = testVersion

            assert test.version == testVersion

        def test_TypeError(self):

            test = new_Library("version")

            errVals = [2930.0, [], "version"]

            for ele in errVals:
                with pytest.raises(AssertionError):
                    test.version = ele

# ____________________COMPILER_FLAGS____________________
    class Test_compilerFlags:
        def test_TypeError(self):

            test = new_Library("flags")

            errVals = [90, "foo", list()]
            
            for ele in errVals:
                with pytest.raises(AssertionError):
                    test.compilerFlags = ele

# ____________________COMPILER_FLAGS____________________
    class Test_compileDefinitions:
        def test_TypeError(self):

            test = new_Library("defs")

            errVals = [90, "foo", list()]
            
            for ele in errVals:
                with pytest.raises(AssertionError):
                    test.compileDefs = ele
