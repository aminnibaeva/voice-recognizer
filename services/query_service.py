from repositories.users_query_repository import UsersQueryRepository

users_query_repository = UsersQueryRepository()


class QueryService:
    def update_query(self, user_query_id):
        users_query_repository.update_user_query_by_user_query_id(user_query_id)

    def delete_query(self, user_query_id):
        users_query_repository.delete_user_query_by_user_query_id(user_query_id)
