import json
from psycopg2 import Error
from objects import Publisher, Book, Stock, Shop, Sale, session


def load_data_from_file(file: str):
    # task 3
    try:
        with open(file, 'r') as f:
            data = json.load(f)

        for elem in data:
            model = {
                'publisher': Publisher,
                'shop': Shop,
                'book': Book,
                'stock': Stock,
                'sale': Sale,
            }[elem.get('model')]
            session.add(model(id=elem.get('pk'), **elem.get('fields')))
        session.commit()
    except(Exception, Error) as error:
        print('Непредвиденная ошибка.', error)
