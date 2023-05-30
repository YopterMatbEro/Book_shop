from database import load_data_from_file
from utils import delete_objects
from objects import Publisher, Book, Stock, Shop, Sale, session, InputHandler


def main():
    input_handler = InputHandler()
    publisher_id = input_handler.get_publisher_id()

    q = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale). \
        join(Publisher, Publisher.id == Book.id_publisher). \
        join(Stock, Stock.id_book == Book.id). \
        join(Shop, Shop.id == Stock.id_shop). \
        join(Sale, Sale.id_stock == Stock.id). \
        filter(Publisher.id == publisher_id)

    if q.all():
        print('Акты продаж:')
        for s in q:
            print(*s, sep=' | ')
    else:
        print('Нет совпадений в базе данных.')


if __name__ == '__main__':
    # delete_objects()
    # load_data_from_file()
    main()

