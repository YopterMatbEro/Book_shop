import configparser
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from database import load_data_from_file
from utils import delete_objects
from objects import Publisher, Book, Stock, Shop, Sale, InputHandler, Base


def select_sales(session):
    input_handler = InputHandler()
    publisher_id = input_handler.get_publisher_id(session)

    q = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale). \
        join(Publisher, Publisher.id == Book.id_publisher). \
        join(Stock, Stock.id_book == Book.id). \
        join(Shop, Shop.id == Stock.id_shop). \
        join(Sale, Sale.id_stock == Stock.id). \
        filter(Publisher.id == publisher_id)

    if q.all():
        print('Акты продаж:')
        for book, shop, price, date in q:
            print(f'{book:<40} | {shop:<10} | {price:<8} | {date.strftime("%d-%m-%Y")}')
    else:
        print('Нет совпадений в базе данных.')


def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    db = config['psql']['db']
    user = config['psql']['user']
    password = config['psql']['password']

    DSN = f'postgresql://{user}:{password}@localhost:5432/{db}'
    engine = sqlalchemy.create_engine(DSN)
    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # delete_objects(session)
    # load_data_from_file(session)
    select_sales(session)


if __name__ == '__main__':
    main()

