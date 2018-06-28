import hashlib
class BaseConverter:
    def __init__(self):
        # self.base = base
        # self.baseCharacters = characters
        pass

    def findHighestPower(self, number, base, power = 0):
        if number // (base ** power) < base:
            return power
        return self.findHighestPower(number, base, power + 1)

    def convertToBase(self, number, power, base):
        if power == 0:
            lsd = number // base
            return self._baseCharacters[lsd]
        else:
            msd = number // (base ** power)
            return self._baseCharacters[msd] + self.convertToBase(
                    number - (msd * base**power),
                    power - 1, base)

    def convert(self, number):
        highestPower = self.findHighestPower(number, self._base)
        return self.convertToBase(number, highestPower,self. _base)

    def setBaseCharacters(self, characters):
        self._baseCharacters = characters
        self._base = len(characters)

    @property
    def base(self):
        return self._base

    @property
    def characterSet(self):
        return self._baseCharacters

if __name__ == "__main__":
    # basic test suite
    CHARACTERS = '01234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    url = 'http://www.somename.com/'
    converter = BaseConverter()
    converter.setBaseCharacters(CHARACTERS)

    m = hashlib.sha256()
    m.update(url.encode('utf-8'))

    hashVal = m.hexdigest()[:8]
    hashCode = converter.convert(int(hashVal, 16))
    print(converter.base)
    print(hashVal, hashCode)
