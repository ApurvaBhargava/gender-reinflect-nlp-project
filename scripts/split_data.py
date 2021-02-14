import random 
random.seed(42)

def read_data(path):
    with open(path, encoding='utf8', mode='r') as f:
        return f.readlines()

def split(spanish_data, french_data):
    """
    Args:
        spanish_data: list of lines
        french_data: list of lines
    """
    train = {'es': list(),
             'fr': list()}

    dev = {'es': list(),
           'fr': list()}

    test = {'es': list(),
            'fr': list()}

    random.seed(42)
    # zipping the data to shuffle them together
    # all_data = list(zip(spanish_data, french_data))
    random.shuffle(french_data)
    # spanish_data, french_data = zip(*all_data)

    train_len = int(0.8 * len(french_data))
    dev_len = int(0.9 * len(french_data))

    # train_split_es = spanish_data[:train_len]
    # dev_split_es = spanish_data[train_len:dev_len]
    # test_split_es = spanish_data[dev_len:]

    train_split_fr = french_data[:train_len]
    dev_split_fr = french_data[train_len:dev_len]
    test_split_fr = french_data[dev_len:]

    # train['es'] = train_split_es
    # dev['es'] = dev_split_es
    # test['es'] = test_split_es

    train['fr'] = train_split_fr
    dev['fr'] = dev_split_fr
    test['fr'] = test_split_fr

    return train, dev, test

def write_data(path, data):
    with open(path, encoding='utf8', mode='w') as f:
        for line in data:
            f.write(line)

def main():
    # spanish_data = read_data('../data/data.fr')
    french_data = read_data('../data/data.fr')
    train, dev, test  = split(spanish_data=[],
                              french_data=french_data)

    # write_data(path='../data/splits/train.new.es', data=train['es'])
    write_data(path='../data/splits/train.new.fr', data=train['fr'])

    # write_data(path='../data/splits/dev.new.es', data=dev['es'])
    write_data(path='../data/splits/dev.new.fr', data=dev['fr'])

    # write_data(path='../data/splits/test.new.es', data=test['es'])
    write_data(path='../data/splits/test.new.fr', data=test['fr'])

if __name__ == "__main__":
    main()