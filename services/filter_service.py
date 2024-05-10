import re

from repositories.filter_repository import FilterRepository

filter_repository = FilterRepository()


class FilterService:
    def get_filters(self, application_id, text):
        text = text.lower()
        categories = filter_repository.get_filter_names_by_application_id(application_id)

        current_category = None
        current_category_type = None
        current_element = {}
        result = []
        text_starts_with_category = False

        while text != '':
            for category in categories:
                if text.startswith(category[0]):
                    if current_element != {}:
                        result.append(current_element)
                    current_element = {}
                    text_starts_with_category = True
                    current_category = category[0]
                    current_category_type = category[1]
                    break
            if text_starts_with_category:
                text_starts_with_category = False
                text = text[len(current_category) + 1:]
                current_element['filterName'] = current_category
                current_element['filterType'] = current_category_type
                if current_category_type == 'TOGGLE':
                    current_element['filter'] = True
                else:
                    current_element['filter'] = []
            else:
                word = text.split(" ")[0]
                text = text[len(word) + 1:]
                if current_category_type == 'RANGE':
                    word = re.findall(r'\b\d+\b', word)
                    if word != "" and word != []:
                        current_element['filter'].append(int(''.join(word)))
                        current_element['filter'].sort()
                else:
                    current_element['filter'].append(word)

        if current_element != {} and result.__contains__(current_element) == False:
            result.append(current_element)

        return result
