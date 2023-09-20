# -*- coding: utf-8 -*-
"""
System input validators
"""
from datetime import datetime, date
import re
import logging
from uuid import UUID

from django.conf import settings

# from base.backend.utils.commons import normalize_date

lgr = logging.getLogger(__name__)


def validate_email(email: str) -> bool:
	"""
	Checks if the email provided is a valid email address
	Should conform to the django email standard:
		- at least 8 characters
		- contain one @
		- contain at least 2 '.'
	@param email: the email address to be validated
	@type email: str
	@return: True if valid else False
	@rtype: bool
	"""
	try:
		if len(email) > 4:
			email = str(email).lower().replace(" ", "")
			if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) is not None:
				return True
			return False
		return False
	except Exception as e:
		lgr.error('validate_email: %s', e)
	return False


def validate_name(name: str, min_length: int = 3, max_length: int = 50) -> bool:
	"""
	Checks if the provided name:
		- contains only alphabet characters
		- len(name) is within specified min_length and max_length
		- doesn't contain any spaces within
	@param name: name passed to be validated
	@type name: str
	@param min_length: minimum length of name
	@type min_length: int
	@param max_length: maximum length of name
	@type max_length: int
	@return: True if valid else False
	@rtype: bool
	"""
	try:
		name = str(name).strip()
		if not re.match(r"(^[a-zA-Z\s]+$)", name) and len(name.split()) > 1:
			return False
		if min_length <= len(name) <= max_length:
			return True
	except Exception as e:
		lgr.error('validate_name: %s', e)
	return False


def normalize_phone_number(phone, country_code=None, total_count: int = None):
	"""
	Normalize a phone number ensuring that:
		- it has a valid country code
		- required number of characters
		- all characters are digits
	@param phone: The phone number passed to be normalized
	@type phone: str
	@param country_code: The country code for the phone
	@type country_code: str
	@param total_count: The total digits required
	@type total_count: int
	@return: a normalized phone number
	@rtype: str
	"""
	try:
		if country_code is None:
			country_code = settings.DEFAULT_COUNTRY_CODE
		if total_count is None:
			total_count = settings.PHONE_NUMBER_LENGTH
		phone = phone.replace(" ", "").replace('(', '').replace(')', '').replace('-', '')
		if str(phone).startswith('+'):
			phone = str(phone)[1:]
		if len(phone) == total_count:
			return phone
		elif (len(phone) + len(country_code)) == total_count:
			return str(country_code) + str(phone)
		elif str(phone).startswith('0') and ((len(phone) - 1) + len(country_code)) == total_count:
			return str(country_code) + str(phone)[1:]
		else:
			if len(country_code) > 0:
				overlap = abs((len(phone) + len(country_code)) - total_count)
				return str(country_code) + str(phone)[overlap - 1:]
			else:
				return phone
	except Exception as ex:
		lgr.exception('normalize_phone_number Exception: %s', ex)
		return None


def validate_phone_number(phone_number, country_code=None, total_count=None):
	"""
	Checks if provided phone number is valid
	@param phone_number: phone_number being validated
	@type phone_number: str
	@param country_code: The country code for the phone
	@type country_code: str
	@param total_count: The total digits required
	@type total_count: int
	@return: True if valid else False
	@rtype: bool
	"""
	return re.match(r'^[0-9]{9,15}$', normalize_phone_number(phone_number, country_code, total_count)) is not None


def validate_password(password):
	"""
	Validate whether the Password has:
		- at least 8 characters
		- an uppercase letter
		- a lowercase letter
		- Allowed special characters: @ # ! $ & / \\ + - [ ] { }
		- Disallowed: \\~=[]{}^%
	"""
	allowed = set(r'@#!$&/+-_*')
	illegal = set(r'\~=[]{}^%')
	if (len(password) > 7) and (re.search('[0-9]', password) is not None) and (
			re.search('[A-Z]', password) is not None) and (re.search('[a-z]', password) is not None) and any(
		(a in allowed) for a in password) and (not any((i in illegal) for i in password)):
		return True
	return False


def validate_amount(amount):
	"""
	Checks whether the passed amount:
		- is of type Decimal
	"""
	try:
		import numbers
		import decimal
		amount = decimal.Decimal(amount)
		if isinstance(amount, (numbers.Real, decimal.Decimal)):
			return True
	except Exception as e:
		lgr.error('validate_amount Exception: %s', e)
	return False


def normalize_amount(amount):
	"""
	Normalizes amount by removing special characters.
	"""
	try:
		return str(amount).replace(",", "").replace(" ", "")
	except Exception as e:
		lgr.error('validate_amount Exception: %s', e)
	return False


def validate_uuid7(uuid_string):
	"""
	Validate that a UUID string is in fact a valid uuid4.
	Happily, the uuid module does the actual checking for us.
	It is vital that the 'version' kwarg be passed to the UUID() call, otherwise any 32-character
	hex string is considered valid.
	"""
	# noinspection PyBroadException
	try:
		uuid_string = str(uuid_string).strip()
		_ = UUID(uuid_string, version=4)
	except Exception:
		# If it's a value error, then the string
		# is not a valid hex code for a UUID.
		return False
	return True


# noinspection PyBroadException
# def validate_date(date_text):
	# """
	# Check whether the passed in date is of the correct format
	# """
	# try:
	# 	if isinstance(date_text, (datetime, date)) or normalize_date(date_text):
	# 		return True
	# except Exception:
	# 	pass
	# return False
