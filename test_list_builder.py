"""

This component is responsible for creating a list
of tests-to-run to be used by the redant_test_runner component.
Input for this component : the tests-to-run list which was parsed
from the cli and the return: list of all the tests which are going
to be executed in the current session.

"""
import os
import inspect
import importlib
from comment_parser.comment_parser import extract_comments


class TestListBuilder:
    """
    The test list builder is concerned with parsing
    avialable TCs and their options so as to pass on the
    TC related data to the test_runner.
    """
    tests_to_run: list = []
    tests_run_dict: dict = {"disruptive" : [],
                            "nonDisruptive" : []}
    tests_component_dir: dict = {"functional" : set([]),
                                 "performance" : set([]),
                                 "example" : set([])}

    @classmethod
    def create_test_dict(cls, path: str) -> tuple:
        """
        This method creates a dict of TCs wrt the given directory
        path.
        Args:
            path (str): The directory path which contains the TCs
            to be run.
        Returns:
            A Tuple of the following format
            ({
                "disruptive" : [
                                   {
                                      "volType" : [replicated,..],
                                      "modulePath" : "../glusterd/test_sample.py",
                                      "moduleName" : "test_sample.py",
                                      "componentName" : "glusterd",
                                      "testClass" : <class>,
                                      "testType" : "functional/performance/example"
                                    },
                                    {
                                       ...
                                    }
                                ],
                "nonDisruptive" : [
                                    {
                                         "volType" : [replicated,..],
                                         "modulePath" : "../DHT/test_sample.py",
                                         "moduleName" : "test_sample.py",
                                         "componentName" : "DHT",
                                         "testClass" : <class>,
                                         "testType" : "functional/performance/example"
                                    },
                                    {
                                         ...
                                    }
                                  ]
            },
            {
                "functional" : ["component1", "component2",...],
                "performance" : ["component1", "component2", ...],
                "example" : ["component1"...]
            }
        """
        # Obtaining list of paths to the TCs under given directory.
        try:
            for root, _, files in os.walk(path):
                for tfile in files:
                    if tfile.endswith(".py") and tfile.startswith("test"):
                        cls.tests_to_run.append(os.path.join(root, tfile))

        except Exception as e:
            print(e)
            return {}

        # Extracting the test case flags and adding module level info.
        for test_case_path in cls.tests_to_run:
            test_flags = cls._get_test_module_info(test_case_path)
            test_dict = {}
            test_dict["volType"] = test_flags["volType"]
            test_dict["modulePath"] = test_case_path
            test_dict["moduleName"] = test_case_path.split("/")[-1]
            test_dict["componentName"] = test_case_path.split("/")[-2]
            test_dict["testClass"] = cls._get_test_class(test_case_path)
            test_dict["testType"] = test_case_path.split("/")[-3]
            cls.tests_component_dir[test_dict["testType"]].add(\
                test_case_path.split("/")[-2])
            cls.tests_run_dict[test_flags["tcNature"]].append(test_dict)

        # Cleaning up the component list
        for test_type in cls.tests_component_dir:
            cls.tests_component_dir[test_type] =\
                list(cls.tests_component_dir[test_type])
        return (cls.tests_run_dict, cls.tests_component_dir)

    @classmethod
    def _get_test_module_info(cls, tc_path: str) -> dict:
        """
        This method gets the volume types for which the TC is to be run
        and the nature of a TC
        Args:
           tc_path (str): The path of the test case.

        Returns:
           test_flags (dict): This dictionary contains the volume types
                              for which the TC is to be run and the nature
                              of the TC, i.e. Disruptive / Non-Disruptive.
           For example,
                      {
                        "tcNature" : "disruptive",
                        "volType" : [replicated, ...]
                      }
        """
        flags = str(extract_comments(tc_path, mime="text/x-python")[0])
        tc_flags = {}
        tc_flags["tcNature"] = flags.split(';')[0]
        tc_flags["volType"] = flags.split(';')[1].split(',')

        return tc_flags

    @classmethod
    def _get_test_class(cls, tc_path: str):
        """
        Method to import the module and inspect the class to be stored
        for creating objects later.
        """
        tc_module_str = tc_path.replace("/", ".")[:-3]
        tc_module = importlib.import_module(tc_module_str)
        tc_class_str = inspect.getmembers(tc_module,
                                          inspect.isclass)[1][0]
        tc_class = getattr(tc_module, tc_class_str)
        return tc_class
