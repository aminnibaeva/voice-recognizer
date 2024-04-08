from repositories.application_repository import ApplicationRepository

application_repository = ApplicationRepository()


class ApplicationService:
    def get_language_by_application_id(self, token):
        return application_repository.get_language_by_application_id(token)
