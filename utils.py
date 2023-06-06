from objects import Publisher, Book, Stock, Shop, Sale


def delete_objects(session):
    session.query(Sale).filter(Sale.id > 0).delete()
    session.query(Stock).filter(Stock.id > 0).delete()
    session.query(Shop).filter(Shop.id > 0).delete()
    session.query(Book).filter(Book.id > 0).delete()
    session.query(Publisher).filter(Publisher.id > 0).delete()
    session.commit()
