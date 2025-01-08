import os
from dotenv import load_dotenv
from peewee import *

# Загрузим переменные
load_dotenv()

db_server = os.getenv("SQL_SERVER")
db_user = os.getenv("SQL_USER")
db_password = os.getenv("SQL_PASSWORD")
db_port = int(os.getenv("SQL_PORT")) if os.getenv("SQL_PORT") else 3306
db_name = os.getenv("SQL_DB")

database = MySQLDatabase(
    db_name,
    **{
        "charset": "utf8",
        "sql_mode": "PIPES_AS_CONCAT",
        "use_unicode": True,
        "host": db_server,
        "port": db_port,
        "user": db_user,
        "password": db_password,
    }
)


class UnknownField(object):
    def __init__(self, *_, **__):
        pass


class BaseModel(Model):
    class Meta:
        database = database


class Actor(BaseModel):
    actor_id = AutoField()
    first_name = CharField()
    last_name = CharField(index=True)
    last_update = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = "actor"


class Country(BaseModel):
    country = CharField()
    country_id = AutoField()
    last_update = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = "country"


class City(BaseModel):
    city = CharField()
    city_id = AutoField()
    country = ForeignKeyField(
        column_name="country_id", field="country_id", model=Country
    )
    last_update = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = "city"


class Address(BaseModel):
    address = CharField()
    address2 = CharField(null=True)
    address_id = AutoField()
    city = ForeignKeyField(column_name="city_id", field="city_id", model=City)
    district = CharField()
    last_update = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    location = UnknownField(index=True)  # geometry
    phone = CharField()
    postal_code = CharField(null=True)

    class Meta:
        table_name = "address"


class Category(BaseModel):
    category_id = AutoField()
    last_update = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    name = CharField()

    class Meta:
        table_name = "category"


class Language(BaseModel):
    language_id = AutoField()
    last_update = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    name = CharField()

    class Meta:
        table_name = "language"


class Film(BaseModel):
    description = TextField(null=True)
    film_id = AutoField()
    imdb_id = CharField(null=True)
    language = ForeignKeyField(
        column_name="language_id", field="language_id", model=Language
    )
    last_update = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    length = IntegerField(null=True)
    original_language = ForeignKeyField(
        backref="language_original_language_set",
        column_name="original_language_id",
        field="language_id",
        model=Language,
        null=True,
    )
    poster_url = CharField(null=True)
    rating = CharField(constraints=[SQL("DEFAULT 'G'")], null=True)
    release_year = IntegerField()  # UnknownField(null=True)  # year
    rental_duration = IntegerField(constraints=[SQL("DEFAULT 3")])
    rental_rate = DecimalField(constraints=[SQL("DEFAULT 4.99")])
    replacement_cost = DecimalField(constraints=[SQL("DEFAULT 19.99")])
    special_features = CharField(null=True)
    title = CharField(index=True)

    class Meta:
        table_name = "film"


class FilmActor(BaseModel):
    actor = ForeignKeyField(column_name="actor_id", field="actor_id", model=Actor)
    film = ForeignKeyField(column_name="film_id", field="film_id", model=Film)
    last_update = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = "film_actor"
        indexes = ((("actor", "film"), True),)
        primary_key = CompositeKey("actor", "film")


class FilmCategory(BaseModel):
    category = ForeignKeyField(
        column_name="category_id", field="category_id", model=Category
    )
    film = ForeignKeyField(column_name="film_id", field="film_id", model=Film)
    last_update = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = "film_category"
        indexes = ((("film", "category"), True),)
        primary_key = CompositeKey("category", "film")


class SearchResults(BaseModel):
    description = TextField(null=True)
    release_year = IntegerField(null=True)
    search_type = CharField(null=True)
    search_value = CharField(null=True)
    title = CharField(null=True)

    class Meta:
        table_name = "search_results"
