from url_shortener import db

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), nullable=False)
    shortened = db.Column(db.String(6), unique=True, nullable=False)
    estimated_date = db.Column(db.DateTime(), nullable=False)

    def __repr__(self):
        return f'{self.url} shortened to {self.shortened} till {self.estimated_date}'