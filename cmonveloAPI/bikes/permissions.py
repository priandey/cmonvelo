from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    message = "Vous devez être propriétaire de ce vélo pour pouvoir en modifier les attributs ou le supprimer"

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user


class IsInstitution(permissions.BasePermission):
    message = "Votre compte n'a pas la permission d'accéder à cette ressource. " \
              "Si vous êtes une institution, merci de contacter un administrateur du service"

    def has_permission(self, request, view):
        return request.user.is_institution
