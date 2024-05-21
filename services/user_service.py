from repositories.application_repository import ApplicationRepository
from repositories.page_repository import PageRepository
from repositories.user_repository import UsersRepository
from repositories.users_query_repository import UsersQueryRepository

users_repository = UsersRepository()
application_repository = ApplicationRepository()
page_repository = PageRepository()
users_query_repository = UsersQueryRepository()


class UserService:
    def save_user_query(self, username, application_id, page_name):
        user_id = users_repository.get_user_id_by_username(username)
        is_user_query_exists = users_query_repository.is_user_query_exists(user_id, page_name)

        if is_user_query_exists:
            users_query_repository.update_user_query_by_user_id_and_query(application_id, user_id, page_name)
        else:
            users_query_repository.save_user_query(application_id, user_id, page_name,
                                                   page_repository.get_page_url_by_application_id_and_page_name(
                                                       application_id, page_name),
                                                   application_repository.get_application_url_by_id(application_id))
