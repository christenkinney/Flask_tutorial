from flask import Blueprint

#Blueprint class takes the name of the blueprint, base module (name)
#Creating blueprint object
bp = Blueprint('errors', __name__)

#Import handlers.py module so that error handlers in it are registered with 
#blueprint 
from app.errors import handlers