"""
This file contains a test-case which tests
volume operations like creation and deletion
"""


class TestCase:
    """
    The test case contains one function to test
    for volume creation and deletion
    """

    def __init__(self, remote_exec: object):
        """
        This init function initializes the remote_exec
        class variable which is mixin object passed as a
        reference by runner_thread.
        Args:
            remote_exec (object): mixin object passed as reference.
        """
        self.remote_exec = remote_exec

    def volume_create_delete_test(self):
        """
        The following steps are undertaken in the testcase:
        1) glusterd service is started on the server.
        2) Volume is created on the server node.
        3) Volume is deleted on the server node.
        4) glusterd service is stopped.
        """
        try:

            self.remote_exec.gluster_start("10.70.43.63")

            self.remote_exec.volume_create("10.70.43.63", "test-vol",
                                           ["10.70.43.63:/brick1"],
                                           force=True)
            self.remote_exec.volume_delete("10.70.43.63", "test-vol")

            self.remote_exec.gluster_stop("10.70.43.63")
            print("Test Passed")

        except Exception as error:
            print(f"Test Failed:{error}")
