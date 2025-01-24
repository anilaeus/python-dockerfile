from flask import request
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from schema import StoreSchema
from models.item import ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.store import StoreModel


blp = Blueprint("stores", __name__, description="Operations on Stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):

    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}


@blp.route("/store")
class Store(MethodView):

    @blp.response(200, StoreSchema)
    def get(self):
        stores = StoreModel.query.all()
        return stores

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):

        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()

        except IntegrityError:
            abort(500, message="A store with that name already exists")

        except SQLAlchemyError:
            abort(500, message="Error occured while trying to add store")

        return store
