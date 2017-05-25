# coding: utf-8

import fitz
from flask import Flask, request, jsonify
from InvalidUsageException import InvalidUsageException
from werkzeug.utils import secure_filename
from standard_bank_reader import StandardBankStatementReader

ALLOWED_EXTENSIONS = ['pdf']

app = Flask(__name__)

sbReader = StandardBankStatementReader()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.errorhandler(InvalidUsageException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/GetBankStatementSummary', methods=['POST'])
def bank_statement_summary():
    if 'file' not in request.files:
        raise InvalidUsageException('No file in request')
    file = request.files['file']
    if file.filename == '':
        raise InvalidUsageException('No file in request')
    if not allowed_file(file.filename):
        raise InvalidUsageException('Invalid file extension. Allowed extensions are: ', ALLOWED_EXTENSIONS.join(','))
    return jsonify(get_bank_statement_details(file))

def get_bank_statement_details(bank_pdf_file):
    pdf_contents = bank_pdf_file.read()
    pdf_name = bank_pdf_file.filename
    bank_pdf_file.close()

    return sbReader.get_account_summary(pdf_name, pdf_contents)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False)
