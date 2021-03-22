"""
This module takes care of:
1) Config file parsing (by gluster_test_parser).
2) Tests-to-run list preparation (by test_list_builder).
3) Invocation of the test_runner.
"""

import argparse
from parsing.redant_params_handler import ParamsHandler


def pars_args():
    """Parse arguments with argparse module
    """

    parser = argparse.ArgumentParser(
        description='Create config hashmap based on config file')
    parser.add_argument("-c", "--config",
                        help="Config file(s) to read.",
                        action="store", dest="config_file",
                        default=None, type=str, required=True)
    parser.add_argument("-t", "--test-dir",
                        help="The test directory where TC(s) exist",
                        dest="test_dir", default=None, type=str, required=True)
    parser.add_argument("-l", "--log-dir",
                        help="The directory wherein log will be stored.",
                        dest="log_fir", default="/tmp/redant", type=str)
    return parser.parse_args()


def main():
    """
    Invocation order being.
    1. Parsing the command line arguments.
    2. Parsing the config file to get the configuration details.
    3. Invoking the test_list_builder to build the TC run order.
    4. Passing the details to the test_runner.
    """
    args = pars_args()

    if args.config_file:
        ParamsHandler.get_config_hashmap(args.config_file)


if __name__ == '__main__':
    main()
