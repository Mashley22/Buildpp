from buildpp import new_Library

MAX_DEPTH = 10


class Test_SubDependencies:
    def test_basic(self):

        main = new_Library("main")
        dep = new_Library("dep")
        subDep = new_Library("subDep")

        dep.dependencies.private.add(subDep)
        assert dep.dependencies.private.libs == [subDep]

        main.dependencies.private.add(dep)
        assert main.dependencies.private.libs == [dep]

        main.handleDependencies()
        assert main.dependencies.linkOnly.libs == [subDep]

    def test_referenceBehaviour(self):  # Test that you get a reference to the depdency

        main = new_Library("main")
        dep = new_Library("dep")
        subDep = new_Library("subDep")

        main.dependencies.private.add(dep)
        assert main.dependencies.private.libs == [dep]

        dep.dependencies.private.add(subDep)
        assert dep.dependencies.private.libs == [subDep]  # Swapped the order of adding subDp and dep

        main.handleDependencies()
        assert main.dependencies.linkOnly.libs == [subDep]

    def __multiLevels(self,
                      depth : int = 4):
        
        libs = [new_Library(str(i)) for i in range(depth)]

        for i in range(1, depth):
            libs[i].dependencies.private.add(libs[i - 1])
            assert libs[i].dependencies.private.libs == [libs[i - 1]]

        libs[-1].handleDependencies()
        
        for i in range(1, depth):
            currentLinkOnly = libs[i].dependencies.linkOnly.libs
            assert set(currentLinkOnly) == set(libs[:(i - 1)])
            assert len(set(currentLinkOnly)) == len(currentLinkOnly)  # should be duplicate free

    def test_manyLevels(self):

        for i in range(3, MAX_DEPTH):
            self.__multiLevels(i)
