from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from solcx import compile_source, compile_files, link_code
from web3 import Web3
from web3.contract import ConciseContract


app = Flask(__name__)

sellers = ['Company 1', 'Company 2']



@app.route("/", methods=['GET', 'POST'])
def index():

    return render_template('index.html', sellers=sellers)


@app.route("/about")
def about():
  return render_template("about.html")



if __name__ == "__main__":
  app.run(debug=True)
  