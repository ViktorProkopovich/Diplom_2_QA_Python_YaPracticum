class Endpoints:
    BASE_URL = "https://stellarburgers.education-services.ru"

    # =============== Ингредиенты ===============
    GET_INGREDIENTS = f"{BASE_URL}/api/ingredients" # GET

    # =============== Заказы ===============
    CREATE_ORDER = f"{BASE_URL}/api/orders" # POST — создать заказ

    # =============== Пользователь ===============
    REGISTER = f"{BASE_URL}/api/auth/register" # POST
    LOGIN = f"{BASE_URL}/api/auth/login" # POST
    LOGOUT = f"{BASE_URL}/api/auth/logout" # POST
    TOKEN_REFRESH = f"{BASE_URL}/api/auth/token" # POST

    # Один URL для всех операций с пользователем
    USER = f"{BASE_URL}/api/auth/user" # GET / PATCH / DELETE

    # =============== Пароль ===============
    PASSWORD_RESET = f"{BASE_URL}/api/password-reset" # POST