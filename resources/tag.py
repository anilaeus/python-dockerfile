from flask.views import MethodView
from flask_smorest import abort, Blueprint
from schema import TagSchema
from models.tag import TagModel
from models.store import StoreModel
from db import db
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("tags", __name__, description="Operations on Tags")


@blp.route("/tag/<string:store_id>/tag")
class TagsInStore(MethodView):

    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(
        self, tag_data, store_id
    ):  # json her zaman pathvariable'dan once load olur

        if TagModel.query.filter(
            TagModel.store_id == store_id, TagModel.name == tag_data["name"]
        ).first():
            abort(400, message="Tag exists for the store")

        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=f"Error occured during inserting tag to db {str(e)}")

        return tag


@blp.route("/tag/<string:tag_id>")
def get(self, tag_id):
    tag = TagModel.query.get_or_404(tag_id)
    return tag
