from uuid import uuid4
from helpers import margin_call_price

class MarginCallPriceEntry:
  
    def __init__(self, price, initial_margin, maintenance_margin, type):    
        self.id = uuid4()
        self.price = price
        self.initial_margin = initial_margin
        self.maintenance_margin = maintenance_margin
        self.type = type
        self.margin_call_price = margin_call_price(price, initial_margin, maintenance_margin, type)