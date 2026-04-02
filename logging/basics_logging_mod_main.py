
import logging
import basics_logging_mod_2

# DEBUG: Detailed information, typically of interest only when diagnosing problems.
# INFO: Confirmation that things are working as expected.
# WARNING: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
# ERROR: Due to a more serious problem, the software has not been able to perform some function.
# CRITICAL: A serious error, indicating that the program itself may be unable to continue running.

# Default level set to #3 -> Warning or Higher

# LOGGER CONFIG
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
console_formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

console_handler = logging.StreamHandler()
console_handler.setFormatter(console_formatter) 
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)

file_handler = logging.FileHandler('./logging/mod_main.log')
file_handler.setFormatter(formatter)
# Permite cambiar el nivel de logging
file_handler.setLevel (logging.ERROR)
logger.addHandler(file_handler)

# OSOLETE:
# logging.basicConfig(filename='./logging/test.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')


def add(x, y):
    """Add Function"""
    return x + y


def subtract(x, y):
    """Subtract Function"""
    return x - y


def multiply(x, y):
    """Multiply Function"""
    return x * y

# Logg error or Exception ERROR EXAMPLE DIVIDE BY ZERO
def divide(x, y):
    """Divide Function"""
    try:
        result = x / y
    except ZeroDivisionError as e:
        logger.error(f'Error message: {e}')
        logger.exception('Exception message -> Traceback')
    else: 
        return result


num_1 = 20
num_2 = 0

add_result = add(num_1, num_2)
print('Add: {} + {} = {}'.format(num_1, num_2, add_result))
logger.debug(f'Add: {num_1} + {num_2} = {add_result}')
# logging.debug(f'Add: {num_1} + {num_2} = {add_result}') # el name va a ser -> root


sub_result = subtract(num_1, num_2)
logger.debug('Sub: {} - {} = {}'.format(num_1, num_2, sub_result))

mul_result = multiply(num_1, num_2)
logger.debug('Mul: {} * {} = {}'.format(num_1, num_2, mul_result))

div_result = divide(num_1, num_2)
logger.debug('Div: {} / {} = {}'.format(num_1, num_2, div_result))