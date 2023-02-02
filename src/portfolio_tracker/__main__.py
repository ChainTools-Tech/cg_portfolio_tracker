from portfolio_tracker.app import load_portfolio_file, portfolio_table, prepare_portfolio_data
from portfolio_tracker.cli import process_command_line


def main():
    """
    Main function runs appropriate action depends on passed parameters.

    Returns:
        :return: nothing is returned from main function.
    """
    print("Starting portfolio processing...")

    args = process_command_line()

    input_file = args.file

    portfolio_raw_data = load_portfolio_file(input_file)
    portfolio_list, reference_currency = prepare_portfolio_data(portfolio_raw_data)
    portfolio_table(portfolio_list, reference_currency)


if __name__ == '__main__':
    main()
