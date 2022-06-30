from main import db


class CompMatchModel(db.Model):
    # primary_key means its a unique identifier.
    matchId = db.Column(db.String(50), primary_key=True)
    # nullable = False means there must be a name.
    mapId = db.Column(db.String(50), nullable=False)
    seasonId = db.Column(db.String(50), nullable=False)
    # Epoch in ms
    matchStartTime= db.Column(db.Integer, nullable=False)
    tierAfterUpdate= db.Column(db.Integer, nullable=False)
    tierBeforeUpdate= db.Column(db.Integer, nullable=False)
    rankedRatingAfterUpdate= db.Column(db.Integer, nullable=False)
    rankedRatingBeforeUpdate= db.Column(db.Integer, nullable=False)
    rankedRatingEarned= db.Column(db.Integer, nullable=False)
    rankedRatingPerformanceBonus=db.Column(db.Integer, nullable=False)
    
    # return a printable representation of the given object
    # def __repr__(self)=
    #     return f"Video(name={name}, views={views}, likes={likes})"