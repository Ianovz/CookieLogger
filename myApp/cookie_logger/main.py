import argparse
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(levelname)s : %(message)')


class CookieLogger:
    """
        A class to parse a cookie log file and find the most active cookies for a given day.

        Attributes:
            filepath (str): The path to the cookie log file.
            cookie_counters (dict): A dictionary to count occurrences of each cookie.
        """

    def __init__(self, filepath):
        """
            Initializes the CookieLogger with a specific log file path.

            Parameters:
                filepath (str): The path to the cookie log file.
        """
        self.filepath = filepath
        self.cookie_counters = {}

    def parse_log_file(self, target_date):
        """
            Parses the log file and counts occurrences of cookies for a given target date.

            Parameters:
                target_date (str): The date for which to find cookies, in "YYYY-MM-DD" format.
        """
        line_nr = 0
        try:
            with open(self.filepath, 'r') as file:
                try:
                    next(file)  # try skipping header
                    line_nr += 1
                except StopIteration:
                    logging.info("The file is empty.")
                    return

                for line in file:
                    line_nr += 1
                    try:
                        cookie, timestamp = line.strip().split(',')
                        date = timestamp.split('T')[0]  # extracts the date in "YYYY-MM-DD" format
                        if date == target_date:
                            self.cookie_counters[cookie] = self.cookie_counters.get(cookie, 0) + 1
                    except ValueError as e:
                        logging.warning(f"Line {line_nr} was malformed: {line.strip()}. Error: {e}")
        except FileNotFoundError:
            logging.error(f"The file {self.filepath} was not found.")
            raise FileNotFoundError(f"The file {self.filepath} was not found.")

        except PermissionError:
            logging.error(f"Permission denied when trying to read {self.filepath}.")
            raise PermissionError(f"Permission denied when trying to read {self.filepath}.")

    def find_most_active_cookies(self):
        """
            Identifies and returns the most active cookies for the target date.

            Returns:
                A list of cookies (str) that were most active on the target date.
        """
        if not self.cookie_counters:
            logging.info("No cookies found for the given date.")
            return []
        max_count = max(self.cookie_counters.values())
        most_active_cookies = [cookie for cookie, counter in self.cookie_counters.items() if counter == max_count]
        return most_active_cookies


def valid_date(s):
    """
        Validates the format of the date string.

        Parameters:
            s (str): The date string to validate.

        Returns:
            datetime.date: The validated date.

        Raises:
            argparse.ArgumentTypeError: If the date string is not in the expected format.
        """
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        msg = "The date is not valid: '{0}'. Expected format is YYYY-MM-DD.".format(s)
        raise argparse.ArgumentTypeError(msg)


def main():
    """
        Parses command-line arguments and finds the most active cookies for a given date.
    """
    parser = argparse.ArgumentParser(description="Find the most active cookie in a log file for a specific date.")
    parser.add_argument('-f', '--file', required=True, help="Filepath of the cookie log file")
    parser.add_argument('-d', '--date', required=True, help="Target date in YYYY-MM-DD format", type=valid_date)
    args = parser.parse_args()

    cookie_logger = CookieLogger(args.file)
    cookie_logger.parse_log_file(args.date.strftime("%Y-%m-%d"))
    most_active_cookies = cookie_logger.find_most_active_cookies()

    for cookie in most_active_cookies:
        print(cookie)


if __name__ == '__main__':
    main()
