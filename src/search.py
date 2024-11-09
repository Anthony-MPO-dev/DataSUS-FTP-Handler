import argparse
import logging
import os
import sys
from datetime import datetime

# Adds the base directory to sys.path for module access
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

from datetime import datetime

from src.modules.data_processing.convert_to_csv import (
    converter_dbc_para_dbf,
    converter_dbf_para_csv,
)
from src.modules.data_processing.init_cleaning import cleaning_data

# from src.modules.webscraping.scraper.search import start_search
from src.modules.post_request.post_search import start_search_resquest

# Retrieve the current year
current_year = datetime.now().year

# Define available years range
AVAILABLE_YEARS = list(range(2001, current_year + 1))

# Theme conversion dictionary
theme_converter = {
    'TU': 'TUBE',
    # Add other conversion pairs as needed
}

path_src = (
    os.path.abspath(__file__).split('/src')[0] + '/src/'
)  # Path to the project's source directory


def validate_years(years):
    """Validates the year range argument.

    If no years are provided, it defaults to all available years. Raises an error if
    the input format is incorrect or if the years are out of the available range.

    Args:
    -----
    years : str
        Year range in 'YYYY-YYYY' format.

    Returns:
    --------
    list
        List of years within the specified range.

    Raises:
    -------
    argparse.ArgumentTypeError
        If the input format is incorrect or the years are out of range.
    """
    if not years:
        return AVAILABLE_YEARS

    try:
        init_year, end_year = map(int, years.split('-'))
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Error: The year format should be 'YYYY-YYYY'. Example: '2001-2005'."
        )

    if (
        init_year not in AVAILABLE_YEARS
        or end_year not in AVAILABLE_YEARS
        or init_year > end_year
    ):
        raise argparse.ArgumentTypeError(
            f'Error: Year range must be within: {AVAILABLE_YEARS[0]}-{AVAILABLE_YEARS[-1]}.\n'
            f"Example: '2001-2005'. Provided: '{init_year}-{end_year}'."
        )

    return list(range(init_year, end_year + 1))


def configure_logging():
    """Sets up logging to save logs to a specified file.

    Configures both file and console logging handlers, creating the log directory if it
    doesn't exist. Also redirects `stderr` to the logger.

    Returns:
    --------
    logging.Logger
        Configured logger instance.
    """
    # Define log file path and name
    current_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    path_log = path_src + f'log/{current_date}_search.log'

    # Create the log directory if it doesn't exist
    os.makedirs(os.path.dirname(path_log), exist_ok=True)

    # Setup logging configuration
    logging.basicConfig(
        level=logging.INFO,  # Set default level to INFO
        format='%(asctime)s - %(levelname)s - [%(funcName)s] - %(message)s',
        handlers=[
            logging.FileHandler(path_log),
            logging.StreamHandler(sys.stdout),  # Display logs in console
        ],
    )

    # Redirects stderr to the logger
    sys.stderr = StreamToLogger(logging.getLogger('STDERR'), logging.ERROR)

    logger = logging.getLogger(__name__)
    return logger


class StreamToLogger:
    """Redirects stream output (like stderr) to a logger.

    Parameters:
    -----------
    logger : logging.Logger
        The logger instance to receive the output.
    log_level : int
        Logging level for the redirected output, defaulting to INFO.
    """
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass  # Necessary for stream compatibility


def configure_parameters(logger: logging.Logger) -> argparse.Namespace:
    """
    Configure and define command-line arguments for the Web Scraping program.

    Uses `argparse` to define and validate required and optional parameters for the
    script. Logs errors if parsing fails.

    Parameters:
    -----------
    logger : logging.Logger
        Logger instance for error messages and logging.

    Returns:
    --------
    argparse.Namespace
        Parsed arguments object with values for each argument.

    Exceptions:
    -----------
    argparse.ArgumentError
        Raised if command-line argument parsing fails.
    """
    parser = argparse.ArgumentParser(
        description='Web Scraping and Data Analysis Program.',
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Primary arguments
    parser.add_argument(
        '-log',
        '--log',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Logging level (default: INFO). Options: DEBUG, INFO, WARNING, ERROR, CRITICAL. Example: --log DEBUG.',
    )
    parser.add_argument(
        '-t',
        '--theme',
        required=True,
        choices=['TU'],
        help="Extraction theme, e.g., 'TU' for Tuberculosis. Example: --theme TU.",
    )
    parser.add_argument(
        '-y',
        '--years',
        type=validate_years,
        help="Year range in 'YYYY-YYYY' format. Example: --years 2001-2005.",
    )

    # Optional arguments
    parser.add_argument(
        '-c',
        '--clean',
        action='store_true',
        help='Runs the cleaning function after execution. Example: --clean.',
    )

    parser.add_argument(
        '-b',
        '--browser_mode',
        choices=['visible', 'headless'],
        default='headless',
        help='Browser mode: "visible" for GUI or "headless" for hidden mode (default). Example: --browser_mode visible.',
    )

    # Parse arguments
    try:
        args = parser.parse_args()
        return args
    except argparse.ArgumentError as e:
        logger.error(f'Argument parsing error: {e}\n')
        parser.print_help()
        sys.exit(1)


def start_program():
    """Initializes the program, processes arguments, and configures logging.

    Sequentially logs each stage of execution, starting from argument setup, validating,
    configuring the logging level, running web scraping, data processing, and optional
    cleaning based on provided arguments.
    """
    logger = configure_logging()

    # Log program start
    logger.info('\n\n')
    logger.info('=' * 50)
    logger.info(' PROGRAM STARTING ')
    logger.info('=' * 50 + '\n')

    logger.info('Step 1/6: Configuring program arguments...')

    # Argument verification
    args = configure_parameters(logger)

    logger.info('Step 2/6: Arguments configured successfully.')
    logger.info('Updating logging level...')

    # Update logging level based on user input
    logger.setLevel(args.log.upper())
    logger.info('Program starting with provided arguments.')

    try:
        logger.info('Step 3/6: Validating arguments...')
        logger.info('-' * 20)
        logger.info(f'Extraction theme: {args.theme}')
        logger.info(
            f"Selected years: {args.years if args.years else f'All available [{AVAILABLE_YEARS[0]}-{AVAILABLE_YEARS[-1]}]'}"
        )
        logger.info(f'Browser mode: {args.browser_mode}')

        logger.info(f"Post-execution cleaning: {'Yes' if args.clean else 'No'}")
        logger.info('-' * 20)
        logger.info('\n')

        # Initiate data extraction via WebScraping
        logger.info(
            'Step 4/6: Performing Extraction and Downloading Files...'
        )

        # start_search(
        #     args.theme,
        #     args.browser_mode,
        #     (args.years if args.years else AVAILABLE_YEARS),
        # )

        start_search_resquest(
            theme_converter[args.theme],
            (args.years if args.years else AVAILABLE_YEARS),
        )

        logger.info('Step 5/6: Processing data...')

        caminho_arquivo = os.path.abspath(__file__).split('/src')[0]

        # Example usage
        diretorio_entrada_dbc = caminho_arquivo + '/src/data/raw/'
        diretorio_saida_dbf = caminho_arquivo + '/src/data/processed/'
        diretorio_saida_csv = diretorio_saida_dbf

        # Convert DBC files to DBF
        converter_dbc_para_dbf(diretorio_entrada_dbc, diretorio_saida_dbf)

        # Convert DBF files to CSV
        converter_dbf_para_csv(diretorio_saida_dbf, diretorio_saida_csv)

        logger.info('\n')
        logger.info('Starting Data Cleaning and Processing:')

        cleaning_data(diretorio_saida_csv)

        # Execute cleanup if --clean argument is provided
        if args.clean:
            logger.info('\n')
            logger.info('-' * 20)
            logger.info('Step 6/6: Executing obsolete file cleanup...')
            # Check and remove files in directory
            # Check each file in the directory and delete if the "clean" argument is passed.
            for root, dirs, files in os.walk(diretorio_saida_csv):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        os.remove(file_path)
                        logger.info(f'Deleted obsolete file: {file_path}')
                    except Exception as e:
                        logger.error(f'Error deleting file {file_path}: {e}')

        logger.info('\n')
        logger.info('=' * 50)
        logger.info(' PROGRAM COMPLETED SUCCESSFULLY ')
        logger.info('=' * 50 + '\n')
    except Exception as e:
        logger.error(f'An unexpected error occurred: {e}')
        sys.exit(1)


if __name__ == '__main__':
    start_program()
