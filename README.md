# The Philospher's Groan: How I Learned To Love SQLAlchemy

Databases and the language of databases, SQL, provide us an intuitive and time-tested way to describe and interact with databases.

Programming languages like Python give us a powerful way to express the transformation of data. In order to be useful, data at any scale needs to be recombined endlessly as it bounces from frontend to backend.

It's completely necessary that programming languages afford us some way to interface with SQL databases. There are security risks associated with running raw SQL from an application. Almost more importantly, it's weird to have SQL mixed into other code. It's a code smell. It can create a high cognitive switching cost for developers.

ORMs and sql-rendering tools allow us to step around a lot of these problems. SQLAlchemy is the tool of choice for many Python developers.

Created in 2006, SQLAlchemy has been around the block and supports a multitude of databases. It's *extensively* documented. Its name is completely apt. Database spelunkers know, the complexity of some SQL queries borders on arcane. SQLAlchemy does not shy from this.

![giphy](./README.assets/giphy.gif)

Much like transmuting the elements, transmuting data expertly with SQLAlchemy takes practice and a good bit of study. In my time learning it at least, I found myself battered from the journey at times.

![giphy-2](./README.assets/giphy-2.gif)

Today I'll be going over what I've come to understand about the nature SQLAlchemy since picking it up in earnest. We'll pay particular attention to the things that I had trouble wrapping my had around on my journey. I'll also share some of the cool transmutation techniques I've learned along the way.

![giphy-1](./README.assets/giphy-1.gif)
