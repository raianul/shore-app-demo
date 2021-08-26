from flask_restful import Api

from shore_app.api.users import UserItem, UserItems
from shore_app.api.subscription import SubscriptionItem, SubscriptionItems

api = Api()

api.add_resource(UserItems, '/api/users')
api.add_resource(UserItem, '/api/user/<int:user_id>')
api.add_resource(SubscriptionItems, '/api/subscriptions')
api.add_resource(SubscriptionItem, '/api/subscription/<int:sub_id>')
