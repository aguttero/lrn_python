
import logging

# DEBUG: Detailed information, typically of interest only when diagnosing problems.
# INFO: Confirmation that things are working as expected.
# WARNING: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
# ERROR: Due to a more serious problem, the software has not been able to perform some function.
# CRITICAL: A serious error, indicating that the program itself may be unable to continue running.

# Default level set to #3 -> Warning or Higher


# si no agregamos esta linea el nombre del logger es 'root'
logger = logging.getLogger("this_module_name")
# logger = logging.getLogger(__name__)

logging.basicConfig(filename='./logging/test.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')


def add(x, y):
    """Add Function"""
    return x + y


def subtract(x, y):
    """Subtract Function"""
    return x - y


def multiply(x, y):
    """Multiply Function"""
    return x * y


def divide(x, y):
    """Divide Function"""
    return x / y


num_1 = 20
num_2 = 10

add_result = add(num_1, num_2)
print('Add: {} + {} = {}'.format(num_1, num_2, add_result))
logger.debug(f'Add: {num_1} + {num_2} = {add_result}')
logging.debug(f'Add: {num_1} + {num_2} = {add_result}') # el name va a ser -> root


sub_result = subtract(num_1, num_2)
logger.debug('Sub: {} - {} = {}'.format(num_1, num_2, sub_result))

mul_result = multiply(num_1, num_2)
logger.debug('Mul: {} * {} = {}'.format(num_1, num_2, mul_result))

div_result = divide(num_1, num_2)
logger.debug('Div: {} / {} = {}'.format(num_1, num_2, div_result))