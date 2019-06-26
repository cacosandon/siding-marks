# -*- coding: latin-1 -*-

from flask import Flask, render_template, request, session, render_template_string
from qualifications import get_qual
from methods import logout


app = Flask(__name__)

@app.route('/')
def home():
   logout()
   return render_template('student.html')

@app.route('/result', methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form.to_dict()
      creds = f"login={result['login']}&passwd={result['passwd']}"
      string = get_qual(creds)
      return render_template_string(string)

if __name__ == '__main__':
   app.config['TEMPLATES_AUTO_RELOAD'] = True
   app.run()
    
    