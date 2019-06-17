import csv

base_name = 'tomos-ukraine'

bound_name = './results/' + base_name + '-VAD-result'
source_file = './raw-data/' + base_name + '-result.csv'
data_file = './source/formatted.csv'

arousal_fringe = 0.4
dominance_fringe = 0.6
use_fringes = False


def create_lib(data_raw):
    result_dict = {}
    for line in data_raw:
        result_object = {
            'v': line[3],
            'a': line[4],
            'd': line[5]
        }
        result_dict[line[0]] = result_object
    return result_dict


def bind_together(source_raw, data_raw):
    lib = create_lib(data_raw)
    result = []
    for pair in source_raw:
        tokens = pair[1].split(',')
        count = 0
        v = 0
        a = 0
        d = 0
        word_in_lib = []
        for token in tokens:
            if token in lib:
                check = True if not use_fringes else (float(lib[token]['a']) > arousal_fringe and float(lib[token]['d']) < dominance_fringe)
                if check:
                    # print(lib[token])
                    count = count + 1
                    v = v + float(lib[token]['v'])
                    a = a + float(lib[token]['a'])
                    d = d + float(lib[token]['d'])
                    append_it = token + ' (' + lib[token]['v'] + ';' + lib[token]['a'] + ';' + lib[token]['d'] + ') '
                    # if lib[token]['a'] > lib[token]['d']:
                    #     print(token)
                    word_in_lib.append(append_it)
        if count > 0:
            result_v = round(v / count, 3)
            result_a = round(a / count, 3)
            result_d = round(d / count, 3)
            result.append([pair[0], pair[1], ','.join([str(x) for x in word_in_lib]), result_v, result_a, result_d])
    return result


def persist_to_csv(name, data_to_persist):
    result_name = name + '-result.csv'
    with open(result_name, 'w', newline='', encoding="UTF8") as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(['TITLE', 'TOKENS', 'TOKENS-VAD', 'V-MED', 'A-MED', 'D-MED'])
        for row in data_to_persist:
            writer.writerow(row)
    csvFile.close()


def extract_from_csv(name):
    result_array = []
    with open(name, 'r', newline='', encoding="UTF8") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            result_array.append(row)
    return result_array


source = extract_from_csv(source_file)
data = extract_from_csv(data_file)
bound = bind_together(source, data)
persist_to_csv(bound_name, bound)
