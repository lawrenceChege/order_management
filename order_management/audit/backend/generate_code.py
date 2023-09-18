""" Helper methods for audit module """


def generate_fixed_length_code(start_character: str = 'A', code: str = '1', filler: str = '0', length: int = 9) -> str:
	"""
	This generates a code of specified length
	@param start_character : Specify the character to start the code
	@type start_character: str
	@param code: The unique code to append
	@type code: str
	@param filler: The element to use as a filler
	@type filler: str
	@param length: To specify the length of the code
	@type length: int
	@return code : The alphanumeric code generated
	@type code: str
	"""
	length = length - len(start_character)
	code = code.rjust(abs(length), filler)
	return "{}{}".format(start_character, code)


def increment_alphabetical_character(character: str) -> str:
	"""
	Increment from A to Z
	@param character: The alphabet character to increment
	@type character: str
	@return : The next alphabetical character
	@type : str
	"""
	allowed = [
		'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
		'V', 'W', 'X', 'Y', 'Z']
	next_character = chr(ord(character) + 1)
	if next_character in allowed:
		return next_character
	return increment_alphabetical_character(next_character)


def increment_alphanumeric_character(character: any) -> str:
	"""
	Increment from 0-9 to A-Z
	@param character: The alphanumeric character to increment
	@type character: any
	@return : The next alphanumeric character
	@type : str
	"""
	if character == 9:
		return "A"
	if character == "Z":
		return "0"
	if isinstance(character, str) and character != "Z":
		return increment_alphabetical_character(character)
	if isinstance(character, int) and character != "9":
		return str(character + 1)
	

def generate_internal_reference(last_reference: str = None) -> str:
	"""
		This function generates the internal reference number.
		@param last_reference: The last reference to be generated. If None, the starting pattern is used.
		@type last_reference: str | None
		@return: The generated reference number.
		@rtype: str
	"""
	if last_reference:
		index = -1
		ref = last_reference[index:]
		code = last_reference[:index]
	else:
		ref = '0'
		code = generate_fixed_length_code()
	r = increment_alphanumeric_character(ref)
	return code + r