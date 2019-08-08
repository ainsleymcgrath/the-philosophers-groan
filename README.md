# The Philosopher's Groan: How I Learned To Love SQLAlchemy

This is more or less the same as the content of my slides. There's a bunch of additional commentary, as I wrote it out as preparation for my presentation and for posterity.

Thanks to [Typora](https://typora.io/) for creating a pleasant place to write this and this [lovely tool](https://romannurik.github.io/SlidesCodeHighlighter/) for adding code blocks to Google Slides by @romannurik. 

And to the developers of SQLAlchemy. And the creators of Fullmetal Alchemist.

---

Databases and the language of databases, SQL, provide us an intuitive and time-tested way to describe and interact with databases.

Programming languages like Python give us a powerful way to express the transformation of data. To be useful, data at any scale needs to be recombined endlessly as it bounces from frontend to backend.

Programming languages must afford us some way to interface with SQL databases. There are security risks associated with running raw SQL from an application. Almost more importantly, it's weird to have SQL mixed into other code. It's a code smell. It can create a high cognitive switching cost for developers.

ORMs and SQL-rendering tools allow us to step around a lot of these problems. SQLAlchemy is the tool of choice for many Python developers.

Created in 2006, SQLAlchemy has been around the block and supports a multitude of databases. It's *extensively* documented. Its name is completely apt. Database spelunkers know, the complexity of some SQL queries borders on arcane. SQLAlchemy does not shy from this.

![giphy](./README.assets/giphy.gif)

Much like transmuting the elements, transmuting data expertly with SQLAlchemy takes practice and a good bit of study. In my time learning it at least, I found myself battered from the journey at times.

![giphy-2](./README.assets/giphy-2.gif)

Today I'll be going over what I've come to understand about the nature SQLAlchemy since picking it up in earnest. We'll pay particular attention to the things that I had trouble wrapping my head around on my journey. I'll also share some of the transmutation techniques I've learned along the way.

## 2.5 Ways of Doing Things

SQLAlchemy is a large library divided into 2 parts. `core` and `orm`.

They differ conceptually, but the constructs overlap frequently and the two toolsets are very cross-functional. Both allow you to manage and interact with your database from the comfort of Python.

The .5th way of doing things will be covered later, alongside `core`, but in short, this library also allows you to interact with databases managed outside of Python apps.

Below are some truncated samples of what `core` and `orm` code looks like. Major constructs that you'll see here are covered later on.

### sqlalchemy.orm

`orm` does what you'd expect. It allows you to map Python class definitions to SQL tables and subsequently map instances of those classes to rows of those tables.

```python
# ddl
class Bakery(Base):
    __tablename__ = "bakery"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    founded_date = Column(Date)
    
    def __repr__(self):
          return f"<Baker {self.name}>"

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

### sqlalchemy.core

Rather than bending SQL constructs into the shape of the familiar objects of a programming language, `CORE` relies on an extensive selection of functions to *render SQL expressions programmatically*.

Authors use things like the `select()` function to create `SELECT` statements, passing in `and_()` function calls to create `AND` clauses and so on.

```python
# ddl
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
      .where(bakery.c.founded_date is None)
    .delete()  
)

conn.execute(delete_statement)
```

Here, the actual SQL is all up in your face. You build statements and then pass them to a live database connection to execute them.

Note how we `.where()` insead of `.filter()` to get data. That's because we are not dealing with instances of anything, we're rendering SQL. Calling `str()` on `insert_statement` or `delete_statement` would produce SQL. In contrast, calling `str()` on an ORM instance returns its `__repr__`.

#### Why use it?

1. You like FP and native data structures.
2. You are a native SQL speaker. You speak SQL eloquently. You love SQL.
3. You dislike Django.
4. Your queries are complicated, you need to be scrappy and clever.

### sqlalchemy.core: headless

In some cases, you're dealing with databases or parts of databases that are out of your control for some reason. Making models or `Table`s in SQLAlchemy comes with the assumption that you will create your tables *from* them. When this is impossible, `core` has powerful tools for inspecting and reflecting preexisting databases.

```python
metadata = MetaData(bind=engine)
metadata.reflect_all()
bakery = metadata.tables["bakery"]
```

#### Why use it?

1. You are unable to manage your database with Python.
2. You are interactively exploring a database, with Python.

## Key Players

A number of factories and resulting objects are frequently sighted in SQLAlchemy code. Some are only useful and idiomatic in one part of the library, some are cross-functional. Understanding the distinctions is key to effectively learning this library and performing arcane acts of SQL. 

![giphy-1](./README.assets/giphy-1.gif)

#### The Database Engine & Dialects

The SQLALchemy [docs](https://docs.sqlalchemy.org/en/13/core/engines.html) have referred to this as "home base." 

Users interface with it in a limited capacity, but it does all the heavy lifting of figuring out how best to communicate with the `Dialect` of your particular database, creating connection pools, and interpreting Python's `DBAPI`.

```python
# factory is common to core and orm
from sqlalchemy import create_engine
engine = create_engine("postgresql://van:hoenheim@resembool.db:5432/fma")
engine.dispose()  # close down all connections when work is over
```

`Dialect`s are barely touched at all except for rendering generated SQL, either interactively or for logs. Most [major databases](https://docs.sqlalchemy.org/en/13/dialects/index.html) are supported

#### The Database Schema

Aptly named, `MetaData`, this class is accessible in several ways, with separate approaches for `core` and `orm`

```python
# core
from sqlalchemy import MetaData
metadata = MetaData(bind=engine)

#orm
from sqlalchemy.ext.declarative import declarative_base
Base = declarati(bind=engine)  # config can happen in many places
Base.metadata  # produces the same object as above
```

`MetaData` magically maintains the global state of the database objects defined by your SQLAlchemy code and optionally any preexisting objects in the database/schema your `Engine` points at. Noteworthy methods and attributes include:

```python
create_all()  # creates Tables and table mappings defined in your python code
drop_all()  # drops anything created with `create_all`
reflect()  # gives `MetaData` awareness of an existing DB's information schema
bind  # an attribute often used as a setter; attach `Engine`s with it
tables  # a dict, contains `Table` instances that have been created/reflected
```

#### Table Abstractions

The essence of any kind of data access tool is the abstraction used to represent your remote data. This is where alchemic approaches begin to diverge notably. The things we most often touch directly are the `declarative_base` factory, the `Table` object, and the `Column` object.

The thing we don't touch is the `mapper`, but when using ORM it does quite a bit of work. 

```python
# core
Table()  # instances take positional args to emit table DDL 
         # and later access data from those tables

# orm
declarative_base()  # factory that produces a class you use to map Python objects to 
                                        # database objects, again emitting DDL and acting as an accessor

mapper()  # does the aforementioned mapping, almost always behind the scenes

# common
Column()  # aids in DDL emission, does what you'd expect and provides conveniences
          # such as triggers, fancy value defaults, 
```

#### Connections & Transactions

The divergence intensifies. `orm` users will want to grab themselves a `Session` when making queries (which are covered in the next section). `core` users get their kicks with a `Connection` or `Transaction`.

```python
# orm
from sqlalchemy.orm.session import sessionmaker
Session = sessionmaker()  # use it like a global or singleton
session = Session(bind=engine)  # instantiate at query time, somewhere local
```

The `Session` is magic. It's like a cutting board. We do all our prep on it and pause before tossing the whole mess in the pan. Objects are added to it via various methods and it holds on to these operations in state. We can inspect the changes to our mapped ORM object instances before finally `commit`ing them and emitting SQL to the database. Notable methods and attributes include:

```python
add()  # add an object to the session; prepare to add data to the corresponding table
add_all()  # same as above but in bulk
delete()  # add instructions to delete an object before doing so in the DB
new  # a list-like of objects added since session creation
dirty  # a list-like of objects in session that have been mutated
query()  # produces a `Query`, more info in the next section
rollback()  # undo the current transaction
commit()  # emits the SQL version of anything done to the session before
```

The `Connection` is spartan. No bells, no whistles, very little magic. We get it from our `engine`. Usage is pretty transparent:

```python
# core
conn = engine.connect()  # the engine came from somewhere global
                                                 # connection should be local

conn.execute(statement)  # statement building covered soon
conn.close()
```

Some less frequently used `Connection` tools:

```python
transaction = conn.begin()  # a `Transaction` object offers some niceties of `Session`
conn.execute(statemement)
transaction.commit()  # emits pending statements from conn.execute calls

raw_conn = engine.raw_connection()  # for barbarians; .execute() takes plain SQL
```

#### Queries and Queryish Constructs

This is where my confusion became unbearable. The idioms from `core` and `orm` *can* be wrestled into working together, but that's either gonna be advanced or smelly. We've fully diverged at this point. 

`orm` has the `Query` object. Not bad. It has methods like `cte`, `subquery`,  and `limit` to let us build out SQL constructs from the comfort of Python objects.

```python
session.query(Bakery)  # produces a `Query`. 
                                             # this one is equivalent to SELECT * FROM BAKERY

bennisons = Bakery(name="bennisons", location="Evanston")
session.add(bennisons)  # on commit(), an insert is emitted
bennisons.name = "Bennison's"  # session will remember this mutation and commit accordingly

session.query(Bakery.name, Baker.name)
    .filter(Bakery.location == "Chicago")
      .join(Baker)
    .filter(Baker.pronouns == "she/her")
    .order_by(Baker.age.desc())
    .limit(10)
    .cte(name="oldest_female_identifying_bakers")
```

The second `query` call above produces some SQL like this.

```sql
WITH oldest_female_identifying_bakers AS (
    SELECT bkry.name, bkr.name
  FROM bakery bkry
  JOIN bakery_employees be ON be.bakery_id = bkry.id
  JOIN baker bkr ON bkr.id = be.baker_id
  WHERE bkr.pronouns = "she/her"
  ORDER BY bkr.age DESC
  LIMIT 10
)

SELECT * FROM oldest_female_identifying_bakers;
```

Note how we use `.filter` rather than something like `.where`. That's what makes ORM ORM. We aren't dealing with tables, we are dealing with a set of Python objects *mapped* to tables. For our comfort, this is abstracted away and hidden inside the mechanics of `session.commit()`. We `session.add` objects rather than talking about database inserts, etc.

 `core` takes it to a lower level, offering a dizzying array of objects such as `Selectable`, `Insert`, `Update`, `From`, and `Delete`, all with lowercased factories to produce them and dialect-specific variations. There are myriad helper functions as well, such as `and_`, `or_`, `case`, and the venerable `func`, to really get the party going. 

Recreating the above with core looks pretty different.

```python
select([bakery])  # bakery here is an instance of `Table`
                  # this is SELECT * FROM BAKERY
  
inset_smt = bakery.insert().values({"name": "bennisons", "location": "Evanston"})
conn.execute(insert_smt)

update_smt = (
  bakery.update()
    .where(bakery.c.name == "bennisons")
  .values(name="Bennison's")
)
conn.execute(update_smt)

join = bakery.join(bakery_employees).join(baker)
select_smt = select([bakery.c.name, baker.c.name])
        .select_from(join)
      .where(baker.c.pronouns == "she/her")
    .order_by(baker.c.age.desc())
    .limit(10)
    .cte(name="oldest_female_identifying_bakers")
    
result = conn.execute(select_smt).fetchall()
```

## In Conclusion

SLALchemy is a wonderful tool for interacting with SQL databases in Python.

With the `orm` part of the library, we gain all the benefits of an ORM. There are great conveniences for dealing with i/o spanning database relationships.

With `core`, we can get down and dirty with SQL. We think in statements rather than in objects, and in the absence of models and migrations and the like, it provides a low-level toolset for creating complex SQL queries.

Both can have a place in your codebase as long as we keep the delineation of style clear. Better to get a model's table object from `metadata.tables` than from `Model.__table__`. It sets the tone for the reader and avoids the suspicion aroused by a mysterious dunder. Hopefully, the examples above have proved illustrative. 

May your transmutations yield new and exciting combinations of data. Please use your newfound arcane wisdom for good.