from abc import ABC


class Parent_Test(ABC):

    """
    This class contains the standard info and methods which are needed by
    most of the tests
    """

    _PASS: bool = True
    _FAIL: bool = False

    _TEST_RES: bool = _PASS

    COMPONENT: str
    TEST_NAME: str


    def core_init(self):
        """
        Establishes ssh connection
        Since added in redant_mixin so
        can call establish_connection directly
        """

        self.establish_connection()

    def init(self):
        """
        Establishes connection by calling core_init
        Creates volume
        And runs the specific component in the
        test case
        """

        self.core_init()
        self.rlog(f"{self.TEST_NAME} from {self.COMPONENT} inits")

    def run_test(self):
        """
        It will be overriden by Test cases
        """
        pass

    def terminate(self):
        """
        Deletes the volume
        Closes connection
        """

        self.rlog(f"{self.TEST_NAME} terminates")