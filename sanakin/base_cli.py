import sys

from sqlalchemy.exc import IntegrityError

from .cli_const import INSERT_DATA_NUM, MAX_QUERY_SIZE

def _simple_insert(klass, logger, *column_names):
    def _insert(session, *attr):
        d = dict(zip(column_names, attr))

        m = klass(**d)

        try:
            session.add(m)
            session.commit()
        except IntegrityError as e:
            err_code, _ = e.orig.args
            if err_code == 1062:
                logger.info('格納済み')
                session.rollback()
            else:
                raise e

    return _insert

def _simple_delete(klass, *column_names):
    def _delete(session, *attr):
        d = dict(zip(column_names, attr))

        m = session.query(klass).filter_by(**d)
        m.delete()
        session.commit()

    return _delete

def _bulk_insert(
    session,
    engine,
    iterator,
    insert_statement,
    logger,
    is_develop_mode
):

    def _insert(instances):
        with engine.begin() as conn:
            conn.execute(insert_statement, instances)
        logger.info(f'INSERT: {len(instances)}件挿入!!!')

    instances = []

    n = 0
    for i in iterator:
        if is_develop_mode and n >= INSERT_DATA_NUM:
            break

        if sys.getsizeof(instances) < MAX_QUERY_SIZE:
            instances.append(i)
        else:
            _insert(instances)
            instances = []
        n += 1

    if instances:
        _insert(instances)
    session.commit()
