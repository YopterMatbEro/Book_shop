import json
from psycopg2 import Error
from objects import Publisher, Book, Stock, Shop, Sale, session

if __name__ == '__main__':

    # удаление объектов
    # session.query(Sale).filter(Sale.id > 0).delete()
    # session.query(Stock).filter(Stock.id > 0).delete()
    # session.query(Shop).filter(Shop.id > 0).delete()
    # session.query(Book).filter(Book.id > 0).delete()
    # session.query(Publisher).filter(Publisher.id > 0).delete()
    # session.commit()  # фиксируем изменения

    # task 2
    id_publisher = 'Неизвестный id'
    publisher = input('Введите имя или id издателя: ')
    if publisher.isdigit():
        id_publisher = int(publisher)
    else:
        for elem in session.query(Publisher).filter(Publisher.name.ilike(f'%{publisher}%')).all():
            id_publisher = elem.id

    q = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).\
    join(Publisher, Publisher.id == Book.id_publisher).\
    join(Stock, Stock.id_book == Book.id).\
    join(Shop, Shop.id == Stock.id_shop).\
    join(Sale, Sale.id_stock == Stock.id).\
    filter(Publisher.id == id_publisher)

    for s in q.all():
        print(*s, sep=' | ')

    # task 3
    # try:
    #     with open('tests_data.json', 'r') as f:
    #         data = json.load(f)
    #
    #     for elem in data:
    #         model = {
    #             'publisher': Publisher,
    #             'shop': Shop,
    #             'book': Book,
    #             'stock': Stock,
    #             'sale': Sale,
    #         }[elem.get('model')]
    #         session.add(model(id=elem.get('pk'), **elem.get('fields')))
    #     session.commit()
    # except(Exception, Error) as error:
    #     print('Непредвиденная ошибка.', error)
