class RequirementsException(BaseException):
    def __init__(self, m: str):
        self.message = m

    def __str__(self):
        return self.message


class UserRequirements:
    def add_input(self, inp):
        self.inputs.append(inp)

    def __init__(self, time, norm, path_name):
        self.time = time
        self.path_name = path_name
        self.normalization = norm
        self.inputs = []

    def __str__(self):
        return "time: " + str(self.time) + ", normalization: " + str(
            self.normalization) + ", path: " + self.path_name + ".mid, inputs: " + str(self.inputs)


# name -> alpha-3
def name_code3(country_name):
    import json

    # from 'countries_pl-eng': formal English name ->  alpha-2
    def en_formal1_code2():
        with open('jsons_data/countries_pl-eng.json', 'r', encoding="utf8") as f:
            c = json.loads(f.read())
            return {country_data['name_en']: country_data['code'] for country_data in c}

    # from 'countries_pl-eng': Polish name ->  alpha-2
    def pl_code2():
        with open('jsons_data/countries_pl-eng.json', 'r', encoding="utf8") as f:
            c = json.loads(f.read())
            return {country_data['name_pl']: country_data['code'] for country_data in c}

    # from 'country_code.json': alpha-2 -> alpha-3
    def code2_code3():
        with open('jsons_data/country_code.json', 'r', encoding="utf8") as f:
            c = json.loads(f.read())
            return {country_data['alpha-2']: country_data['alpha-3'] for country_data in c}

    # from 'country_code.json': formal English name -> alpha-3
    def en_formal2_code3():
        with open('jsons_data/country_code.json', 'r', encoding="utf8") as f:
            c = json.loads(f.read())
            return {county_data['name']: county_data['alpha-3'] for county_data in c}

    # from 'countries_coordinates.json': informal English name -> alpha-3
    def en_informal_code3():
        with open('jsons_data/countries_coordinates.json', 'r', encoding="utf8") as f:
            c = json.loads(f.read())
            return {country_data['properties']['name']: country_data['id']
                    for country_data in c['features']}

    dict_name_code3 = dict()
    dict_name_code3.update(en_informal_code3())
    dict_name_code3.update(en_formal2_code3())
    dict_name_code3.update(en_formal2_code3())
    dict_name_code3.update({"Kosowo": "CS-KM", "Cypr Północny": "NOR-CYP", "Republika Somalilandu": "SOM_LAND"})

    c2_c3 = code2_code3()
    dict_name_code2 = dict()
    dict_name_code2.update(en_formal1_code2())
    dict_name_code2.update(pl_code2())
    for name, code2 in dict_name_code2.items():
        code3 = c2_c3.get(code2)
        if code3 is not None:
            dict_name_code3[name] = code3

    code3 = dict_name_code3.get(country_name)
    if code3 is None:
        raise RequirementsException("Nie znana nazwa kraju: " + country_name)
    else:
        return code3


def input_file_parse(file):
    lines = file.read().splitlines()
    code3 = name_code3(lines[0])
    if code3 is not None:
        transformations = list()
        for line in lines[1:]:
            table = line.split(' ')
            if table[0] == 'scaling:' and len(table) == 3:
                transformations.append(('scl', float(table[1]), float(table[2])))

            if table[0] == 'translation:' and len(table) == 3:
                transformations.append(('tsl', float(table[1]), float(table[2])))

            if table[0] == 'reflection:' and len(table) == 3:
                transformations.append(('ref', float(table[1]), float(table[2])))

            if table[0] == 'rotation:' and len(table) == 2:
                transformations.append(('rot', float(table[1])))

        return code3, transformations


def parse():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('name', help="nazwa pliku wynikowego")
    parser.add_argument('-t', '--time', type=int, help="czas trwania w sekundach")
    parser.add_argument('-n', '--normalization', type=int, nargs=2, metavar=('LOWER_NOTE', 'HIGHER_NOTE'),
                        help="ostateczne rozciągnięcie w nutach")
    parser.add_argument('-o', '--output', help="ścieżka do miejsca w którym ma zapisać plik")
    parser.add_argument('-i', '--input', type=argparse.FileType(mode='r', encoding="utf8"), required=True,
                        action='append', help="plik z wymaganiami dotyczącymi kraju")

    args = parser.parse_args()

    if args.output is not None:
        path_name = args.output + "/"
    else:
        path_name = "output/"
    path_name += args.name

    requirements = UserRequirements(args.time, args.normalization, path_name)

    for file in args.input:
        setting = input_file_parse(file)
        requirements.add_input(setting)
        file.close()

    return requirements
