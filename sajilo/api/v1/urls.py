from django.urls import include, path

app_name = "api_v1"

urlpatterns = [
    path(
        "users/", 
        include("sajilo.users.api.v1.urls", namespace="users"),
    ),
    # path(
    #     "core/",
    #     include("sajilo.core.api.v1.urls", namespace="core"),
    # ),
]
