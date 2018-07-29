import hashlib, string
"""
A general class for converting decimal integers into a differnt radix

Designed for use with the flask app, urlShorterner, which turns urls
into a hash value and then uses BaseConverter to convert to a new
number for use as a shortened url

Setting a radix value or a characterSet is required before calling
convert, the only public method.

Todo:
    * allow negative numbers
    * allow non-decimal numbers to be entered as strings and literals
    (i.e., 0xa3c8)
"""
class BaseConverter:
    def __init__(self):
        self._radix = None
        self._characters = None

    def _findHighestPower(self, number, power = 0):
        """
        helper function: finds the number of digits of a
        decimal number in a base-n number system

        Used in _convertToBase
        equivalent to: Math.log(number, self._radix) + 1

        @param number The integer (i.e., decimal) number to be converted
        @param power A starting value for the recursive call
        @return An integer value
        """
        if number // (self._radix ** power) < self._radix:
            return power
        return self._findHighestPower(number, power + 1)

    def _convertToBase(self, number, power):
        """
        helper function for convert
        @param number The integer to be converted
        @param power The number of digits
        @return string A string: represenation fo the base-n number
        """
        if power == 0:
            return self._characters[number]
        else:
            msd = number // (self._radix ** power)
            return self._characters[msd] + self._convertToBase(
                    number - (msd * self._radix**power),
                    power - 1)

    def convert(self, number, inputRadix=10):
        """
        the main public method
        converts a number of the inputRadix to a base-BaseConverter.radix
        nubmer in string represenation form

        BaseConverter.characterSet controls the characters
        and ordering used

        @param number An integer
        @param inputBase To extend functionality later
        @return A string representation of the base-n number
        @throws AttributeError if no characters have been set
        """
        if self._characters is None:
            raise AttributeError('Must assign a character set first')
        if number < 0:
            raise AttributeError('Number must be non-negative')
        if inputRadix != 10:
            raise AttributeError('inputBase must equal 10; feature not yet implemented.')
        highestPower = self._findHighestPower(number)
        return self._convertToBase(number, highestPower)

    @property
    def radix(self):
        """the radix/base of the encoding number system"""
        return self._radix

    @radix.setter
    def radix(self, newRadix):
        """
        if radix is set, a default character set will be assigned from
        the 62 ascii set of numbers, lowercase, and upercase letters.
        Ordering will be string.numbers + string.ascii_letters

        @param newRadix an integer in range [2, 62]
        @throws AttributeError Input is not in range [2, 62]
        """
        if newRadix < 2 or newRadix > 62:
            raise AttributeError('The radix must be betwen 2 and 62.')
        self._radix = newRadix
        fullCharSet = string.digits + string.ascii_letters
        self._characterSet = fullCharSet[:40]

    @property
    def characterSet(self):
        return self._characters

    @characterSet.setter
    def characterSet(self, characters):
        """
        characterSet controls which characters and the total
        ordering are used in the new
        base-BaseConverter.radix number

        @param characters A string of unique chacters
        @throws AttributeError len(characters) is out of range: [2, 62]
        @throws AttributeError characters contains duplicates
        """
        # check for proper length and duplicates
        if len(characters) < 2 or len(characters) > 62:
            raise AttributeError('The character string must be between 2 and 62.')
        if len(characters) != len(set([x for x in characters])):
            raise AttributeError('The character string has duplicate characters.')
        self._characters = characters
        self._radix = len(characters)

if __name__ == "__main__":
    # basic test suite
    CHARACTERS = string.digits + string.ascii_letters
    converter = BaseConverter()
    try:
        converter.convert(656)
    except AttributeError as e:
        print('Caught attempted conversion without specifiying a radix: ', e)

    converter.characterSet = CHARACTERS

    # change characterSet and check again
    converter.characterSet = '01'
    assert converter.convert(656) == '1010010000'

    # set another characterSet
    converter.characterSet = '0123456789ABCDEF'
    assert converter.convert(656) == '290'

    try:
        converter.characterSet = CHARACTERS + ',.?'
    except AttributeError as e:
        print("Successfully caught string outside of range [2, 62]: ", e)

    try:
        converter.characterSet = '01234567890'
    except AttributeError as e:
        print("Successfully caught string with duplicate: ", e)

    # mutate converting by assinging new radix
    converter.radix = 2
    assert converter.convert(656) == '1010010000'
    converter.radix = 8
    assert converter.convert(656) == '1220'

    try:
        converter.radix = 1;
    except AttributeError as e:
        print("Successfully caught radix assignment error: ", e)

    try:
        converter.convert(-10)
    except AttributeError as e:
        print("Successfully caught negative input to convert: ", e)
