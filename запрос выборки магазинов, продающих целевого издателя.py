from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Publisher, Book, Shop, Stock, Sale

# Создадим движок и сессию
engine = create_engine('postgresql://postgres:richard@localhost:5432/database')
Session = sessionmaker(bind=engine)
session = Session()

# Получаем ввод для имени или идентификатора издателя
publisher_input = input("Enter the name or id of the publisher: ")

# Запрашиваем базу данных
publisher = session.query(Publisher).filter(Publisher.name == publisher_input).first()
if publisher:
    books = session.query(Book).filter(Book.id_publisher == publisher.id).all()
    for book in books:
        stocks = session.query(Stock).filter(Stock.id_book == book.id).all()
        for stock in stocks:
            sale = session.query(Sale).filter(Sale.id_stock == stock.id).first()
            if sale:
                shop = session.query(Shop).filter(Shop.id == stock.id_shop).first()
                print(f"{book.title} | {shop.name} | {sale.price} | {sale.date_sale}")
else:
    print("Publisher not found.")

# Закрываем сессию
session.close()

"""
Здравствуйте, Александр!

Хорошая работа, зачёт!

Есть некоторые моменты, которые можно улучшить:

желательно выносить каждый проект в отдельный репозиторий/папку

соблюдайте правила именования модулей


postgresql://postgres:richard@localhost:5432/database параметры подключения к БД лучше разбить на отдельные переменные

запрос выборки должен разрешать выборку не только по имени, но и по id издателя. Вы можете реализовать его таким образом:
"""
#def get_sales(author_id = 0, author_name = ''):
#     res = session.query(Book.title, Shop.name, Sale.price, Sale.count, Sale.date_sale).\
#           join(Publisher).join(Stock).join(Sale).join(Shop).\
#           filter(or_(Publisher.id==author_id, Publisher.name.ilike(f'%{publisher_name}%')))
#
#     for book, shop, price, count, date in res:
#         print(f'{book: <40} | {shop: <10} | {price*count: <8} | {date.strftime('%d-%m-%Y')}')
#
#
# ...
# if __name__ == '__main__':
#     ...
#     q = input('Введите id или название издателя: ')
#     if q.isdigit():
#         get_sales(author_id=int(q))
#     else:
#         get_sales(author_name=q)
