from flask import Flask, redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['UPLOAD_FOLDER'] = './DataDrivenFinance/______submissions/'

import DataDrivenFinance.index
import DataDrivenFinance.groups
import DataDrivenFinance.submit
import DataDrivenFinance.portfolios
import DataDrivenFinance.performance
import DataDrivenFinance.debug_setup
import DataDrivenFinance.debug_cleanup

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/')
def home():
    return redirect('/index')