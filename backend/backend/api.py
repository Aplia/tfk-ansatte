from django.db.models import Prefetch
from rest_framework import routers, viewsets
from rest_framework import serializers
from rest_framework.response import Response
from backend.models import Person, Position, Department


def search_string(request):
    q = request.GET.get('q', '').strip()
    if q and len(q) >= 2:
        return q
    elif q:
        return False
    else:
        return None


# Person API

class PersonDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name')


class PersonPositionSerializer(serializers.ModelSerializer):
    department = PersonDepartmentSerializer(many=False, read_only=True)

    class Meta:
        model = Position
        fields = ('id', 'info', 'department', )


class PersonSerializer(serializers.ModelSerializer):
    positions = PersonPositionSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = (
            'id', 'given_name', 'family_name', 'email', 'mobile_phone', 'work_phone',
            'positions'
        )


class PersonViewSet(viewsets.ModelViewSet):
    """ API endpoint for Persons

    Available paramters:
        * `?q`: Search firstname and lastname (like search)
        * `?department_id`: List or search firstname/lastname a specific department
    """
    queryset = Person.objects.prefetch_related('positions__department').all()
    serializer_class = PersonSerializer

    def get_queryset(self):
        qs = self.queryset
        department_id = self.request.GET.get('department_id', None)

        if department_id:
            qs = qs.filter(positions__department_id=department_id)

        term = search_string(self.request)
        if term:
            return Person.search(qs, term)
        elif department_id:
            return qs
        else:
            return []


# Department API

class DepartmentPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = (
            'id', 'given_name', 'family_name', 'email', 'mobile_phone', 'work_phone',
        )


class DepartmentPositionSerializer(serializers.ModelSerializer):
    person = DepartmentPersonSerializer(many=False, read_only=True)

    class Meta:
        model = Position
        fields = ('id', 'info', 'person')


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name')


class DepartmentWithPositionsSerializer(serializers.ModelSerializer):
    positions = DepartmentPositionSerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = ('id', 'name', 'positions')


class DepartmentViewSet(viewsets.ModelViewSet):
    """ API endpoint for Departments

    Available paramters:
        * `?q`: Search name of departments (like search)
        * `/department_id/?q`: Search firstname, lastname of department employees (like search)
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        qs = self.queryset

        term = search_string(self.request)
        if term:
            return Department.search(qs, term)
        else:
            return qs

    def retrieve(self, request, pk=None):
        qs = Department.objects.all()
        term = search_string(request)
        qs = self.queryset

        if term:
            qs = Department.objects.prefetch_related(
                Prefetch(
                    'positions',
                    queryset=Position.search(Position.objects.all(), term)
                ),
                'positions__person',
            )

        department = qs.get(pk=pk)
        serializer = DepartmentWithPositionsSerializer(department)
        return Response(serializer.data)


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'departments', DepartmentViewSet)
router.register(r'people', PersonViewSet)
