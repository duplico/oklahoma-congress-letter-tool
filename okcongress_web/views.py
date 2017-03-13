from flask import render_template, flash, redirect, session, request, url_for, make_response
from okcongress_web import app, house_data, senate_data, all_committees
from okcongress_web import committee_names, house_committee_names
from okcongress_web import senate_committee_names

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/committee_membership')
def membership():
    return render_template('list.html', cmtes=committee_names, membership=all_committees)

@app.route('/cmte_letter')
def letter_start():
    return render_template('list_select.html',
                           all_cmtes=committee_names,
                           house_cmtes=house_committee_names,
                           senate_cmtes=senate_committee_names,
                           membership=all_committees)
