from application import db

class Token(db.Model):
    """Data model for user accounts."""

    __tablename__ = 'tokens'
    key = db.Column(
        db.String(15),
        primary_key=True
    )
    value = db.Column(
        db.String(12),
        index=True,
        unique=True,
        nullable=False
    )