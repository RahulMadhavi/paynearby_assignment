# paynearby_assignment

Python version 3.6.8

 1. install requirements.txt

 2. run server using: python manage.py run

 3. database used: postgres. port: 5433. password: root, database name: assignment, schema: paynearby

 4. Run following SQL query in paynearby schema:

CREATE TABLE paynearby.daily_transactions ( rrn_no numeric primary key, txn_date date NOT NULL, mask_card_number varchar NULL, account_no numeric NULL, bank_name varchar NULL, account_holder_name varchar NULL, transaction_type varchar NULL, amount numeric NULL, date_key int4 NULL );

CREATE INDEX daily_transactions_date_key_idx ON paynearby.daily_transactions (date_key);

CREATE INDEX daily_transactions_bank_name_idx ON paynearby.daily_transactions (bank_name);

CREATE INDEX daily_transactions_transaction_type_idx ON paynearby.daily_transactions (transaction_type);

CREATE INDEX daily_transactions_account_holder_name_idx ON paynearby.daily_transactions (account_holder_name);

5. Specify path of CSV in config.py:

self.FILE_PATH = your csv file path
