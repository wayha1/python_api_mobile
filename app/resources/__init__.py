from app.resources.resource import *
from app.extensions import api 

api.add_namespace(ns_profile)
api.add_namespace(ns_auth)
api.add_namespace(ns_category)
api.add_namespace(ns_book)
api.add_namespace(ns_author)