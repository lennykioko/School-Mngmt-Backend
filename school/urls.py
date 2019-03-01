from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView


admin.site.site_header = 'SCHOOL MANAGEMENT'
admin.site.site_title = 'SCHOOL MANAGEMENT'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
