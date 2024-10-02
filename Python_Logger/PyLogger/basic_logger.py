import logging

logger = logging.getLogger(__name__)

# instantiation
console_handler = logging.StreamHandler() # sends logs to console
file_handler = logging.FileHandler( # sends log to the file 
    "app.log",  # file name
    mode="a",   # append
    encoding="utf-8")
# addition to the logger

logger.addHandler(console_handler)
logger.addHandler(file_handler)

# handlers can be seen with:
print(logger.handlers)

# test of logging
logger.warning("Test1")