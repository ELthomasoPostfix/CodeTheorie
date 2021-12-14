from src.Utils.Utils import toLatin
from math import log10



"""
    Heavy inspiration from http://practicalcryptography.com/ and their ngram_score.py module
"""
class LatinNGrams:
    def __init__(self, ifileName: str, statType: str, delimiter=" "):
        """
        Calculate and keep track of the logFrequencies of ngrams.
        Ignore case.
        :param ifileName: The file containing the frequency statistics.
                The file must exclusively contain ngrams of the same length.
                The file must contain rows of the following format:
                the ngram followed by a delimiter followed by the frequency statistic.
        :param statType: NGrams accepts the CF and PF types of statistics.
                CF stands for count frequency and is the amount of times a ngram
                was recognized in a text.
                PF stands for percentage frequency and is the percentage chance
                that a randomly selected ngram is the ngram in question.
                e.g. if the letter E appears 13% of the time, then
                'E 0.13' is a row in the file.
        :param delimiter: The delimiter to expect in the input file.
        """
        if statType != 'CF' and statType != 'PF':
            raise ValueError("Incorrect input statistic type")

        self.floor = -4
        self.__count = -1
        self.ngramSize = 0
        self.__logFrequencies = {}

        fi = open(ifileName, 'r')

        # Sum frequency
        first = True
        for line in fi:
            datum = line.split(delimiter)
            stat = float(datum[1].strip("\n"))
            ngram = toLatin(datum[0]).upper()

            if first:
                first = False
                self.ngramSize = len(ngram)

            self.__logFrequencies.setdefault(ngram, 0)
            self.__logFrequencies[ngram] += stat
        fi.close()

        # Transform count into frequency
        if statType == 'CF':
            self.__count = sum(self.__logFrequencies.values())
            self.floor = log10(0.01 / self.__count)
            for key in self.__logFrequencies.keys():
                self.__logFrequencies[key] /= self.__count

        # Transform frequency into logFrequency
        for key in self.__logFrequencies.keys():
            self.__logFrequencies[key] = log10(self.__logFrequencies[key])

    def __contains__(self, ngram: str):
        return ngram in self.__logFrequencies

    def frequency(self, ngram: str):
        """
        Return the log frequency of the ngram calculated from
        the frequency in the provided file. The lower the frequency,
        the lower the log frequency.
        :param ngram: The ngram to score.
        :return: The log frequency of the ngram. If the ngram is not present
        in the list, a default value is returned. If the non-recognized ngram
        if of a different size than the first ngram in the provided file,
        then 0 is returned. Else -3 (equivalent to a frequency of 0.1%)
        is returned.
        """
        ngram = ngram.upper()
        return self.__logFrequencies.get(ngram, (len(ngram) != self.ngramSize) * self.floor)

    def score(self, text: str):
        score = 0
        for i in range(len(text) - self.ngramSize + 1):
            ngram = text[i:i+self.ngramSize]
            score += self.frequency(ngram)
        return score

