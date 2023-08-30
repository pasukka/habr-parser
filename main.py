# -*- coding: utf-8 -*-
import parse_habr as ph

# ------- exapmle for one page -------
if __name__ == "__main__":
    number = 692272
    txt_path = './'
    html_path = './'
    list_of_keywords = ['Natural Language Processing', 'Artificial Intelligence',
                        'Искусственный интеллект']
    dict_of_keywords = {'Data Mining' : ['Machine learning', 'Машинное обучение',
                                        'Семантика', 'Semantics'],
                        'Big Data' : ['Machine learning', 'Машинное обучение',
                                    'Семантика', 'Semantics'],
                        'Поисковые технологии' : ['Data Mining', 'Machine learning',
                                                'Машинное обучение', 'Big Data']}

    document = ph.Document(number)
    document.set_txt_path(txt_path)
    document.set_html_path(html_path)
    document.set_list_of_keywords(list_of_keywords)
    document.set_dict_of_keywords_used_together(dict_of_keywords)
    document.process()