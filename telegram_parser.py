import os


def preparing_data_files():
    print('\nPreparing /database dir')
    folder = os.path.abspath('./database')
    if not os.path.exists(folder):
        os.mkdir('database')
    os.chdir('./database')
    for i in ['nicknames.txt', 'phonenumbers.txt', 'drop_names.txt']:
        with open(i, 'w') as fout:
            print('', file=fout)
    print('Finish preparation')
    os.chdir('../')


def define_paths():
    exclude_files = {'nicknames.txt', 'phonenumbers.txt', 'drop_names.txt'}
    os.chdir('./database')
    folder = os.path.abspath('./')
    files = list(set(os.listdir(folder)).difference(exclude_files))
    return_files = list()
    for file in files:
        apath = fr'{os.path.normpath(os.path.abspath(file))}'
        if os.path.isfile(apath):
            return_files.append(apath)
    os.chdir('../')
    return return_files


def clear_spaces_between_rows(path):
    with open(path, 'r') as fin:
        data = fin.readlines()
    data = [i for i in data if i != '\n']
    with open(path, 'w') as fout:
        print(''.join(data), file=fout)


def split_to_phones_and_nicknames(path):
    with open(path, 'r') as fin:
        data = fin.readlines()
    nicknames = list()
    phones = list()
    excluded_symbols = '@- \n()+'
    for current in data:
        name = current
        for sym in excluded_symbols:
            name = name.replace(sym, '')
        if name.isdigit():
            try:
                if len(name) <= 10:
                    raise TypeError('Неправильный формат номера')
                phones.append(name[-10:])
            except Exception as err:
                with open('./database/drop_names.txt', 'a') as fout:
                    print(f'{name} - неправильный формат номера телефона', file=fout)
        else:
            nicknames.append(name)
    with open('./database/nicknames.txt', 'a') as fout:
        print('\n'.join(nicknames), file=fout)
    with open('./database/phonenumbers.txt', 'a') as fout:
        print('\n'.join(phones), file=fout)


def clean_after_parse():
    print('\nCleaning extra-enters in phonenumbers.txt and nicknames.txt')
    os.chdir('./database')
    for path in ['nicknames.txt', 'phonenumbers.txt']:
        clear_spaces_between_rows(path)
        with open(path, 'r') as fin:
            data = fin.readlines()
        data = [i.replace('\n', '').replace(' ', '') for i in data if i != '\n']
        data = [item for item in data if item != '']
        with open(path, 'w') as fout:
            print('\n'.join(data), file=fout)
    print('Finish cleaning extra-enters\n')


def delete_all_same(path):
    with open(path, 'r') as fin:
        data = fin.readlines()
    rest = list()
    for item in data:
        if item.replace('\n', '') not in rest and item.replace('\n', '') != '':
            rest.append(item.replace('\n', ''))
    with open(path, 'w') as fout:
        response = [f'{rest[j]}\n' for j in range(len(rest)) if j != len(rest) - 1]
        response.append(str(rest[-1]).replace('\n', ''))
        print(''.join(response), file=fout)


def parse_data():
    preparing_data_files()
    print('\nStart defining the data paths\n')
    need_parse_files = define_paths()
    print(*[f'\t{i})\t{need_parse_files[i - 1]}\t\n' for i in range(1, len(need_parse_files) + 1)])
    if not len(need_parse_files):
        print('No files to parse\nExiting')
        exit(0)
    print('\nStart splitting data to phone and usernames')
    for path in need_parse_files:
        clear_spaces_between_rows(path)
        split_to_phones_and_nicknames(path)
    print('Finished splitting data\n')
    clean_after_parse()
    print('\nDelete all same names in both files')
    for path in ['nicknames.txt', 'phonenumbers.txt']:
        delete_all_same(path)
    print('Finish delete in files')
    os.chdir('../')
    print('Backward from ./database')
