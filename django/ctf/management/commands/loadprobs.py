import os, sys, traceback, shutil, uuid
from os.path import join, isfile, isdir

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

import yaml

from ctf.models import CtfProblem


class Command(BaseCommand):
    help = "Adds/Updates problems from PROBLEM_DIR"

    def add_arguments(self, parser):
        pass

    def handle(self, **options):
        # TODO(Cam): Copy static files

        BASEDIR = settings.PROBLEMS_DIR
        STATIC_BASE = join(settings.STATIC_ROOT, 'problems')
        PROBLEM_BASENAME = 'problem.yaml'
        GRADER_BASENAME = 'grader.py'
        PK_FIELD = 'id'

        write = self.stdout.write

        errors = []

        write("Walking '{}'".format(BASEDIR))
        for root in os.listdir(BASEDIR):

            # Skip files
            if isfile(join(BASEDIR, root)):
                continue

            # Ignore private dirs
            if root.startswith('_'):
                write("Ignoring '{}': Marked private with underscore".format(root))
                continue

            # Load problem file
            problem_filename = join(BASEDIR, root, PROBLEM_BASENAME)
            try:
                with open(problem_filename) as problem_file:
                    data = yaml.load(problem_file)
            except (IsADirectoryError, FileNotFoundError):
                write("Skipping '{}': No problems file found".format(root))
                errors.append(sys.exc_info())
                continue
            else:
                if 'id' in data:
                    write('Warning: integer IDs are deprecated/ignored and will be replaced with UUIDs.')
                    write("Create or edit .uuid file in folder '{}' instead.".format(root))
                    del data['id']
                data['grader'] = join(root, GRADER_BASENAME)

            # XXX(Cam): Maybe get rid of magic '.uuid' string?
            uuid_file = join(BASEDIR, root, '.uuid')
            uuid_exists = isfile(uuid_file)
            if uuid_exists:
                with open(uuid_file, 'r') as f:
                    data['id'] = uuid.UUID(f.read())

            # Check it problem already exists
            problem_id = data.get(PK_FIELD, '')
            # XXX(Cam) - why make the end developer have to keep track of his own problem IDs?
            query = CtfProblem.objects.filter(**{PK_FIELD: problem_id})
            # create the directories we'd copy static files to and from
            static_from = join(BASEDIR, root, 'static')
            static_to = join(STATIC_BASE, root, 'static')
            try:
                if PK_FIELD in data and query.exists():
                    write("Trying to update problem for '{}'".format(root))
                    query.update(**data)
                    for problem in query:
                        problem.save()
                    if isdir(static_from):
                        write("Warning: Deleting existing staticfiles at '{}'".format(static_to))
                        shutil.rmtree(static_from)

                # Otherwise, create a new one
                else:
                    write("Trying to create problem for '{}'".format(root))
                    problem = CtfProblem(**data)
                    problem.save()
                    write('Writing .uuid file in problem directory.')
                    with open(uuid_file, 'w') as f:
                        f.write(str(problem.id))

                if isdir(static_from):
                    write("Trying to copy static files from '{}'".format(static_from))
                    shutil.copytree(static_from, static_to)

            # Output success or failure
            except ValidationError:
                write("Validation failed for '{}'".format(root))
                errors.append(sys.exc_info())
                continue
            except (shutil.Error, IOError):
                write("Unable to copy static files for '{}'".format(root))
                errors.append(sys.exc_info())
                continue
            else:
                write("Successfully imported problem for '{}'".format(root))

        # Print stacktraces from before
        if errors:
            write("\nPrinting stacktraces of encountered exceptions")
            for err in errors:
                write(''.join(traceback.format_exception(*err)))
