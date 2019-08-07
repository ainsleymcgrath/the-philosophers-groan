from sqlalchemy import select
from sqlalchemy.dialects import sqlite

from examples.source_data import baker_form, all_existing_breads
from examples.schemas_and_ddl.core_style import (
    baker,
    bread,
    baker_specialty,
    contact_info,
)


def render(smt):
    print(smt.compile(compile_kwargs={"literal_binds": True}, dialect=sqlite.dialect()))


def insert_and_update(conn):
    baker_insert_smt = baker.insert().values(
        [
            {"name": name, "pronouns": info_dict["pronouns"]}
            for name, info_dict in baker_form.items()
        ]
    )

    breakpoint()
    # no reprs, but we can render!

    conn.execute(baker_insert_smt)

    bakers_in_db = conn.execute(select([baker.c.id, baker.c.name]))
    baker_id_dict = {
        baker_name: baker_id for baker_id, baker_name in bakers_in_db.fetchall()
    }

    contact_insert_smt = contact_info.insert().values(
        [
            {**info_dict["contact"], "baker_id": baker_id_dict[name]}
            for name, info_dict in baker_form.items()
        ]
    )

    breakpoint()
    # acrobatics frequently required; note how executions return stuff

    conn.execute(contact_insert_smt)

    bread_insert_smt = bread.insert().values(
        [bread_info_dict for bread_info_dict in all_existing_breads]
    )

    conn.execute(bread_insert_smt)

    breads_in_db = conn.execute(select([bread.c.id, bread.c.name]))
    bread_id_dict = {
        bread_name: bread_id for bread_id, bread_name in breads_in_db.fetchall()
    }

    specialty_values = []
    for name, info_dict in baker_form.items():
        baker_id = baker_id_dict[name]
        for specialty in info_dict["specialties"]:
            specialty_values.append(
                {"baker_id": baker_id, "bread_id": bread_id_dict[specialty]}
            )

    breakpoint()
    baker_specialty_insert_smt = baker_specialty.insert().values(specialty_values)
    conn.execute(baker_specialty_insert_smt)


def select_join_delete(conn):
    join = baker.join(baker_specialty).join(bread)

    mediocre_bakers = (
        select([baker.c.id]).select_from(join).where(bread.c.is_delicious == False)
    )

    delete_smt = baker.delete().where(baker.c.id.in_(mediocre_bakers))

    breakpoint()

    conn.execute(delete_smt)


def walkthrough(engine):
    conn = engine.connect()

    insert_and_update(conn)
    select_join_delete(conn)

    conn.close()
