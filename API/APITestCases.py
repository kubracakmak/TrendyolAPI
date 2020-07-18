import requests
import http.client
import json
import logging
import unittest
import pytest
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

url = 'http://localhost:8080/api/books/'

class APITestCases(unittest.TestCase):


    def test_emptyStore(self):

        r = requests.get(url)

        # json object to string
        jsonData = json.dumps(r.text)

        # string to json object
        bookCount = json.loads(jsonData)

        if not (len(bookCount)):
            print("Store is empty")
        print("Store is not empty")

    def test_requiredAuthor(self):

        try:
            data = {"title": "SRE 101"}
            headers = {'content-type': 'application/json'}

            r = requests.put(url=url, data=json.dumps(data), headers=headers)
            finalJson = json.loads(r.text)["error"]
            r.raise_for_status()

        except requests.exceptions.HTTPError as e:
            print(e)
            self.assertEqual(finalJson, "Field 'author' is required.", "Message is not valid.")

    def test_requiredTitle(self):

        try:
            data = {"author": "John Smith"}
            headers = {'content-type': 'application/json'}

            r = requests.put(url=url, data=json.dumps(data), headers=headers)
            finalJson = json.loads(r.text)["error"]
            r.raise_for_status()

        except requests.exceptions.HTTPError as e:
            print(e)
            self.assertEqual(finalJson, "Field 'title' is required.", "Message is not valid.")

    def test_emptyTitle(self):

        try:
            data = {"author": "John Smith","title": ""}
            headers = {'content-type': 'application/json'}

            r = requests.put(url=url, data=json.dumps(data), headers=headers)
            finalJson = json.loads(r.text)["error"]
            r.raise_for_status()

        except requests.exceptions.HTTPError as e:
            print(e)
            self.assertEqual(finalJson, "Field 'title' cannot be empty.", "Message is not valid.")

    def test_emptyAuthor(self):

        try:
            data = {"author": "","title": "SRE 101"}
            headers = {'content-type': 'application/json'}

            r = requests.put(url=url, data=json.dumps(data), headers=headers)
            finalJson = json.loads(r.text)["error"]
            r.raise_for_status()

        except requests.exceptions.HTTPError as e:
            print(e)
            self.assertEqual(finalJson, "Field 'author' cannot be empty.", "Message is not valid.")

    def test_idReadOnly(self):

        try:
            data = {"id": 1,"author": "John Smith","title": "SRE 101"}
            headers = {'content-type': 'application/json'}

            r = requests.put(url=url, data=json.dumps(data), headers=headers)
            finalJson = json.loads(r.text)["error"]
            r.raise_for_status()

        except requests.exceptions.HTTPError as e:
            print(e)
            self.assertEqual(finalJson, "Field 'id' is readonly.", "Message is not valid.")

    def test_newBook(self):

        try:
            data = {"author": "John Smith", "title": "SRE 101"}
            headers = {'content-type': 'application/json'}

            r = requests.put(url=url, data=json.dumps(data), headers=headers)
            finalJson = json.loads(r.text)["error"]
            r.raise_for_status()
            print(r.text)

            if r.text == requests.get(url=url, params=data):
                print("The same book was found.")
            print("The book wasn't found.")

        except requests.exceptions.HTTPError as e:
            print(e)
            self.assertEqual(finalJson, "Another book with similar title and author already exists.", "Message is not valid.")

    def test_DuplicateBook(self):
        try:

            data = {"author": "John Smith","title": "SRE 101"}
            headers = {'content-type': 'application/json'}

            r = requests.put(url=url, data=json.dumps(data), headers=headers)
            finalJson = json.loads(r.text)["error"]

            if requests.get(url=url, params=data) == r.text:
                r.raise_for_status()

        except requests.exceptions.HTTPError as e:
            print(e)
            self.assertEqual(finalJson, "Another book with similar title and author already exists.", "Message is not valid.")