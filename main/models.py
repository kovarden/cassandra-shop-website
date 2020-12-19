import uuid
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel


# class Users(DjangoCassandraModel):
#     # example_id    = columns.UUID(primary_key=True, default=uuid.uuid4)
#     email = columns.Text(primary_key=True, default=uuid.uuid4)
#     example_type = columns.Integer(index=True)
#     created_at = columns.DateTime()
#     description = columns.Text(required=False)

# class GoodsSortedByRating(DjangoCassandraModel):
#     class Meta:
#         # use_in_migrations = False
#         managed = False
#         db_table = 'goods_sorted_by_rating'
#         get_pk_field = 'category_name'
#     category_name = columns.Text(primary_key=True)
#     rating = columns.Integer(primary_key=True, clustering_order="DESC")
#     id = columns.TimeUUID(primary_key=True, clustering_order="ASC", default=uuid.uuid1)
#     number_of_ratings = columns.Integer(default=0)
#     title = columns.Text()
#     description = columns.Text()

class CategoriesById(DjangoCassandraModel):
    class Meta:
        get_pk_field = 'cat_id'
    id = columns.TimeUUID(primary_key=True, default=uuid.uuid1)
    cat_name = columns.Text()


class Goods(DjangoCassandraModel):
    class Meta:
        get_pk_field = 'cat_id'
    cat_id = columns.TimeUUID(primary_key=True)
    id = columns.TimeUUID(primary_key=True, clustering_order="ASC")
    number_of_ratings = columns.Integer(default=0)
    rating = columns.Double(default=0)
    title = columns.Text()
    description = columns.Text()


class GoodsSortedByRating(DjangoCassandraModel):
    class Meta:
        get_pk_field = 'cat_id'
    cat_id = columns.TimeUUID(primary_key=True)
    rating = columns.Integer(primary_key=True, clustering_order="DESC", default=0)
    id = columns.TimeUUID(primary_key=True, clustering_order="DESC")
    number_of_ratings = columns.Integer(default=0)
    title = columns.Text()
    description = columns.Text()


class ReviewsByGood(DjangoCassandraModel):
    class Meta:
        get_pk_field = 'good_id'
    good_id = columns.TimeUUID(primary_key=True)
    review_id = columns.TimeUUID(primary_key=True, clustering_order="DESC")
    user_id = columns.TimeUUID()
    date = columns.DateTime()
    text = columns.Text()
    mark = columns.Integer()


class GoodsByOrder(DjangoCassandraModel):
    class Meta:
        get_pk_field = 'order_id'
    order_id = columns.TimeUUID(primary_key=True)
    good_id = columns.TimeUUID(primary_key=True, clustering_order="ASC")
    count = columns.Integer()
    sum = columns.Double()


class OrdersByUser(DjangoCassandraModel):
    class Meta:
        get_pk_field = 'user_id'
    user_id = columns.TimeUUID(primary_key=True)
    order_id = columns.TimeUUID(primary_key=True, clustering_order="DESC")
    count = columns.Integer()
    sum = columns.Double()


class UserByEmail(DjangoCassandraModel):
    class Meta:
        get_pk_field = 'email'
    email = columns.Text(primary_key=True)
    password = columns.Text()
    user_id = columns.TimeUUID()


class CartByUser(DjangoCassandraModel):
    class Meta:
        get_pk_field = 'user_id'
    user_id = columns.TimeUUID(primary_key=True)
    good_id = columns.TimeUUID(primary_key=True, clustering_order="ASC")
    count = columns.Counter()


class UserById(DjangoCassandraModel):
    class Meta:
        get_pk_field = 'user_id'
    user_id = columns.TimeUUID(primary_key=True, default=uuid.uuid1)
    email = columns.Text()
    password = columns.Text()


class ReviewsByUser(DjangoCassandraModel):
    class Meta:
        get_pk_field = 'user_id'
    user_id = columns.TimeUUID(primary_key=True)
    review_id = columns.TimeUUID(primary_key=True, clustering_order="DESC")
    good_id = columns.TimeUUID()
    text = columns.Text()
    mark = columns.Integer()
    date = columns.DateTime()
