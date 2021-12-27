import graphene
from graphene_django import DjangoObjectType
from .models import Workout
from graphene_django.filter import DjangoFilterConnectionField
from graphql_auth import mutations
from graphql_jwt.decorators import superuser_required


class WorkoutType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = Workout
        fields = ('id', 'title', 'time')
        filter_fields = {
            'time': ["lte", "gte", "exact"],
        }
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    workout = graphene.Field(WorkoutType, id=graphene.Int())
    workouts = DjangoFilterConnectionField(WorkoutType)
    workouts_in_range = graphene.List(
        WorkoutType,
        required=True,
        start_time_offset=graphene.DateTime(required=True),
        end_time_offset=graphene.DateTime(required=True)
    )

    def resolve_workout(self, info, **kwargs):
        id = kwargs.get('id', None)

        try:
            return Workout.objects.get(pk=id)
        except Exception as e:
            print(e)
            return None

    def resolve_workouts(self, info, **kwargs):
        try:
            return Workout.objects.all()
        except Exception as e:
            print(e)
            return None

    def resolve_workouts_in_range(self, info, start_time_offset, end_time_offset):
        print(start_time_offset)
        try:
            return Workout.objects.filter(time__range=(start_time_offset, end_time_offset))
        except Exception as e:
            print(e)
            return None


class WorkoutInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    time = graphene.DateTime()


class CreateWorkoutMutation(graphene.Mutation):
    class Arguments:
        input = WorkoutInput()
    ok = graphene.Boolean()
    workout = graphene.Field(WorkoutType)

    @classmethod
    @superuser_required
    def mutate(cls, root, info, input=None):
        superuser = info.context.user.is_superuser
        ok = False
        try:
            workout_instance = Workout.objects.create(title=input.title, time=input.time)
            return cls(ok=ok, workout=workout_instance)
        except Exception as e:
            print(e)
            return cls(ok=False, workout=None)


class UpdateWorkoutMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = WorkoutInput(required=True)

    ok = graphene.Boolean()
    workout = graphene.Field(WorkoutType)

    @classmethod
    @superuser_required
    def mutate(cls, root, info, id, input=None):
        superuser = info.context.user.is_superuser
        ok = False
        try:
            workout_instance = Workout.objects.get(pk=id)
        except Workout.DoesNotExist:
            return cls(ok=ok, workout=None)

        if workout_instance:
            ok = True
            workout_instance.title = input.title
            workout_instance.time = input.time
            workout_instance.save()
            return cls(ok=ok, workout=workout_instance)
        return cls(ok=ok, workout=None)


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()


class Mutation(graphene.ObjectType):
    create_workout = CreateWorkoutMutation.Field()
    update_workout = UpdateWorkoutMutation.Field()
