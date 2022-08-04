"""
--current structure
CREATE TABLE paynearby.daily_transactions (
	rrn_no numeric primary key,
	txn_date date NOT NULL,
	mask_card_number varchar NULL,
	account_no numeric NULL,
	bank_name varchar NULL,
	account_holder_name varchar NULL,
	transaction_type varchar NULL,
	amount numeric NULL,
	date_key int4 NULL
);
CREATE INDEX daily_transactions_date_key_idx ON paynearby.daily_transactions (date_key);
CREATE INDEX daily_transactions_bank_name_idx ON paynearby.daily_transactions (bank_name);
CREATE INDEX daily_transactions_transaction_type_idx ON paynearby.daily_transactions (transaction_type);
CREATE INDEX daily_transactions_account_holder_name_idx ON paynearby.daily_transactions (account_holder_name);
"""



"""
---for more transactions
CREATE TABLE paynearby.daily_transactions (
	rrn_no numeric not null,
	txn_date date NOT NULL,
	mask_card_number varchar NULL,
	account_no numeric NULL,
	bank_name varchar NULL,
	account_holder_name varchar NULL,
	transaction_type varchar NULL,
	amount numeric NULL,
	date_key int4 NULL
)
PARTITION BY LIST (date_key);
CREATE INDEX daily_transactions_date_key_idx ON paynearby.daily_transactions (date_key);


CREATE TABLE paynearby.daily_transactions_20200101 PARTITION OF paynearby.daily_transactions (
	CONSTRAINT rdaily_transactions_20200101_pk PRIMARY KEY (rrn_no)
)FOR VALUES IN (20200101);
"""