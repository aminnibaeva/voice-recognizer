from repositories.application_repositoty import ApplicationRepository
from repositories.user_repository import UsersRepository
from repositories.users_application_repository import UsersApplicationRepository
from repositories.users_query_repository import UsersQueryRepository

users_repository = UsersRepository()
users_application_repository = UsersApplicationRepository()
application_repository = ApplicationRepository()
users_query_repository = UsersQueryRepository()


class UserService:
    def save_user_query(self, username, token, query):
        user_id = users_repository.get_user_id_by_username(username)

        application_id = application_repository.get_application_id_by_token(token)
        is_user_exists = users_application_repository.is_user_application_exists(user_id, application_id)

        if not is_user_exists:
            users_application_repository.save_into_users_application(user_id, application_id)

        users_query_repository.save_user_query(user_id, query)
