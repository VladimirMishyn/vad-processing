from nltk.stem.snowball import SnowballStemmer
import csv

stem_it = SnowballStemmer("russian")
no_translation = 'NO TRANSLATION'

result_dict = {}


def format_it(stemmed, array_line):
    if stemmed not in result_dict:
        result_object = {
            'original': array_line[0].strip(),
            'translated': array_line[1].strip(),
            'valence': array_line[2].strip(),
            'arousal': array_line[3].strip(),
            'dominance': array_line[4].strip()
        }
        result_dict[stemmed.strip()] = result_object


def read_it(file_name):
    with open(file_name, 'r', newline='', encoding="UTF8") as source:
        next(source)
        for line in source:
            line_wo_spaces = " ".join(line.split())
            array_from_string = line_wo_spaces.split(',')
            with_strip = []
            for element in array_from_string:
                if element:
                    with_strip.append(element.strip())
            if len(with_strip) == 5:
                translated = with_strip[1]
                if translated != no_translation:
                    format_it(stem_it.stem(with_strip[1]), with_strip)
                # print(array_from_string)
                # print(stem_it.stem(array_from_string[1]))
            # array.append()
            # print(line)
    source.close()


def pre_csv_format(dictionary):
    old_dict = dictionary.copy()
    array_to_write = [['STEM', 'ORIGINAL', 'TRANSLATED', 'VALENCE', 'AROUSAL', 'DOMINANCE']]
    for key, value in old_dict.items():
        append_it = [key, value['original'], value['translated'], value['valence'], value['arousal'],
                     value['dominance']]
        array_to_write.append(append_it)
    return array_to_write


def write_to_csv(name, write_it):
    result_name = name + '.csv'
    with open(result_name, 'w', newline='', encoding="UTF8") as csvFile:
        writer = csv.writer(csvFile)
        for row in write_it:
            writer.writerow(row)
    csvFile.close()


read_it('VAD.csv')
# print(result_dict)
formatted = pre_csv_format(result_dict)
write_to_csv('formatted', formatted)
