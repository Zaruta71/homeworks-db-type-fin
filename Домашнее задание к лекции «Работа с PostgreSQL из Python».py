import psycopg2

class Database:
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

    def create_tables(self):
        with self.conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS clients (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(50),
                    last_name VARCHAR(50),
                    email VARCHAR(100)
                );
            ''')

            cur.execute('''
                CREATE TABLE IF NOT EXISTS phones (
                    id SERIAL PRIMARY KEY,
                    client_id INTEGER REFERENCES clients(id),
                    phone_number VARCHAR(20)
                );
            ''')

        self.conn.commit()

    def add_client(self, first_name, last_name, email):
        with self.conn.cursor() as cur:
            cur.execute('INSERT INTO clients (first_name, last_name, email) VALUES (%s, %s, %s) RETURNING id', (first_name, last_name, email))
            client_id = cur.fetchone()[0]

        self.conn.commit()

        return client_id

    def add_phone(self, client_id, phone_number):
        with self.conn.cursor() as cur:
            cur.execute('INSERT INTO phones (client_id, phone_number) VALUES (%s, %s)', (client_id, phone_number))

        self.conn.commit()

    def change_client(self, client_id, first_name=None, last_name=None, email=None):
        with self.conn.cursor() as cur:
            if first_name is not None:
                cur.execute('UPDATE clients SET first_name = %s WHERE id = %s', (first_name, client_id))
            if last_name is not None:
                cur.execute('UPDATE clients SET last_name = %s WHERE id = %s', (last_name, client_id))
            if email is not None:
                cur.execute('UPDATE clients SET email = %s WHERE id = %s', (email, client_id))

        self.conn.commit()

    def remove_phone(self, phone_id):
        with self.conn.cursor() as cur:
            cur.execute('DELETE FROM phones WHERE id = %s', (phone_id,))

        self.conn.commit()

    def remove_client(self, client_id):
        with self.conn.cursor() as cur:
            cur.execute('DELETE FROM clients WHERE id = %s', (client_id,))
            cur.execute('DELETE FROM phones WHERE client_id = %s', (client_id,))

        self.conn.commit()

    def find_client(self, first_name=None, last_name=None, email=None, phone_number=None):
        with self.conn.cursor() as cur:
            query = 'SELECT * FROM clients WHERE '
            params = []

            if first_name is not None:
                query += 'first_name = %s AND '
                params.append(first_name)
            if last_name is not None:
                query += 'last_name = %s AND '
                params.append(last_name)
            if email is not None:
                query += 'email = %s AND '
                params.append(email)

            query = query[:-5]

            cur.execute(query, tuple(params))
            clients = cur.fetchall()

            if phone_number is not None:
                filtered_clients = []

                for client in clients:
                    cur.execute('SELECT * FROM phones WHERE client_id = %s AND phone_number = %s', (client[0], phone_number))
                    phone = cur.fetchone()

                    if phone is not None:
                        filtered_clients.append(client)

                return filtered_clients

            return clients
