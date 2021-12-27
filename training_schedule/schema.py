import graphene
from main import schema
from graphql_auth.schema import MeQuery


class Mutation(schema.Mutation, schema.AuthMutation, graphene.ObjectType):
    pass


class Query(schema.Query, MeQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
