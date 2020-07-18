import unittest
from API.APITestCases import APITestCases

class Main():

    def __init__(self):
        print("Test starts")


if __name__ == '__main__':
    unittest.main()
    test = APITestCases()
    test.test_emptyStore()
    test.test_requiredAuthor()
    test.test_requiredTitle()
    test.test_emptyTitle()
    test.test_emptyAuthor()
    test.test_idReadOnly()
    test.test_newBook()
    test.test_DuplicateBook()
