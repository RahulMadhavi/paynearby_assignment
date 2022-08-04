import os

from pandas import read_csv, DataFrame
from flask import current_app


def insert_records(csv_file_path):
    csv_data = read_csv(csv_file_path)
    with current_app.config.get('TEMP_SESSION').create_scope() as session:
        for i, row in csv_data.iterrows():
            data = row['NARRATION'].split(r'/')
            # date = row['TXN DATE']
            date_key = row['TXN DATE'].replace('-', '')
            # Amount = int(row['AMOUNT'])

            insert_query = """
            --CREATE table if not exists paynearby.daily_transactions_{date_key} PARTITION OF paynearby.daily_transactions FOR VALUES IN ({date_key});
            insert into 
            paynearby.daily_transactions
            (rrn_no,txn_date,mask_card_number,account_no,bank_name,account_holder_name,transaction_type,amount,date_key) 
            values
            ({rrn_no},'{txn_date}', '{mask_card_number}',{account_no}, '{bank_name}', '{account_holder_name}', '{transaction_type}', {amount}, {date_key})
            on conflict do nothing; 
            """.format(rrn_no=int(data[2].split(':')[1]),
                    txn_date=row['TXN DATE'],
                    mask_card_number=data[1],
                    account_no=data[3],
                    bank_name=data[4],
                    account_holder_name=data[5].title(),
                    transaction_type=data[6],
                    amount=int(row['AMOUNT']),
                    date_key=date_key,
                    )
            session.execute(insert_query)
    os.remove(csv_file_path)
            
        
        
    