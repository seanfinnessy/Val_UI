from main import ma
from models import CompMatchModel


class CompMatchSchema(ma.SQLAlchemySchema):
    class Meta:
        model = CompMatchModel
        fields = (
            'matchId',
            'mapId',
            'seasonId',
            'matchStartTime',
            'tierAfterUpdate',
            'tierBeforeUpdate',
            'rankedRatingAfterUpdate',
            'rankedRatingBeforeUpdate',
            'rankedRatingEarned',
            'rankedRatingPerformanceBonus'
        )
    matchId = ma.auto_field()
    mapId = ma.auto_field()
    seasonId = ma.auto_field()
    matchStartTime = ma.auto_field()
    tierAfterUpdate = ma.auto_field()
    tierBeforeUpdate = ma.auto_field()
    rankedRatingAfterUpdate = ma.auto_field()
    rankedRatingBeforeUpdate = ma.auto_field()
    rankedRatingEarned = ma.auto_field()
    rankedRatingPerformanceBonus = ma.auto_field()
