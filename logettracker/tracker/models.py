from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import uuid    

def collectedCardsDataValidator(jsonData):
        if not isinstance(jsonData, dict) or not len(jsonData) == 1 or not 'collected' in jsonData or not isinstance(jsonData['collected'], list):
            raise ValidationError(
                _("The collectedCards field must be a dictionary of format {'collected': [cardid1, cardid2, ...]}."),
                params={'jsonData': jsonData},
                )
        
        listOfCardIds = jsonData['collected']
        validCardIds = LoGetCards.objects.values_list('id', flat=True)
        for cardId in listOfCardIds:
            if not isinstance(cardId, int) or not cardId in validCardIds:
                raise ValidationError(
                    _("The collectedCards field must be a dictionary of format {'collected': [cardid1, cardid2, ...]}."),
                    params={'jsonData': jsonData},
                    )

class Users(models.Model):
    
    Id = models.UUIDField(default=uuid.uuid4, editable=False)
    Username = models.CharField(max_length=50)
    Created_at = models.DateTimeField(auto_now_add=True)
    Email = models.EmailField(max_length=254, primary_key=True)
    CardsColleted = models.JSONField(validators=[collectedCardsDataValidator], default=dict)



class URLStartCheckValidator(URLValidator):
    def __init__(self, startString, schemes=None, **kwargs):
        self.startString = startString
        super().__init__(schemes, **kwargs)
    
    def __call__(self, url):
        if not url.startswith(self.startString):
            raise ValidationError(
                _("The URL must start with '%(startString)s'."),
                params={'url': url, 'startString': self.startString},
                )
        super().__call__(url)
    

class LoGetCards(models.Model):        
    Id = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=100)
    Img = models.URLField(validators=[URLValidator(), URLStartCheckValidator("https://loget-card.jp/img/cards")])
    SpotmapLink = models.URLField(validators=[URLValidator(), URLStartCheckValidator("https://loget-card.jp/list_map.aspx")])
    LoGetURL = models.URLField(validators=[URLValidator(), URLStartCheckValidator("https://loget-card.jp/list.aspx")])
    SpotWebsiteLink = models.URLField()