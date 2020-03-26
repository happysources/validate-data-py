#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Validate function
"""

import six
from logni import log


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
		value = int(value)
	except ValueError as val_err:
		raise TypeError(('{name_str} expected int, {value_error}').format(\
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


def validate_email(value, required=True, name=None):
	""" validate email """

	ret = validate_str(value, 6, 100, required, name)
	if not ret:
		return False

	if not value:
		return ret

	name_str = __name(name)
	emails = value.split('@')
	if len(emails) != 1:	
		log.error('%s must be a format name@domain.tld', (name_str,), priority=2)
		return False

	domains = emails[1].split('.')
	if len(domains[-1]) < 2:
		log.error('%s must be a format name@domain.tld', (name_str,), priority=2)
		return False

	return True


def validate_ip(value, required=True, name=None):
	""" validate ip address """

	name_str = __name(name)
	log.debug('ip %s value=%s, required=%s', (name_str, value, required))

	ret = validate_str(value, 7, 15, required, name)
	if not ret:
		return False

	if not value:
		return ret

	ips = value.split('.')
	if len(ips) != 4:
		log.error('%s must be a format 0.0.0.0', (name_str,), priority=2)
		return False

	for ip in ips:
		if not validate_int(ip, 1, 255, True, 'ip'):
			return False

	return True


def validate_array(value, arr, required=True, name=None):
	""" validate for array/tuple """

	name_str = __name(name)
	log.debug('array %s %s in %s, required=%s', (name_str, value, arr, required))

	if arr:	
		if type(value) not in (type([]), type(())):
			value = (value,)

		for value1 in value:
			if value1 not in arr:
				log.error('array %s=%s not in %s', (name, value1, arr), priority=1)
				raise ValueError(('{name} value out of array').format(name=name_str))

			elif value1 in arr:
				continue

	if type(value) in (type([]), type(())):
		return True

	log.error('array %s=%s must be a array', (name, value), priority=1)
	raise ValueError(('{name} must be a array').format(name=name_str))



if __name__ == '__main__':

	print('int:')
	print('-ok : 10', validate_int(10, 1, 100, True, 'numbername'))
	print('-ok : 10', validate_int('10'))
	#print('-err: xxx', validate_int('xxx', name='numbername'))
	#print('-err:', validate_int(None, 1, 10, True, name='numbernone'))
	print('-err: None', validate_int(None, 1, 10, False, name='numbernone'))
	print('-ok : 10', validate_int(10, 1, 10, False, name='numbernone'))

	print()
	print('str:')
	print('-ok : aaa', validate_str('aaa', 1, 10, True, 'stringname'))
	#print('-err:', validate_str(None, 1, 10, True, 'stringnone'))
	print('-ok : None', validate_str(None, 1, 10, False, 'stringnone'))

	print()
	print('ip:')
	print('-ok : 1.2.3.4', validate_ip('1.2.3.4', True, 'ip'))
	print('-err: 11.222.33', validate_ip('11.222.33', True, 'ip'))

	print()
	print('email:')
	print('-ok : email@domain.tld', validate_email('email@domain.tld'))
	print('-err: email@domain.x', validate_email('email@domain.x'))
