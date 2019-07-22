from flask import render_template
from app import db
from app.errors import bp

#returning the contents of their respective templates
#returns the error code number along with the template

#new version __ use the blueprint decorator
#making the blueprint independent of the application so that it is
#more portable 
#changing the path to indicate errors sub directory
@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404



#500 error to be invoked after a db error
#any db session failures do not interfere with
#db aceesess, so issue a rollback which resets the
#session to a clean slate
@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500