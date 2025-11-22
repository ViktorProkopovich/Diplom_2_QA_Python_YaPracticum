class TextResponse:
    # =============== Пользователь ===============
    USER_ALREADY_EXISTS = "User already exists"
    EMAIL_IS_BUSYU = "User with such email already exists"
    REQUIRED_FIELDS = "Email, password and name are required fields"
    INCORRECT_CREDENTIALS = "email or password are incorrect"
    USER_CREATED_SUCCESSFULLY = "User created successfully"
    SUCCESSFUL_LOGOUT = "Successful logout"

    # =============== Заказы ===============
    NO_INGREDIENT_IDENTIFIERS = "Ingredient ids must be provided"
    ORDER_INVALID_HASH = "Internal Server Error"
    NO_AUTHORIZATION = "You should be authorised"

    # =============== Пароль ===============
    RESET_EMAIL_OK = "Reset email sent"
    RESET_PASS_OK = "Password successfully reset"
    