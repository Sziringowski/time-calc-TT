import numpy as np
import itertools

# определим допустимые значения в json-объекте doc
doc = {
    'features': {
        'categorial': {
            'font_type': ['antiqua', 'grotesque', 'mixed', 'handwritten', 'logo'],
            'is_italic': [0, 1],
             #'is_hinting_manual': [0, 1],
            'calc_type': ['new', 'upd', 'tech_upd', 'logo', 'custom', 'cyrillization']
        },
        'numerical': {
            'n_gliphs': np.linspace(0, 10_000, 10_001, dtype=int),
            'n_styles': np.linspace(0, 10_000, 10_001, dtype=int)
        }
    },
    'targets': {
        't_sketch': np.linspace(0, 500, 501, dtype=int),
        't_straight': np.linspace(0, 500, 501, dtype=int),
        't_angled': np.linspace(0, 500, 501, dtype=int),
        't_mast': np.linspace(0, 500, 501, dtype=int),
        't_kern': np.linspace(0, 500, 501, dtype=int),
        't_hint': np.linspace(0, 500, 501, dtype=int)
    }
}

# определим имена по умолчанию для атрибутов
default_names = {
    'features': {
        'categorial': {
            'font_type': "Тип шрифта",
            'is_italic': "Италики",
            'calc_type': "Тип проекта"
        },
        'numerical': {
            'n_gliphs': "Кол-во знаков в начертании",
            'n_styles': "Кол-во начертаний"
            #'n_masters': 'Кол-во мастеров'
        }
    },
    'targets': {
        't_sketch': "идеи/\nскетчи",
        't_straight': "прямые",
        't_angled': "наклонные",
        't_mast': "мастеринг",
        't_kern': "кернинг",
        't_hint': "хинтинг"
    }
}

combines_of_cat_features = np.array(list(itertools.product(
         *(doc["features"]["categorial"].values()) 
         )))


