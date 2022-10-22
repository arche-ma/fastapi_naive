import strawberry


@strawberry.input
class UserInput:
    password: str
    username: str


@strawberry.type
class TokenType:
    token: str


@strawberry.type
class UserNotFound:
    message: str = "User not found"


@strawberry.type
class AuthenticationFailed:
    message: str = "Authentication failed, try again"


UserAuthResponse = strawberry.union(
    "UserAuthResponse", [TokenType, UserNotFound, AuthenticationFailed]
)
