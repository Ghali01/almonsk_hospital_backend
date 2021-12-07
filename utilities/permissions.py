from rest_framework.permissions import BasePermission
class MainPermission(BasePermission):
    __TOKEN='EGRTgrGRTfrgHGNGNYexgegG3N656J4Y5TYJ5RTEX6ukW2R6VBTedgfgfNYBTFR125DT55FE7486sf5SRDAESQXsf6755CVBfhbKHYsf5TREXZ96W6fwf6Q26d3egWukEGUY'


    def has_permission(self, request, view):
        return request.headers['token'] == self.__TOKEN
        