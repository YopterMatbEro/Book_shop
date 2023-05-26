import configparser
import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

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
    price = sq.Column(sq.Integer, nullable=False)
    date_sale = sq.Column(sq.Date(), nullable=False)
    __table_args__ = (sq.CheckConstraint('date_sale <= CURRENT_DATE'),)
    id_stock = sq.Column(sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer, default=1)

    stock = relationship(Stock, backref='sales')


def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


config = configparser.ConfigParser()
config.read('config.ini')
db = config['psql']['db']
user = config['psql']['user']
password = config['psql']['password']

DSN = ('postgresql://%s:%s@localhost:5432/%s', (user, password, db))
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()
