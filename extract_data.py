from nltk.stem.snowball import SnowballStemmer
import csv
import re
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation

file_name = './raw-data/tomos-ukraine'
# Create lemmatizer and stopwords list
mystem = Mystem()
russian_stopwords = stopwords.words("russian")

stem_it = SnowballStemmer("russian")


def extract_from_csv(name):
    result_array = []
    with open(name, 'r', newline='', encoding="UTF8") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            result_array.append(row[0])
    return result_array


def basic_process(text):
    return " ".join(re.findall("[a-zA-Zа-яА-Я]+", text))


def process_text(text):
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords \
              and token != " " \
              and token.strip() not in punctuation]

    text = " ".join(tokens)
    return text


def process_array(array):
    tmp_array = []
    size = len(array)
    step = round(float(100 / size), 2)
    for index, string in enumerate(array):
        processed_text = basic_process(string)
        tmp_array.append([string, process_text(processed_text)])
        print('Done:' + str(int(index * step)))

    result_array = []
    for pair in tmp_array:
        inner = []
        as_array = pair[1].split(' ')
        for el in as_array:
            inner.append(stem_it.stem(el))
        result_array.append([pair[0], ','.join([str(x) for x in inner])])
    return result_array


def persist_to_csv(name, pairs):
    result_name = name + '-result.csv'
    with open(result_name, 'w', newline='', encoding="UTF8") as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(['NAME', 'TOKENS'])
        for row in pairs:
            writer.writerow(row)
    csvFile.close()


extracted = extract_from_csv(file_name + '.csv')
processed_array = process_array(extracted)
persist_to_csv(file_name, processed_array)
# print(processed_array)
