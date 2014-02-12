from . import web, db


def shell():
    import IPython
    from .web import session
    from . import *
    events = session.query(Event).all()
    e = events[0]
    IPython.embed()


def parse_args():
    import argparse

    parser = argparse.ArgumentParser(prog='WorkoutCalendar', description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    sps = parser.add_subparsers()

    sp = sps.add_parser('initdb', help=db.initdb.__doc__)
    sp.set_defaults(func=db.initdb)

    sp = sps.add_parser('resetdb', help=db.resetdb.__doc__)
    sp.set_defaults(func=db.resetdb)

    sp = sps.add_parser('shell', help=shell.__doc__)
    sp.set_defaults(func=shell)

    sp = sps.add_parser('runweb', help=web.runweb.__doc__)
    sp.add_argument('-p', '--port', type=int, default=4848,
                    help='port to bind the server to')
    sp.add_argument('-H', '--host', default='localhost',
                    help='host to bind the server to')

    sp.set_defaults(func=web.runweb)

    args = parser.parse_args()
    kwargs = dict(args._get_kwargs())
    del kwargs['func']

    debug = kwargs.pop('debug', False)
    if debug:
        import ipdb

        with ipdb.launch_ipdb_on_exception():
            args.func(**kwargs)
    else:
        args.func(**kwargs)

