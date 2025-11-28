from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from .register import *
from .login import *
from .token import *
