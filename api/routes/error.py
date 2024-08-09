from flask import Blueprint, render_template # type: ignore

error = Blueprint('error', __name__,
                        template_folder='../../templates')

@error.app_errorhandler(404) 
def not_found(e): 
  return render_template("404.html", title="404") 

@error.app_errorhandler(403) 
def forbidden(e): 
  return render_template("forbidden.html", title="403") 