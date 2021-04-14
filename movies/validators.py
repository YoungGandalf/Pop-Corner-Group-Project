from django.core.exceptions import ValidationError
import re


# Validates the length of the name is less than 200
def validate_name_length(value):
    length = len(value)  # get length of the input
    if length > 100:
        raise ValidationError("The length of the this field must be less than 100 characters long")
    else:
        return value


# Validates the name only contains alphabetical characters and digits
def validate_username_alphadigits(value):
    validmatch = re.match('^[\w]+$', value)
    if not validmatch:
        raise ValidationError("The username can only contain alphabetical characters and numbers")
    else:
        return value


# Validates the length of the password is minimum of size 8 and less than 256
def validate_password_length(value):
    length = len(value)  # get length of the input
    if length < 8 or length > 256:
        raise ValidationError("The password must be at least 8 characters in length and no greater than 30 characters")
    else:
        return value


# Validates the password contains at least one digit
def validate_password_digit(value):
    if not re.search(r"[\d]+", value):  # searches for a digit
        raise ValidationError("The password must contain at least one digit")
    else:
        return value


# Validates the password contains at least one uppercase character
def validate_password_uppercase(value):
    if not re.search(r"[A-Z]+", value):  # searches for an uppercase character
        raise ValidationError("The password must contain at least one uppercase character")
    else:
        return value


# Validates the phone number
def validate_phonenumber(value):
    # Possible formats for the phone number: (###)###-###, ###-###-###, ##########, or ###########
    regex = r"\(\w{3}\)\w{3}-\w{4}"
    regex2 = r"\w{3}-\w{3}-\w{4}"
    regex3 = r"\b\w{10,11}\b"
    # If the number does not match any of the phone number formats then raise an error
    if not re.search(regex, value) and not re.search(regex2, value) and not re.search(regex3, value):
        raise ValidationError(
            "The phone number must be in format (###)###-###, ###-###-###, ##########, or ########### ")
    else:
        return value


def validate_zip_code(value):
    # Regex to check for 5 digits in a row and no other data in the field
    regex = r"^\d{5}$"

    if re.search(regex, value):
        return value
    else:
        raise ValidationError("The zip code must be 5 digits 0-9")


def validate_security_code(value):
    # Regex to check for 3 digits in succession with nothing surrounding it
    regex = r"^\d{3}$"

    if re.search(regex, value):
        return value
    else:
        raise ValidationError("The security code must be 3 digits 0-9")


def validate_expiration_date(value):
    # Regex to check for proper date format of mm/yy
    regex = r"^^((0[1-9])|(1[0-2]))\/[2]\d$$"

    if re.search(regex, value):
        return value
    else:
        raise ValidationError("Please enter a valid expiration date in the mm/yy format")


def validate_card_number(value):

    NoSpaceRegex = r"^([0-9]){16}$"
    DashRegex = r"^\d{4}-\d{4}-\d{4}-\d{4}$"
    SpaceRegex = r"^\d{4}\s\d{4}\s\d{4}\s\d{4}$"

    # Return formatted card number based on which format was given
    if re.search(NoSpaceRegex, value) or re.search(DashRegex, value) or re.search(SpaceRegex, value):
        return value

    else:
        raise ValidationError(
            "Please enter a 16 digit credit card number using spaces, dashes, or nothing in between the numbers.")
