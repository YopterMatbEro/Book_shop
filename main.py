import json
from psycopg2 import Error
from objects import Publisher, Book, Stock, Shop, Sale, session

if __name__ == '__main__':

    # task 2
    # publisher = 'Пушкин'  # других в бд не занесено
    #
    # q = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).\
    # join(Publisher, Publisher.id == Book.id_publisher).\
    # join(Stock, Stock.id_book == Book.id).\
    # join(Shop, Shop.id == Stock.id_shop).\
    # join(Sale, Sale.id_stock == Stock.id).\
    # filter(Publisher.name == publisher)

    # for s in q.all():
    #     print(*s, sep=', ')

    # task 3
    try:
        with open('tests_data.json', 'r') as f:
            data = json.load(f)
            print(data)
            for elem in data:
                for key, value in elem.items():
                    if value == 'model':
                        table_name = value
                    elif key == 'pk':
                        pk = value
                    elif key == 'fields':
                        values = value
                    else:
                        print('Ошибка')
                input_data = pass
    except(Exception, Error) as error:
        print('Непредвиденная ошибка.', error)