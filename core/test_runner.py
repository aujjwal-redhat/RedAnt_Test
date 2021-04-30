"""
The test runner is responsible for handling the list of TCs
to be run and invoking them.
"""
import uuid
import time
from datetime import datetime
from threading import Thread, Semaphore
from colorama import Fore, Style
from runner_thread import RunnerThread


class TestRunner:
    """
    Test runner class will encapsulate the functionalities corresponding
    to the invocation of the runner threads with respect to the list
    created by the test list builder.
    """

    @classmethod
    def init(cls, test_run_dict: dict, param_obj: dict,
             base_log_path: str, log_level: str, semaphore_count: int):
        cls.param_obj = param_obj
        cls.semaphore = Semaphore(semaphore_count)
        cls.base_log_path = base_log_path
        cls.log_level = log_level
        cls.concur_test = test_run_dict["nonDisruptive"]
        cls.non_concur_test = test_run_dict["disruptive"]
        cls.excluded_tests = excluded_tests
        cls.threadList = []
        cls.test_results = {}
        cls._prepare_thread_tests()

    @classmethod
    def run_tests(cls):
        """
        The non-disruptive tests are invoked followed by the disruptive
        tests and excluded tests are displayed in the end.
        """
        for test_thread in cls.threadList:
            test_thread.start()

        for test_thread in cls.threadList:
            test_thread.join()

        thread_flag = False

        for test in cls.non_concur_test:
            cls.test_results[test['moduleName'][:-3]] = []

        for test in cls.non_concur_test:
            cls._run_test(test, thread_flag)

        if len(cls.excluded_tests) > 0:
            print("Excluded tests: " + str(len(cls.excluded_tests)))
            for test in cls.excluded_tests:
                print(Fore.YELLOW + test)

            print(Style.RESET_ALL)

        return cls.test_results

    @classmethod
    def _prepare_thread_tests(cls):
        """
        This method creates the threadlist for non disruptive tests
        """
        thread_flag = True

        for test in cls.concur_test:
            cls.test_results[test['moduleName'][:-3]] = []

        for test in cls.concur_test:
            cls.threadList.append(Thread(target=cls._run_test,
                                         args=(test, thread_flag,)))

    @classmethod
    def _run_test(cls, test_dict: dict, thread_flag: bool):
        """
        A generic method handling the run of both disruptive and non
        disruptive tests.
        """
        if thread_flag:
            cls.semaphore.acquire()
        tc_class = test_dict["testClass"]
        tc_log_path = cls.base_log_path+test_dict["modulePath"][5:-3]+"/" +\
            test_dict["volType"]+"/"+test_dict["moduleName"][:-3]+".log"

        # to calculate time spent to execute the test
        start = time.time()
        runner_thread_obj = RunnerThread(tc_class, cls.param_obj,
                                         test_dict["moduleName"][:-3],
                                         test_dict["volType"], tc_log_path,
                                         cls.log_level, thread_flag)
        test_stats = runner_thread_obj.run_thread()

        test_stats['timeTaken'] = time.time() - start
        result_text = test_dict["moduleName"][:-3]+"-"+test_dict["volType"]
        if test_stats['testResult']:
            test_stats['testResult'] = "PASS"
            result_text += " PASS"
            print(Fore.GREEN + result_text)
            print(Style.RESET_ALL)
        else:
            result_text += " FAIL"
            test_stats['testResult'] = "FAIL"
            print(Fore.RED + result_text)
            print(Style.RESET_ALL)
        if thread_flag:
            cls.semaphore.release()

        cls.test_results[test_dict['moduleName'][:-3]].append(test_stats)
