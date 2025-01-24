from flask.views import MethodView
from flask_smorest import abort, Blueprint
from schema import TagAndItemSchema, TagSchema
from models import TagModel, StoreModel, TagAndItemSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models.item import ItemModel

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


@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()

        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the tag")

        return tag

    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):

        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the tag")

        return {"message": "Item removed from tag", "item": item, "tag": tag}


@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):

    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @blp.response(
        202,
        description="Deletes a tag if no item is tagged with it.",
        example={"message": "Tag deleted"},
    )
    @blp.alt_response(404, description="Tag not found")
    @blp.alt_response(
        400,
        description="Returned if the tag is assigned to one or more itms. In this case the tag is not deleted",
    )
    def delete(self, tag_id):

        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            try:
                db.session.delete(tag)
                db.session.commit()
                return {"message": "Tag deleted"}
            except SQLAlchemyError:
                abort(500, message="Error while trying to delete the tag")
        abort(
            400,
            message="Could not delete the tag since there are items associated with it.",
        )
