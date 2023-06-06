import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=60), unique=True)


class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.Text, nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    publisher = relationship(Publisher, backref='books')


class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)


class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer, default=0)

    book = relationship(Book, backref='stock_book')
    shop = relationship(Shop, backref='stock_shop')


class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.DateTime(), nullable=False)
    __table_args__ = (sq.CheckConstraint('date_sale <= CURRENT_DATE'),)
    id_stock = sq.Column(sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer, default=1)

    stock = relationship(Stock, backref='sales')


class InputHandler():
    def __init__(self):
        self.publisher_id = None

    def get_publisher_id(self, session):
        while True:
            publisher = input('Введите имя или id издателя: ')
            if publisher.isdigit():
                self.publisher_id = int(publisher)
                break
            else:
                query = session.query(Publisher).filter(Publisher.name.ilike(f'%{publisher}%'))
                if query.count() == 0:
                    print(f'Издатель {publisher} не найден в базе данных')
                elif query.count() == 1:
                    self.publisher_id = query.first().id
                    break
                else:
                    print(f'Найдено несколько издателей с именем {publisher}. Выберите нужный id из списка:')
                    publisher_list_id = []
                    for elem in query.all():
                        publisher_list_id.append(elem.id)
                        print(f'{elem.id}: {elem.name}')
                    while self.publisher_id not in publisher_list_id:
                        self.publisher_id = input('Введите id издателя: ')
                        if self.publisher_id == 'exit':
                            print('Вы закрыли сессию. Всего доброго!')
                            return
                        elif not self.publisher_id.isdigit() or int(self.publisher_id) not in publisher_list_id:
                            print('Некорректный id издателя')
                        elif int(self.publisher_id) in publisher_list_id:
                            return int(self.publisher_id)
        return int(self.publisher_id)