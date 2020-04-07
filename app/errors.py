from flask import render_template
from app import app#, db


class APIError(Exception):
    """Base class for exceptions in this module."""
    pass

class ImageDetectionError(APIError):
    """Exception raised for errors in landmark detection.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(413)
def request_too_large_error(error):
    return render_template('413.html'), 413


@app.errorhandler(500)
def internal_error(error):
    # db.session.rollback()
    return render_template('500.html'), 500


@app.errorhandler(ImageDetectionError)
def custom_error(error):
    return render_template('image_error.html')


@app.errorhandler(Exception)
def unknown_error(error):
    return render_template('unknown_error.html')
