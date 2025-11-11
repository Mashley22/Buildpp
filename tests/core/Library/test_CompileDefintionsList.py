from buildpp import CompileDefinitionsList

import pytest

BAD_VALS = [4,
            "foo",
            [],
            {4 : "foo"}
            ]

GOOD_VALS = {"foo" : 4,
             "bar" : True,
             "test" : "67",
             "pi" : 3.14,
             "myval" : None}

GOOD_VALS_2 = {"banana" : None,
               "potato" : 4
               }


class Test_CompileDefinitionsList:

    # ____________________CONSTRUCTORS____________________
    def test_constructor_empty(self):

        test = CompileDefinitionsList()

        assert not test.symbols

    def test_constructor_dict(self):

        test = CompileDefinitionsList(GOOD_VALS)
        
        for key in GOOD_VALS.keys():

            assert test.symbols[key] == GOOD_VALS[key]
        
        new_key = "new_key"
        test.add(new_key)

        assert new_key not in GOOD_VALS.keys()  # Test that we recieve an independent copy of the dict from the constructor
 
    def test_constructor_TypeError(self):

        for bad in GOOD_VALS:
            with pytest.raises(AssertionError):
                CompileDefinitionsList(bad)

    # ____________________OTHER____________________
    def test_deDuplicate(self):

        test = CompileDefinitionsList()
        
        test.deDuplicate()  # It's a dict, this shouldn't do anything

    def test_add(self):
        
        test = CompileDefinitionsList()

        for key in GOOD_VALS.keys():

            test.add(key, GOOD_VALS[key])

        for key in GOOD_VALS.keys():

            assert test.symbols[key] == GOOD_VALS[key]

    def test_add_TypeError(self):

        for val in BAD_VALS:
            with pytest.raises(AssertionError):
                CompileDefinitionsList(val)
    
    def test_update(self):

        test = CompileDefinitionsList()

        test.update(GOOD_VALS)

        for key in GOOD_VALS.keys():

            assert test.symbols[key] == GOOD_VALS[key]

    def test_update_TypeError(self):

        test = CompileDefinitionsList()

        with pytest.raises(AssertionError):
            test.update(BAD_VALS)

    def test_contains(self):

        test = CompileDefinitionsList()

        assert "foo" not in test

        test.update(GOOD_VALS)

        for key in GOOD_VALS.keys():

            assert key in test

    def test_merge(self):
        
        test1 = CompileDefinitionsList(GOOD_VALS_2)

        test2 = CompileDefinitionsList(GOOD_VALS)

        test1.merge(test2)
        
        for key in GOOD_VALS.keys():

            assert test1.symbols[key] == GOOD_VALS[key]

        for key in GOOD_VALS_2.keys():

            assert test1.symbols[key] == GOOD_VALS_2[key]

        test2.merge(test1)

        assert test2.symbols == test1.symbols
