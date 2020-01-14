#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Validate function
"""

import six

def __name(name=None):
	""" name value """

	if not name:
		return ''

	return '%s:' % name


def __min_length(value=None, min_length=0, name_str=None):
	""" text / string: mininal lenght """

	if min_length and len(value) < min_length:
		raise ValueError(('{name_str} expected at least {min_length} characters, '\
			'but string is only {length} characters long'\
        		).format(name_str=name_str, length=len(value), min_length=min_length))


def __max_length(value=None, max_length=0, name_str=None):
	""" text / string: maxima lenght """

	if max_length and len(value) > max_length:
		raise ValueError(('{name_str} expected at most {max_length} characters, '\
			'but string is only {length} characters long'\
        		).format(name_str=name_str, length=len(value), max_length=max_length))


def __min_value(value=None, min_value=0, name_str=None):
	""" integer: min value """

	if min_value and value < min_value:
		raise ValueError(('{name_str} expected value less than {min_value}, but got {value}'\
        		).format(name_str=name_str, value=value, min_value=min_value))


def __max_value(value=None, max_value=0, name_str=None):
	""" integer: max value """

	if max_value and value > max_value:
		raise ValueError(('{name_str} expected value greater than {max_value}, but got {value}'\
        		).format(name_str=name_str, value=value, max_value=max_value))


def validate_int(value=None, min_value=None, max_value=None, required=True, name=None):
	""" validate integer """

	name_str = __name(name)

	if not value and not required:
		return False

	if not value and required:
		raise TypeError(('{name_str} expected int, interger must be input').format(\
			name_str=name_str))

	# convect str->int?
	try:
		int(value)
	except ValueError as val_err:
		return TypeError(('{name_str} expected int, {value_error}').format(\
			name_str=name_str, value_error=val_err))

	__min_value(value, min_value, name_str)
	__max_value(value, max_value, name_str)

	return True


def validate_float(value=None, min_value=None, max_value=None, required=True, name=None):
	""" validate float """

	return validate_int(value, min_value, max_value, required, name)


def validate_str(value=None, min_length=None, max_length=None, required=True, name=None):
	""" validate string """

	name_str = __name(name)

	if not value and not required:
		return False

	if not value and required:
		raise TypeError(('{name_str} expected str, string must be input').format(\
			name_str=name_str))

	if not isinstance(value, six.text_type):
		raise TypeError(('{name_str} expected unicode string, but value is of type {cls!r}'\
        		).format(name_str=name_str, cls=value.__class__.__name__))

	__min_length(value, min_length, name_str)
	__max_length(value, max_length, name_str)

	return True


if __name__ == '__main__':

	print('int:')
	print('-ok :', validate_int(10, 1, 100, True, 'numbername'))
	print('-ok :', validate_int('10'))
	print('-err:', validate_int('xxx', name='numbername'))
	#print('-err:', validate_int(None, 1, 10, True, name='numbernone'))
	print('-err:', validate_int(None, 1, 10, False, name='numbernone'))
	print('-ok :', validate_int(10, 1, 10, False, name='numbernone'))

	print()
	print('str:')
	print('-ok :', validate_str('aaa', 1, 10, True, 'stringname'))
	#print('-err:', validate_str(None, 1, 10, True, 'stringnone'))
	print('-ok :', validate_str(None, 1, 10, False, 'stringnone'))
