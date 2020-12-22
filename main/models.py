import uuid
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel, DjangoCassandraModelMetaClass
from django.urls import reverse


class ConsistencyForMultipleModels:
    def save(self):
        class_list = (getattr(sys.modules[__name__], model) for model in self.models_list)
        obj = super(DjangoCassandraModel, self).save()
        obj_kwargs = {item[0]: item[1] for item in self.items()}
        for model_class in class_list:
            if self.__class__ != model_class:
                sub_obj = model_class(**obj_kwargs)
                super(DjangoCassandraModel, sub_obj).save()
        return obj


class CategoryByUrl(DjangoCassandraModel):
    class Meta:
        get_pk_field = 'url'
    url = columns.Text(primary_key=True)
    name = columns.Text()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', args=[self.url])


class Product(ConsistencyForMultipleModels, DjangoCassandraModel):
    __abstract__ = True
    models_list = ('ProductByUrl', 'Products', 'ProductsSortedByRating')
    price = columns.Double()
    number_of_ratings = columns.Integer(default=0)
    title = columns.Text()
    description = columns.Text()

    def get_absolute_url(self):
        return reverse('product-detail', args=[self.cat_url, self.url])


class ProductByUrl(Product):
    class Meta:
        get_pk_field = 'cat_url'
    cat_url = columns.Text(primary_key=True)
    url = columns.Text(primary_key=True, clustering_order="ASC")
    id = columns.TimeUUID()
    rating = columns.Double(default=0)


class Products(Product):
    class Meta:
        get_pk_field = 'cat_url'
    cat_url = columns.Text(primary_key=True)
    id = columns.TimeUUID(primary_key=True, clustering_order="ASC")
    number_of_ratings = columns.Integer(default=0)
    rating = columns.Double(default=0)


class GoodsSortedByRating(DjangoCassandraModel):
    class Meta:
        get_pk_field = 'cat_url'
    cat_url = columns.Text(primary_key=True)
    rating = columns.Double(primary_key=True, clustering_order="DESC", default=0)
    id = columns.TimeUUID(primary_key=True, clustering_order="DESC")
    url = columns.Text()


class ReviewsByProduct(DjangoCassandraModel):
    class Meta:
        get_pk_field = 'product_id'
    product_id = columns.TimeUUID(primary_key=True)
    review_id = columns.TimeUUID(primary_key=True, clustering_order="DESC")
    user_id = columns.TimeUUID()
    date = columns.DateTime()
    text = columns.Text()
    mark = columns.Integer()


class ReviewsByUser(DjangoCassandraModel):
    class Meta:
        get_pk_field = 'user_id'
    user_id = columns.TimeUUID(primary_key=True)
    review_id = columns.TimeUUID(primary_key=True, clustering_order="DESC")
    product_id = columns.TimeUUID()
    text = columns.Text()
    mark = columns.Integer()
    date = columns.DateTime()


class ItemsByOrder(DjangoCassandraModel):
    class Meta:
        get_pk_field = 'order_id'
    order_id = columns.TimeUUID(primary_key=True)
    product_id = columns.TimeUUID(primary_key=True, clustering_order="ASC")
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
    id = columns.TimeUUID()


class CartByUser(DjangoCassandraModel):
    class Meta:
        get_pk_field = 'user_id'
    user_id = columns.TimeUUID(primary_key=True)
    good_id = columns.TimeUUID(primary_key=True, clustering_order="ASC")
    count = columns.Counter()


class UserById(DjangoCassandraModel):
    class Meta:
        get_pk_field = 'user_id'
    id = columns.TimeUUID(primary_key=True, default=uuid.uuid1)
    email = columns.Text()
    password = columns.Text()
