from sqlalchemy.orm import sessionmaker

from examples.source_data import baker_form, all_existing_breads
from examples.schemas_and_ddl.orm_style import (
    Baker,
    Bread,
    baker_specialty,
    ContactInfo,
)


def insert_and_update(session):
    bakers_with_contact_info = [
        Baker(
            name=name,
            pronouns=info_dict["pronouns"],
            contact=ContactInfo(**info_dict["contact"]),
        )
        for name, info_dict in baker_form.items()
    ]

    session.add_all(bakers_with_contact_info)

    breakpoint()
    # observe that 8, rather than 4 objects are in session
    # herein lie the niceties of ORM

    breads = [Bread(**bread_info_dict) for bread_info_dict in all_existing_breads]

    session.add_all(breads)

    breakpoint()
    # observe how we can query the session even though nothing is committed

    for baker in session.query(Baker).all():
        specialties_from_form = baker_form[baker.name]["specialties"]

        # updates are asssignments in ORM world
        baker.specialties = (
            session.query(Bread).filter(Bread.name.in_(specialties_from_form)).all()
        )

    breakpoint()
    # observe the dirty session, note that we didn't touch the bridge table

    session.commit()


def select_join_delete(session):
    mediocre_bakers = (
        session.query(Baker)
        .join(baker_specialty)
        .join(Bread)
        .filter(Bread.is_delicious == False)
        .all()
    )

    breakpoint()

    for baker in mediocre_bakers:
        session.delete(baker)

    breakpoint()
    # observe, we can rollback! we won't thogugh.

    session.commit()


def walkthrough(engine):
    Session = sessionmaker(bind=engine)
    conn = engine.connect()
    session = Session(bind=conn)

    insert_and_update(session)
    select_join_delete(session)

    session.close()
