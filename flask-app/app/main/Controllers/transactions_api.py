import os

from flask import Blueprint, current_app, request
from pandas import DataFrame, pivot_table
from sqlalchemy import text


from app.main.utils.validator import check_valid_csv
from app.main.utils.update_records import insert_records

transactions_api = Blueprint('transactions_api', __name__)


@transactions_api.route('/post_data', methods=['POST'])
def upload_csv_file_records():
    response = {
        'data': None,
        'errors': None,
        'requested_filters': None
    }
    request_args = request.args
    uploaded_file = request.files.get('file')
    
    try:
        if check_valid_csv(uploaded_file.filename):
            file_path = os.path.join(current_app.config['FILE_PATH'], uploaded_file.filename)
            uploaded_file.save(file_path)
            insert_records(file_path)
            response['data'] = f'{uploaded_file.filename} file records are stored successfully'
        else:
            response['errors'] = 'Upload valid csv'
    except Exception as e:
        response['errors'] = e
    finally:
        return response


@transactions_api.route('/records', methods=['GET'])
def view_records():
    response = {
        'data': None,
        'errors': None,
        'requested_filters': None
    }

    request_args = request.args
    try:
        with current_app.config.get('TEMP_SESSION').create_scope() as session:
            test_query = """
            select 
                count(1) as "Total Rows"
            from 
            paynearby.daily_transactions
            """
            result_data = [dict(x) for x in session.execute(text(test_query)).fetchall()]
        response['data'] = result_data
    except Exception as e:
        response['errors'] = e
    finally:
        return response


@transactions_api.route('/banks', methods=['GET'])
def unique_banks():
    response = {
        'data': None,
        'errors': None,
        'requested_filters': None
    }

    request_args = request.args
    try:
        with current_app.config.get('TEMP_SESSION').create_scope() as session:
            test_query = """
            select 
                distinct bank_name as "Bank Name"
            from
                paynearby.daily_transactions
            """
            result_data = [dict(x) for x in session.execute(text(test_query)).fetchall()]
        response['data'] = result_data
    except Exception as e:
        response['errors'] = e
    finally:
        return response


@transactions_api.route('/customer_names', methods=['GET'])
def unique_customer_names():
    response = {
        'data': None,
        'errors': None,
        'requested_filters': None
    }

    request_args = request.args
    try:
        with current_app.config.get('TEMP_SESSION').create_scope() as session:
            test_query = """
            select 
            distinct 
              account_holder_name  as "Customer Names"
            from
            paynearby.daily_transactions
            """
        result_data = [dict(x) for x in session.execute(text(test_query)).fetchall()]
        response['data'] = result_data
    except Exception as e:
        response['errors'] = e
    finally:
        return response


@transactions_api.route('/transaction_summary', methods=['GET'])
def transaction_type_count_summary():
    response = {
        'data': None,
        'errors': None,
        'requested_filters': None
    }

    request_args = request.args
    try:
        with current_app.config.get('TEMP_SESSION').create_scope() as session:
            test_query = """
            select 
              transaction_type as "Transaction Type", 
              count(1) as "Number of Transactions"
            from
            paynearby.daily_transactions
            group by 1
            """
            _cursor = session.execute(text(test_query))
            columns = _cursor._metadata.keys

            if _cursor.rowcount > 0:
                result_data = DataFrame(_cursor.fetchall())
                result_data.columns = columns
            else:
                result_data = DataFrame(columns=columns)

            # result_data['Transactions Amount'] = result_data['Transactions Amount'].astype(float).round(2)

            result_data = pivot_table(
                result_data,
                columns=['Transaction Type'],
                values=['Number of Transactions']
            )
            result_data = result_data.to_dict('records')
        # result_data = [dict(x) for x in session.execute(text(test_query)).fetchall()]
        response['data'] = result_data
    except Exception as e:
        response['errors'] = e
    finally:
        return response


@transactions_api.route('/transaction_amount_summary', methods=['GET'])
def transaction_type_amount_summary():
    response = {
        'data': None,
        'errors': None,
        'requested_filters': None
    }

    request_args = request.args
    try:
        with current_app.config.get('TEMP_SESSION').create_scope() as session:
            test_query = """
            select 
              transaction_type as "transaction_type", 
              round(sum(amount),2)::text as "Transactions Amount"
            from
            paynearby.daily_transactions
            group by 1
            """
            _cursor = session.execute(text(test_query))
            columns = _cursor._metadata.keys

            if _cursor.rowcount > 0:
                result_data = DataFrame(_cursor.fetchall())
                result_data.columns = columns
            else:
                result_data = DataFrame(columns=columns)

            result_data['Transactions Amount'] = result_data['Transactions Amount'].astype(float).round(2)

            result_data = pivot_table(
                result_data,
                columns=['transaction_type'],
                values=['Transactions Amount']
            )
            result_data = result_data.to_dict('records')
            # result_data = [dict(x) for x in session.execute(text(test_query)).fetchall()]

        response['data'] = result_data
    except Exception as e:
        response['errors'] = e
    finally:
        return response


@transactions_api.route('/total_transaction_amount', methods=['GET'])
def transaction_amount_summary():
    response = {
        'data': None,
        'errors': None,
        'requested_filters': None
    }

    request_args = request.args
    try:
        with current_app.config.get('TEMP_SESSION').create_scope() as session:
            test_query = """
            select 
              round(sum(amount),2)::text as "Total Transactions Amount"
            from
            paynearby.daily_transactions
            """
            result_data = [dict(x) for x in session.execute(text(test_query)).fetchall()]
        response['data'] = result_data
    except Exception as e:
        response['errors'] = e
    finally:
        return response


@transactions_api.route('/<from_date>/<to_date>', methods=['GET'])
def transaction_details(from_date, to_date):
    response = {
        'data': None,
        'errors': None,
        'requested_filters': None
    }

    request_args = request.args
    from_date = int(from_date.replace('-',''))
    to_date = int(to_date.replace('-',''))
    try:
        with current_app.config.get('TEMP_SESSION').create_scope() as session:
            test_query = f"""
            select 
              count(1) as "No of Transactions" 
            from
            paynearby.daily_transactions
            where date_key between {from_date} and {to_date}
            """
            result_data = [dict(x) for x in session.execute(text(test_query)).fetchall()]
        response['data'] = result_data
    except Exception as e:
        response['errors'] = e
    finally:
        return response
