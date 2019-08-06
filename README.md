# The Philospher's Groan: How I Learned To Love SQLAlchemy



This is more or less the same as the content of my slides. I wrote it out as preparation for my presentation and for posterity.

---

Databases and the language of databases, SQL, provide us an intuitive and time-tested way to describe and interact with databases.

Programming languages like Python give us a powerful way to express the transformation of data. In order to be useful, data at any scale needs to be recombined endlessly as it bounces from frontend to backend.

It's completely necessary that programming languages afford us some way to interface with SQL databases. There are security risks associated with running raw SQL from an application. Almost more importantly, it's weird to have SQL mixed into other code. It's a code smell. It can create a high cognitive switching cost for developers.

ORMs and sql-rendering tools allow us to step around a lot of these problems. SQLAlchemy is the tool of choice for many Python developers.

Created in 2006, SQLAlchemy has been around the block and supports a multitude of databases. It's *extensively* documented. Its name is completely apt. Database spelunkers know, the complexity of some SQL queries borders on arcane. SQLAlchemy does not shy from this.

![giphy](./README.assets/giphy.gif)

Much like transmuting the elements, transmuting data expertly with SQLAlchemy takes practice and a good bit of study. In my time learning it at least, I found myself battered from the journey at times.

![giphy-2](./README.assets/giphy-2.gif)

Today I'll be going over what I've come to understand about the nature SQLAlchemy since picking it up in earnest. We'll pay particular attention to the things that I had trouble wrapping my had around on my journey. I'll also share some of the transmutation techniques I've learned along the way.

![giphy-1](./README.assets/giphy-1.gif)

## 2.5 Ways of Doing Things

SQLAlchemy is a large library divided into 2 parts. `core` and `orm`.

They differ conceptually, but the constructs overlap frequently and the two toolsets are very cross-functional. Both allow you to manage and interact your database from the comfort of Python.

The .5th way of doing things will be covered later, alongside `core`, but in short, this libaray also allows you to interact with databases managed outside of Python apps.

### sqlalchemy.orm

`orm` does what you'd expect. It allows you to map Python class definitions to SQL tables and subsequently map instances of those classes to rows of those tables.

```python
# akin to ddl
class Bakery(Base):
    __tablename__ = "bakery"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    founded_date = Column(Date)

Base.metadata.create_all()

# insert, later on, elsewhere in the codebase...
to_insert = [
    ["Floriole", "Chicago", "01/01/1642"],
    ["Naomi's Treats", "Nebraska", "05/26/2008"],
    ["Taco Bell", "Valhalla", None],
]

session.add_all(
    [
        Bakery(name=name, location=loc, founded_date=dt)
        for name, loc, dt in to_insert
    ]
)

session.commit()

# select and delete, later on, elsewhere in the codebase...
missing_founded_date = session.query(Bakery).filter(
    Bakery.founded_date is None
)
might_not_be_bakery.delete()

session.commit()
```

The actual SQL-ing is largely abstracted away. You make objects and then at some point commit them, and they land in the database. You ask the class later on for instances of itself and receive them in list-like objects. You do stuff to them. Very cool.

#### Why use it?

1. You like OOP, ORMs, Python, or any combination of the 3.
2. Your i/o is straightforward and your database is clean.
3. You like Django.
4. You want there to be a predictable way of doing things across the team.

*[demo]*

### sqlalchemy.core

Rather than bending SQL constructs into the shape of the familiar objects of a programming language, `CORE` relies on an extensive selection of functions to *render sql expressions programatically*.

Authors use things like the `select()` function to create `SELECT` statements, passing in `and_()` function calls to create `AND` clauses and so on.

```python
# akin to ddl
bakery = Table(
    "bakery",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("location", String, nullable=False),
    Column("founded_date", Date),
)

metadata.create_all()

# insert, later on, elsewhere in the codebase...
to_insert = [
    ["Floriole", "Chicago", "01/01/1642"],
    ["Naomi's Treats", "Nebraska", "05/26/2008"],
    ["Taco Bell", "Valhalla", None],
]

insert_statement = bakery.insert().values(
    [
        {"name": name, "location": loc, "founded_date": dt}
        for name, loc, dt in to_insert
    ]
)

conn.execute(insert_statement)

# select and delete, later on, elsewhere in the codebase...
delete_statement = (
    select([bakery])
    .delete()
    .where(bakery.c.founded_date is None)
)

conn.execute(delete_statement)
```

Here, the actual SQL is all up in your face. You build actual statements and then pass them to a live database connection to execute them.

Note how we `.where()` insead of `.filter()` to get data. That's because we are not dealing with instances of anything, we're rendering SQL. Calling `str()` on `insert_statement` or `delete_statement` would produce SQL. In contrast, calling `str()` on an ORM instance returns its `__repr__`.

#### Why use it?

1. You like FP and native data structures.
2. You are a native SQL speaker. You speak SQL eloquently. You love SQL.
3. You dislike Django.
4. Your queries are complicated, you need to be scrappy and clever.

### sqlalchemy.core: guerilla style

In some cases, you're dealing with databases or parts of databases that are out of your control for some reason. Making models or `Table`s in SQLAlchemy comes with the assumption that you will create your tables *from* them. When this is impossible, `core` has powerful tools for inspecting and reflecting preexisting databases.

```python
metadata = MetaData(bind=engine)
metadata.reflect_all()
bakery = metadata.tables["bakery"]
```

This technique shines with iteractive use. You can check SQLAlchemy's assumptions about your database and use Python's already powerful introspection tools to learn more about the `Table` objects that get created.