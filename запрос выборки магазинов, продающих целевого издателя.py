from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Publisher, Book, Shop, Stock, Sale

# Создадим движок и сессию
engine = create_engine('postgresql://username:password@localhost/database')
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
