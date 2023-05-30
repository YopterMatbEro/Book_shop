from database import load_data_from_file
from utils import delete_objects
from objects import Publisher, Book, Stock, Shop, Sale, session


class InputHandler:
    def __init__(self):
        self.publisher_id = None

    def get_publisher_id(self):
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
        print('Нет совпадений.')


if __name__ == '__main__':
    # delete_objects()
    # load_data_from_file('tests_data.json')  # наполнение БД из указанного json-файла
    main()

