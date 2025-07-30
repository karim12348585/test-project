# change file name
# Type in code here
import logging

logger = logging.getLogger()


class MyModule:
    @staticmethod
    def my_function(self):
        logger.info("This will be logged to console and file for my_function method")
        pass


def main():
    """
    the main entrypoint for this script used in the setup.py file

    """
    MyModule.my_function()


if __name__ == "__main__":
    main()
