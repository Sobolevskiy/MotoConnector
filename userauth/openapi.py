from drf_yasg import openapi

from userauth.serializers import VerifyEmailResponseSerializer

registration_response_schema_dict = {
    "201": openapi.Response(
        description='Пользователь успешно зарегистрирован',
        examples={
            "application/json": {
                "success": True,
                "msg": "Verification code sent",
                "user_id": 1
            }
        }
    ),
    "400": openapi.Response(
        description="Ошибки валидации параметров",
    ),
    "403": openapi.Response(
        description='Пользователь с такой почтой уже создан',
        examples={
            "application/json": {
                "user_id": 1,
                "verified": True,
                "msg": "User with this email already exists"
            }
        }
    )
}

verify_email_response_schema_dict = {
    "200": openapi.Response(
        description='Успешная верификация',
        schema=VerifyEmailResponseSerializer,
        examples={
            "application/json": {
                "success": True,
                "msg": "User verified",
            }
        }
    ),
    "400": openapi.Response(
        description="Не хватает параметров",
        examples={
            "application/json": {
                "token": ["This field is required."]
            }
        }
    ),
    "403": openapi.Response(
        description="Ошибка валидации токена",
        schema=VerifyEmailResponseSerializer,
        examples={
            "application/json": {
                "success": False,
                "msg": "Invalid code",
            }
        }
    ),
}


resend_email_response_schema_dict = {
    "200": openapi.Response(
        description='Успешная переотправка',
    ),
    "400": openapi.Response(
        description="Не хватает параметров",
        examples={
            "application/json": {
                "user_id": [
                    "This field is required."
                ]
            }
        }
    ),
}
