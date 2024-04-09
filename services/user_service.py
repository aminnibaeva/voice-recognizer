from repositories.application_repository import ApplicationRepository
from repositories.user_repository import UsersRepository
from repositories.users_query_repository import UsersQueryRepository

users_repository = UsersRepository()
application_repository = ApplicationRepository()
users_query_repository = UsersQueryRepository()


class UserService:
    def save_user_query(self, username, application_id, query):
        user_id = users_repository.get_user_id_by_username(username)

        is_user_query_exists = users_query_repository.is_user_query_exists(user_id, query)

        if is_user_query_exists:
            users_query_repository.update_user_query_by_user_id_and_query(application_id, user_id, query)
        else:
            users_query_repository.save_user_query(application_id, user_id, query)
