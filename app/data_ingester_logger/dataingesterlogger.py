import logging


class DataIngesterLogger:
    FORMAT = '%(asctime)s-%(module)s::%(lineno)d-%(levelname)s : %(message)s'
    logging.basicConfig(format=FORMAT)

    def __init__(self, logger_name: str, stack_level: int = 2):
        """
        Initialize the looger.
        :param logger_name: The name of the logger to get.
        :param stack_level: The stack level of the logger to fix line number and module.
        :return: the logger.
        """
        self._logger = logging.getLogger(logger_name)
        self._stack_level = stack_level

    def info(self, message: str) -> None:
        """
        send an info level log.
        :param message: message to log.
        :return: None
        """
        self._logger.setLevel(logging.INFO)
        self._logger.info(message, stacklevel=self._stack_level)

    def error(self, message: str) -> None:
        """
        send an error level log.
        :param message: message to log.
        :return: None
        """
        self._logger.setLevel(logging.ERROR)
        self._logger.error(message, stacklevel=self._stack_level)
