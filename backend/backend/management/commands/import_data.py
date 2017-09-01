import os
import codecs
import json
from django.core.management.base import BaseCommand
from backend.models import Person, Position, Department


class Command(BaseCommand):
    help = 'Import JSON data'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help="Path to json file")

    def handle(self, *args, **options):
        file = options['file']
        assert os.path.exists(file), "File '%s' does not exist" % file

        Position.objects.all().delete()
        Person.objects.all().delete()
        Department.objects.all().delete()

        with open(file, 'rb') as file:
            reader = codecs.getreader("utf-8")
            json_data = json.load(reader(file))
            for result in json_data['results']:
                person = Person.objects.create(
                    given_name=result['givenName'],
                    family_name=result['familyName'],
                    email=result['email'],
                    mobile_phone=result['mobilePhone'],
                    work_phone=result['workPhone'],
                )
                for position in result['positions']:
                    if not position['departmentName']:
                        continue
                    (department, _) = Department.objects.get_or_create(
                        id=position['departmentId'],
                        name=position['departmentName']
                    )
                    Position.objects.create(
                        info=position['info'],
                        type=position['type'],
                        department=department,
                        person=person,
                    )
