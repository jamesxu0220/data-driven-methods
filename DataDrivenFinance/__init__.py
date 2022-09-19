from tkinter.messagebox import RETRY
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['UPLOAD_FOLDER'] = './DataDrivenFinance/______submissions/'

import DataDrivenFinance.index
import DataDrivenFinance.groups
import DataDrivenFinance.submit
import DataDrivenFinance.portfolios
import DataDrivenFinance.performance
import DataDrivenFinance.test

if __name__ == "__main__":
    app.run(debug=True)