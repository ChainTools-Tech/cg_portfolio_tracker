import argparse


def process_command_line():
    """Command line processor

    :return: name of file with list of hostnames to check
    """
    cmdparser = argparse.ArgumentParser()
    cmdparser.version = "0.1"
    cmdparser.add_argument("-f", "--file", type=str, action="store", dest="file",  required=True, help="specifies input file")
    cmdparser.add_argument("-v", "--version",  action="version")

    args = cmdparser.parse_args()

    return args
