from flask import Flask, request, render_template, redirect, flash
from converter import result, code_is_valid, num_is_valid

app = Flask(__name__)

app.config['SECRET_KEY'] = "oh-so-secret"

@app.route('/')
def get_home():
    """ Route for home page """
    return render_template('index.html')

@app.route('/', methods=['POST'])
def handle_form():
    """ Post route for when user submits data """
    curr_from = request.form.get("curr-from").upper()
    if not code_is_valid(curr_from) or not curr_from: #If code isn't valid of field is left empty
        flash("Starting currency code is not valid")
        return redirect('/')
    curr_to = request.form.get("curr-to").upper()
    if not code_is_valid(curr_to) or not curr_to:
        flash("Ending currency code is not valid")
        return redirect('/')
    amt = (request.form.get("amt"))
    if not num_is_valid(amt) :
        flash("Please enter a valid currency amount")
        return redirect('/')
    

    resulting_data = result(curr_from, curr_to, amt)
    
    print(resulting_data)
    return render_template('index.html', resulting_data = resulting_data)