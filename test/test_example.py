from unittest import TestCase


class ExampleTest(TestCase):

    def test_example(self):
        number = int("1")
        self.assertEqual(1, number)