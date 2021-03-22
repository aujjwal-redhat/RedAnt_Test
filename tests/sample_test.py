"""
This file contains the format of a test case.
It contains one class - TestCase wich would
hold the functions to be run in the test case.
"""

from parent_test import ParentTest


class TestClass(ParentTest):

    """
    The TestCase class contains the functionsto be
    run in the test case. Every function should contain
    the flow of the function(APIs which are called) in
    the form of steps.
    """

    def __init__(self, redant: object):
        """
        Initializer which provides a point of contact to the
        redant framework.
        Args:
            redant (object): mixin object passed as reference.
                             Point of contact for the redant
                             framework.
        """
        super().__init__(redant=redant)

    @classmethod
    def test_fn(cls):
        """
        Function calling required APIs for performing required test.
        Steps:
        1) calling API1
        2) calling API2
        """
        try:
            print("Hello world!")
        except Exception as error:
            print(f"Exception: {error}")
