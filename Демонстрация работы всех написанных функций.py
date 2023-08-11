from database import Database

#создаём экземпляр класса Database и вызваем метод create_tables, чтобы создать таблицы в базе данных:
db = Database(dbname='mydb', user='postgres', password='richard', host='localhost', port='5432')
db.create_tables()

#добавить нового клиента и его телефон:
client_id = db.add_client('John', 'Doe', 'johndoe@example.com')
db.add_phone(client_id, '+1-555-123-4567')

#добавить несколько телефонов для одного клиента:
client_id = db.add_client('John', 'Doe', 'johndoe@example.com')
db.add_phone(client_id, '+1-555-123-4567')
db.add_phone(client_id, '+1-555-987-6543')

#изменить данные о клиенте:
db.change_client(client_id, first_name='Jane', email='janedoe@example.com')

#удалить телефон:
db.remove_phone(phone_id)

#удалить клиента:
db.remove_client(client_id)

#найти клиента по его данным:
clients = db.find_client(first_name='John')

#комбинацию параметров для поиска клиента:
clients = db.find_client(last_name='Doe', phone_number='+1-555-123-4567')



