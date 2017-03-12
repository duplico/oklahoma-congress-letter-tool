from flask import render_template, flash, redirect, session, request, url_for, make_response
from okcongress_web import app, house_data, senate_data, all_committees
from okcongress_web import committee_names

@app.route('/committee_membership')
def membership():
    return render_template('list.html', cmtes=committee_names, membership=all_committees)

