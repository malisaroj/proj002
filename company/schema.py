import graphene
from graphene_django import DjangoObjectType
from .models import *


class CityNode(DjangoObjectType):
    class Meta:
        model = City


class TitleNode(DjangoObjectType):
    class Meta:
        model = Title


class EmployeeNode(DjangoObjectType):
    class Meta:
        model = Employee


class Query(object):
    all_cities = graphene.List(CityNode)

    all_titles = graphene.List(TitleNode)

    all_employees = graphene.List(EmployeeNode)

    def resolve_all_cities(self, info, **kwargs):
        return City.objects.all()

    def resolve_all_titles(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return Title.objects.all()

    def resolve_all_employees(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return Employee.objects.all()


class CreateTitle(graphene.Mutation):
    # The class attributes define the response of the mutation
    title = graphene.Field(TitleNode)

    class Input:
        title_name = graphene.String()

    def mutate(self, info, **input):
        title = Title(
            title_name=input.get('title_name')
        )
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')        
        title.save()
        # Notice we return an instance of this mutation
        return CreateTitle(title=title)


class CreateEmployee(graphene.Mutation):
    employee = graphene.Field(EmployeeNode)

    class Input:
        employee_name = graphene.String()
        employee_city = graphene.String()
        employee_title = graphene.String()

    def mutate(self, info, **input):
        employee = Employee(
            employee_name=input.get('employee_name'),
            employee_city=City.objects.get(
                city_name=input.get('employee_city')),
            employee_title=Title.objects.get(
                title_name=input.get('employee_title'))
        )
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        employee.save()
        # Notice we return an instance of this mutation
        return CreateEmployee(employee=employee)


class UpdateEmployee(graphene.Mutation):
    employee = graphene.Field(EmployeeNode)

    class Input:
        id = graphene.String()
        employee_name = graphene.String()
        employee_city = graphene.String()
        employee_title = graphene.String()

    def mutate(self, info, **input):
        employee = Employee.objects.get(
            pk=(input.get('id')))
        employee.employee_name = input.get('employee_name')
        employee.employee_city = City.objects.get(
            city_name=input.get('employee_city'))
        employee.employee_title = Title.objects.get(
            title_name=input.get('employee_title')
        )
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        employee.save()
        return UpdateEmployee(employee=employee)

class DeleteEmployee(graphene.Mutation):
    employee = graphene.Field(EmployeeNode)    
    
    class Input:
        id = graphene.String()    
    def mutate(self, info, **input):
        employee = Employee.objects.get(
            pk=(input.get('id')))
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        employee.delete()        
        return DeleteEmployee(employee=employee)


class Mutation(graphene.ObjectType):
    create_title = CreateTitle.Field()
    create_employee = CreateEmployee.Field()
    update_employee = UpdateEmployee.Field()
    delete_employee = DeleteEmployee.Field()
