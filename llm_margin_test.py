from core.llm import test_llm_margin_of_error, call_llm  # Adjust import as needed


# Example dummy values for demonstration
filename = "example.py"
content = """
from models import db
from datetime import datetime

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parking_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    leaving_timestamp = db.Column(db.DateTime, nullable=True)
    parking_cost = db.Column(db.Float, nullable=True)  # Calculated on release or booking

"""
decorators = []
repo = "sample_repo"

# Run the margin of error test
test_llm_margin_of_error(
    call_llm_func=call_llm,
    filename=filename,
    content=content,
    decorators=decorators,
    repo=repo,
    html_content=None,
    runs=10
)