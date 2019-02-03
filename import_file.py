"""
This script import XML file.
"""
import argparse
import django
import os

from logging import getLogger


logger = getLogger('carwash.scripts.import_file')


def main(args):
    assert (args.filename), '"--filename" is required'

    logger.info('Importing file %s', dict(
        filename=args.filename,
    ))

    from pos.models import Pos
    Pos.import_file(args.filename)


if __name__ == '__main__':
    # Important !
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carwash.settings")
    django.setup()

    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", help="The filename to import")

    main(parser.parse_args())
