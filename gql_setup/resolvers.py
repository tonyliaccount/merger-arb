from ariadne import QueryType, MutationType
from models import MarginCallPriceEntry

# This is the overall list of calculated margin call prices. Should be replaced with database later on.
price_history = []

query = QueryType()
mutation = MutationType()

@query.field('hello')
def resolve_hello(_, info):
    return "Hello there!"

@query.field('marginCallPriceHistory')
def resolve_price_history(_, info):
    return price_history

@mutation.field('marginCallPrice')
def resolve_margin_call_price(_, info, price, initial_margin, maintenance_margin, type):

    # Create a new margin call price entry. The constructor will automatically call the associated helper function
    newPriceEval = MarginCallPriceEntry(price, initial_margin, maintenance_margin, type.lower())

    # Keep track of the margin call price entry.
    price_history.append(newPriceEval)
  
    return newPriceEval