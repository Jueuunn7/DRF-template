from core.exceptions import BaseCustomException


class AccountException:
    LoginFailException = BaseCustomException(code=400, detail='Fail to login')
