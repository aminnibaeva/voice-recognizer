import re

from repositories.filter_repository import FilterRepository

filter_repository = FilterRepository()


class FilterService:
    def get_filters(self, application_id, text):
        text = text.lower()
        filters = filter_repository.get_filter_names_by_application_id(application_id)

        current_filter = None
        current_filter_type = None
        current_element = {}
        result = []
        text_starts_with_filter = False

        while text != '':
            for filter in filters:
                if text.startswith(filter[0].lower()):
                    if current_element != {}:
                        result.append(current_element)
                    current_element = {}
                    text_starts_with_filter = True
                    current_filter = filter[0]
                    current_filter_type = filter[1]
                    break
            if text_starts_with_filter:
                text_starts_with_filter = False
                text = text[len(current_filter) + 1:]
                current_element['filterName'] = current_filter
                current_element['filterType'] = current_filter_type
                if current_filter_type == 'TOGGLE':
                    current_element['filter'] = True
                else:
                    current_element['filter'] = []
            else:
                word = text.split(" ")[0]
                text = text[len(word) + 1:]
                if current_filter_type == 'RANGE':
                    word = re.findall(r'\b\d+\b', word)
                    if word != "" and word != []:
                        current_element['filter'].append(int(''.join(word)))
                        current_element['filter'].sort()
                else:
                    current_element['filter'].append(word)

        if current_element != {} and result.__contains__(current_element) == False:
            result.append(current_element)

        return result
