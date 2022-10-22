from typing import Any, Awaitable, Union

from strawberry.permission import BasePermission
from strawberry.types import Info

from auth import validate_token


class AdminPermission(BasePermission):
    message = "User doesn't have enough rights to perform this action"

    def has_permission(
        self, source: Any, info: Info, **kwargs
    ) -> Union[bool, Awaitable[bool]]:
        authorization = info.context["request"].headers.get(
            "authorization", None
        )
        if not authorization:
            return False
        is_admin = False
        if authorization:
            payload = validate_token(authorization.split()[1])
            is_admin = payload.get("admin", False)
            if "error" in payload.keys():
                self.message = payload["error"]
        return is_admin
