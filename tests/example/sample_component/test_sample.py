"""
This file contains the format of a test case.
It contains one class - TestCase wich would
hold the functions to be run in the test case.
"""

#disruptive;dist,rep,arb,disp,dist-rep,dist-arb,dist-disp

from tests.parent_test import ParentTest


class TestClass(ParentTest):
    """
    The TestCase class contains the functions to be
    run in the test case. Every function should contain
    the flow of the function(APIs which are called) in
    the form of steps.
    """

    def run_test(self):
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
