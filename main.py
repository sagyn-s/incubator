import pandas as pd


def createBigram():
    f = open('names.txt', 'r')
    listOfBigrams = []
    bigramCounts = {}
    unigramCounts = {}
    for s in f.readlines():
        elem = '^' + s[:-1] + '$' + '\n'
        for i in range(len(elem) - 2):
            listOfBigrams.append((elem[i], elem[i + 1]))
        for i in range(len(elem) - 1):
            if elem[i] in unigramCounts:
                unigramCounts[elem[i]] += 1
            else:
                unigramCounts[elem[i]] = 1
    for elem in listOfBigrams:
        if elem in bigramCounts:
            bigramCounts[elem] += 1
        else:
            bigramCounts[elem] = 1
    return listOfBigrams, unigramCounts, bigramCounts


def calcBigramProb(listOfBigrams, unigramCounts, bigramCounts):
    listOfProb = {}
    for bigram in listOfBigrams:
        word1 = bigram[0]
        listOfProb[bigram] = bigramCounts.get(bigram) / unigramCounts.get(word1)
    return listOfProb


def vyborka(bigramProb):
    probs = []
    bigrams = []
    for elem in bigramProb:
        probs.append(bigramProb[elem])
        bigrams.append(elem)
    data = {
        'Bigram': bigrams,
        'Probability': probs}
    return data


def generate(df):
    bigram = tuple(df.sample()['Bigram'])[0]
    letter = bigram[0]
    second_letter = bigram[1]
    while letter != '^':
        bigram = tuple(df.sample()['Bigram'])[0]
        letter = bigram[0]
        second_letter = bigram[1]
    name = second_letter
    while second_letter != '$':
        bigram = tuple(df.sample()['Bigram'])[0]
        while bigram[0] != second_letter:
            bigram = tuple(df.sample()['Bigram'])[0]
        name += bigram[1]
        second_letter = bigram[1]
    name = name[:-1]
    return name


if __name__ == '__main__':
    listOfBigrams, unigramCounts, bigramCounts = createBigram()
    bigramProb = calcBigramProb(listOfBigrams, unigramCounts, bigramCounts)
    df = pd.DataFrame(vyborka(bigramProb))
    with open('dataframe.html', 'w') as outfile:
        outfile.write(df.to_html())
    name = generate(df)
    print(name)
