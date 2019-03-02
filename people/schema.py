from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.conf import settings

from graphql_jwt.utils import jwt_decode
import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from .models import Guardian, Teacher, Student, Subject, ClassRoom


# User
class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    @login_required
    def mutate(self, info, username, email, password):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class UpdateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        id = graphene.Int(required=True)
        username = graphene.String()
        email = graphene.String()
        password = graphene.String()

    @login_required
    def mutate(self, info, id, username=None, email=None, password=None):
        user = get_user_model().objects.get(pk=id)
        if username and username != user.username:
            user.username = username
        if email and email != user.email:
            user.email = email
        if password:
            user.set_password(password)

        user.save()

        return UpdateUser(user=user)


class DeleteUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        id = graphene.Int(required=True)

    @login_required
    def mutate(self, info, id):
        user = get_user_model().objects.get(pk=id)
        try:
            user.delete()
        except Exception as err:
            raise GraphQLError(f"Error! {str(err)}")

        return DeleteUser(user=user)


# Guardian
class GuardianType(DjangoObjectType):
    class Meta:
        model = Guardian


class CreateGuardian(graphene.Mutation):
    guardian = graphene.Field(GuardianType)

    class Arguments:
        full_name = graphene.String(required=True)
        id_number = graphene.Int(required=True)
        phone = graphene.Int(required=True)
        email = graphene.String()
        religion = graphene.String()
        gender = graphene.String()
        profession = graphene.String()
        DOB = graphene.Date()
        active = graphene.Boolean()

    @login_required
    def mutate(self,
               info,
               full_name,
               id_number,
               phone,
               email=None,
               religion=None,
               gender=None,
               profession=None,
               DOB=None,
               active=None):

        try:
            guardian = Guardian.objects.create(
                full_name=full_name,
                id_number=id_number,
                phone=phone,
                email=email,
                religion=religion,
                gender=gender,
                profession=profession,
                DOB=DOB,
                active=active)
        except Exception as err:
            raise GraphQLError(f"Error! {str(err)}")

        return CreateGuardian(guardian=guardian)


class UpdateGuardian(graphene.Mutation):
    guardian = graphene.Field(GuardianType)

    class Arguments:
        id = graphene.Int(required=True)
        full_name = graphene.String()
        id_number = graphene.Int()
        phone = graphene.Int()
        email = graphene.String()
        religion = graphene.String()
        gender = graphene.String()
        profession = graphene.String()
        DOB = graphene.Date()
        active = graphene.Boolean()

    @login_required
    def mutate(self, info, id, **kwargs):
        try:
            Guardian.objects.filter(pk=id).update(**kwargs)
            guardian = Guardian.objects.get(pk=id)
        except Exception as err:
            raise GraphQLError(f"Error! {str(err)}")

        return UpdateGuardian(guardian=guardian)


class DeleteGuardian(graphene.Mutation):
    guardian = graphene.Field(GuardianType)

    class Arguments:
        id = graphene.Int(required=True)

    @login_required
    def mutate(self, info, id):
        guardian = Guardian.objects.get(pk=id)
        try:
            guardian.delete()
        except Exception as err:
            raise GraphQLError(f"Error! {str(err)}")

        return DeleteGuardian(guardian=guardian)


# Teacher
class TeacherType(DjangoObjectType):
    class Meta:
        model = Teacher


class CreateTeacher(graphene.Mutation):
    teacher = graphene.Field(TeacherType)

    class Arguments:
        full_name = graphene.String(required=True)
        id_number = graphene.Int(required=True)
        phone = graphene.Int(required=True)
        email = graphene.String()
        religion = graphene.String()
        gender = graphene.String()
        subjects = graphene.List(graphene.Int)
        joined_at = graphene.Date()
        DOB = graphene.Date()
        active = graphene.Boolean()

    @login_required
    def mutate(self,
               info,
               full_name,
               id_number,
               phone,
               email=None,
               religion=None,
               gender=None,
               subjects=None,
               joined_at=None,
               DOB=None,
               active=None):

        try:
            teacher = Teacher.objects.create(
                full_name=full_name,
                id_number=id_number,
                phone=phone,
                email=email,
                religion=religion,
                gender=gender,
                joined_at=joined_at,
                DOB=DOB,
                active=active)

            if subjects:
                for pk in subjects:
                    subject = Subject.objects.get(pk=pk)
                    teacher.subjects.add(subject)
        except Exception as err:
            raise GraphQLError(f"Error! {str(err)}")

        return CreateTeacher(teacher=teacher)


class UpdateTeacher(graphene.Mutation):
    teacher = graphene.Field(TeacherType)

    class Arguments:
        id = graphene.Int(required=True)
        full_name = graphene.String()
        id_number = graphene.Int()
        phone = graphene.Int()
        email = graphene.String()
        religion = graphene.String()
        gender = graphene.String()
        subjects = graphene.List(graphene.Int)
        joined_at = graphene.String()
        DOB = graphene.Date()
        active = graphene.Boolean()

    @login_required
    def mutate(self, info, id, **kwargs):
        try:
            subjects = kwargs.pop('subjects')

            Teacher.objects.filter(pk=id).update(**kwargs)
            teacher = Teacher.objects.get(pk=id)

            if subjects:
                for pk in subjects:
                    subject = Subject.objects.get(pk=pk)
                    teacher.subjects.add(subject)

        except Exception as err:
            raise GraphQLError(f"Error! {str(err)}")

        return UpdateTeacher(teacher=teacher)


class DeleteTeacher(graphene.Mutation):
    teacher = graphene.Field(TeacherType)

    class Arguments:
        id = graphene.Int(required=True)

    @login_required
    def mutate(self, info, id):
        teacher = Teacher.objects.get(pk=id)
        try:
            teacher.delete()
        except Exception as err:
            raise GraphQLError(f"Error! {str(err)}")

        return DeleteTeacher(teacher=teacher)


# Student
class StudentType(DjangoObjectType):
    class Meta:
        model = Student


class CreateStudent(graphene.Mutation):
    student = graphene.Field(StudentType)

    class Arguments:
        full_name = graphene.String(required=True)
        class_room = graphene.Int(required=True)
        phone = graphene.Int(required=True)
        registration_number = graphene.Int()
        email = graphene.String()
        religion = graphene.String()
        gender = graphene.String()
        guardians = graphene.List(graphene.Int)
        joined_at = graphene.Date()
        DOB = graphene.Date()
        active = graphene.Boolean()

    @login_required
    def mutate(self,
               info,
               full_name,
               class_room,
               phone,
               email=None,
               registration_number=None,
               religion=None,
               gender=None,
               guardians=None,
               joined_at=None,
               DOB=None,
               active=None):

        try:
            class_room = ClassRoom.objects.get(pk=class_room)
            student = Student.objects.create(
                full_name=full_name,
                class_room=class_room,
                phone=phone,
                email=email,
                registration_number=registration_number,
                religion=religion,
                gender=gender,
                joined_at=joined_at,
                DOB=DOB,
                active=active)

            if guardians:
                for pk in guardians:
                    guardian = Guardian.objects.get(pk=pk)
                    student.guardians.add(guardian)

        except Exception as err:
            raise GraphQLError(f"Error! {str(err)}")

        return CreateStudent(student=student)


class UpdateStudent(graphene.Mutation):
    student = graphene.Field(StudentType)

    class Arguments:
        id = graphene.Int(required=True)
        full_name = graphene.String()
        class_room = graphene.Int()
        phone = graphene.Int()
        email = graphene.String()
        registration_number = graphene.Int()
        religion = graphene.String()
        gender = graphene.String()
        guardians = graphene.List(graphene.Int)
        joined_at = graphene.String()
        DOB = graphene.Date()
        active = graphene.Boolean()

    @login_required
    def mutate(self, info, id, **kwargs):
        try:
            if kwargs["class_room"]:
                # update class_room from an id (int) to an object
                kwargs["class_room"] = ClassRoom.objects.get(pk=kwargs["class_room"])  # noqa E501

            guardians = kwargs.pop('guardians')

            Student.objects.filter(pk=id).update(**kwargs)
            student = Student.objects.get(pk=id)

            if guardians:
                for pk in guardians:
                    guardian = Guardian.objects.get(pk=pk)
                    student.guardians.add(guardian)

        except Exception as err:
            raise GraphQLError(f"Error! {str(err)}")

        return UpdateStudent(student=student)


class DeleteStudent(graphene.Mutation):
    student = graphene.Field(StudentType)

    class Arguments:
        id = graphene.Int(required=True)

    @login_required
    def mutate(self, info, id):
        student = Student.objects.get(pk=id)
        try:
            student.delete()
        except Exception as err:
            raise GraphQLError(f"Error! {str(err)}")

        return DeleteStudent(student=student)


# Subject
class SubjectType(DjangoObjectType):
    class Meta:
        model = Subject


class CreateSubject(graphene.Mutation):
    subject = graphene.Field(SubjectType)

    class Arguments:
        name = graphene.String(required=True)

    @login_required
    def mutate(self, info, name):

        try:
            subject = Subject.objects.create(name=name)
        except Exception as err:
            raise GraphQLError(f"Error! {str(err)}")

        return CreateSubject(subject=subject)


class UpdateSubject(graphene.Mutation):
    subject = graphene.Field(SubjectType)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()

    @login_required
    def mutate(self, info, id, **kwargs):
        try:
            Subject.objects.filter(pk=id).update(**kwargs)
            subject = Subject.objects.get(pk=id)
        except Exception as err:
            raise GraphQLError(f"Error! {str(err)}")

        return UpdateSubject(subject=subject)


class DeleteSubject(graphene.Mutation):
    subject = graphene.Field(SubjectType)

    class Arguments:
        id = graphene.Int(required=True)

    @login_required
    def mutate(self, info, id):
        subject = Subject.objects.get(pk=id)
        try:
            subject.delete()
        except Exception as err:
            raise GraphQLError(f"Error! {str(err)}")

        return DeleteSubject(subject=subject)


# ClassRoom
class ClassRoomType(DjangoObjectType):
    class Meta:
        model = ClassRoom


class CreateClassRoom(graphene.Mutation):
    class_room = graphene.Field(ClassRoomType)

    class Arguments:
        name = graphene.String(required=True)
        class_teacher = graphene.Int(required=True)

    @login_required
    def mutate(self, info, name, class_teacher):

        try:
            class_teacher = Teacher.objects.get(pk=class_teacher)
            class_room = ClassRoom.objects.create(
                name=name, class_teacher=class_teacher)
        except Exception as err:
            raise GraphQLError(f"Error! {str(err)}")

        return CreateClassRoom(class_room=class_room)


class UpdateClassRoom(graphene.Mutation):
    class_room = graphene.Field(ClassRoomType)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        class_teacher = graphene.Int()

    @login_required
    def mutate(self, info, id, **kwargs):
        try:
            ClassRoom.objects.filter(pk=id).update(**kwargs)
            class_room = ClassRoom.objects.get(pk=id)
        except Exception as err:
            raise GraphQLError(f"Error! {str(err)}")

        return UpdateClassRoom(class_room=class_room)


class DeleteClassRoom(graphene.Mutation):
    class_room = graphene.Field(ClassRoomType)

    class Arguments:
        id = graphene.Int(required=True)

    @login_required
    def mutate(self, info, id):
        class_room = ClassRoom.objects.get(pk=id)
        try:
            class_room.delete()
        except Exception as err:
            raise GraphQLError(f"Error! {str(err)}")

        return DeleteClassRoom(class_room=class_room)


class Query(graphene.ObjectType):
    user = graphene.Field(
        UserType,
        id=graphene.Int(required=True),
    )

    users = graphene.List(
        UserType,
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )
    current_user = graphene.Field(UserType, token=graphene.String())

    guardian = graphene.Field(
        GuardianType,
        id=graphene.Int(required=True),
    )

    # pagination
    # first - returns the first n items, skip - skips the first n items.
    guardians = graphene.List(
        GuardianType,
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )

    teacher = graphene.Field(
        TeacherType,
        id=graphene.Int(required=True),
    )

    teachers = graphene.List(
        TeacherType,
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )

    student = graphene.Field(
        StudentType,
        id=graphene.Int(required=True),
    )

    students = graphene.List(
        StudentType,
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )

    subject = graphene.Field(
        SubjectType,
        id=graphene.Int(required=True),
    )

    subjects = graphene.List(
        SubjectType,
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )

    class_room = graphene.Field(
        ClassRoomType,
        id=graphene.Int(required=True),
    )

    class_rooms = graphene.List(
        ClassRoomType,
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )

    @login_required
    def resolve_user(self, info, id, **kwargs):
        return get_object_or_404(get_user_model(), pk=id)

    @login_required
    def resolve_users(self, info, search=None, first=None, skip=None,
                      **kwargs):

        qs = get_user_model().objects.all()
        if search:
            filter = (Q(username__icontains=search)
                      | Q(email__icontains=search)
                      | Q(first_name__icontains=search)
                      | Q(last_name__icontains=search))

            qs = qs.filter(filter)

        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        return qs

    def resolve_current_user(self, info, token=None, **kwargs):
        if token:
            try:
                decoded = jwt_decode(token)
                username = decoded['username']
                user = get_user_model().objects.get(username=username)
                return user
            except Exception as err:
                raise GraphQLError(f"Error! Please ensure that your token is valid. {str(err)}")  # noqa E501

        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Not logged in and user token not provided!")
        return user

    @login_required
    def resolve_guardian(self, info, id, **kwargs):
        return get_object_or_404(Guardian, pk=id)

    @login_required
    def resolve_guardians(self,
                          info,
                          search=None,
                          first=None,
                          skip=None,
                          **kwargs):
        qs = Guardian.objects.all()
        if search:
            filter = (Q(full_name__icontains=search)
                      | Q(phone__icontains=search)
                      | Q(email__icontains=search)
                      | Q(gender__icontains=search)
                      | Q(id_number__icontains=search)
                      | Q(profession__icontains=search)
                      | Q(DOB__icontains=search))

            qs = qs.filter(filter)

        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        return qs

    @login_required
    def resolve_teacher(self, info, id, **kwargs):
        return get_object_or_404(Teacher, pk=id)

    @login_required
    def resolve_teachers(self,
                         info,
                         search=None,
                         first=None,
                         skip=None,
                         **kwargs):
        qs = Teacher.objects.all()
        if search:
            filter = (Q(full_name__icontains=search)
                      | Q(phone__icontains=search)
                      | Q(email__icontains=search)
                      | Q(gender__icontains=search)
                      | Q(id_number__icontains=search)
                      | Q(subjects__icontains=search)
                      | Q(joined_at__icontains=search)
                      | Q(DOB__icontains=search))

            qs = qs.filter(filter)

        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        return qs

    @login_required
    def resolve_student(self, info, id, **kwargs):
        return get_object_or_404(Student, pk=id)

    @login_required
    def resolve_students(self,
                         info,
                         search=None,
                         first=None,
                         skip=None,
                         **kwargs):
        qs = Student.objects.all()
        if search:
            filter = (Q(full_name__icontains=search)
                      | Q(phone__icontains=search)
                      | Q(email__icontains=search)
                      | Q(registration_number__icontains=search)
                      | Q(class_room__icontains=search)
                      | Q(gender__icontains=search)
                      | Q(guardians__full_name__icontains=search)
                      | Q(guardians__id_number__icontains=search)
                      | Q(joined_at__icontains=search)
                      | Q(DOB__icontains=search))

            qs = qs.filter(filter)

        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        return qs

    @login_required
    def resolve_subject(self, info, id, **kwargs):
        return get_object_or_404(Subject, pk=id)

    @login_required
    def resolve_subjects(self,
                         info,
                         search=None,
                         first=None,
                         skip=None,
                         **kwargs):
        qs = Subject.objects.all()
        if search:
            filter = (Q(name__icontains=search))

            qs = qs.filter(filter)

        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        return qs

    @login_required
    def resolve_class_room(self, info, id, **kwargs):
        return get_object_or_404(ClassRoom, pk=id)

    @login_required
    def resolve_class_rooms(self,
                            info,
                            search=None,
                            first=None,
                            skip=None,
                            **kwargs):
        qs = ClassRoom.objects.all()
        if search:
            filter = (Q(name__icontains=search)
                      | Q(class_teacher__full_name__icontainss=search))

            qs = qs.filter(filter)

        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        return qs


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

    create_guardian = CreateGuardian.Field()
    update_guardian = UpdateGuardian.Field()
    delete_guardian = DeleteGuardian.Field()

    create_teacher = CreateTeacher.Field()
    update_teacher = UpdateTeacher.Field()
    delete_teacher = DeleteTeacher.Field()

    create_student = CreateStudent.Field()
    update_student = UpdateStudent.Field()
    delete_student = DeleteStudent.Field()

    create_subject = CreateSubject.Field()
    update_subject = UpdateSubject.Field()
    delete_subject = DeleteSubject.Field()

    create_class_room = CreateClassRoom.Field()
    update_class_room = UpdateClassRoom.Field()
    delete_class_room = DeleteClassRoom.Field()
