import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import documentation as doc
import uuid

def read(patch = 'C:/time-calc-TT/source/for_calc.xlsx', names = doc.default_names) -> dict:
    '''
    patch - путь до файла с .xlsx таблицой
    name - JSON-объект, устанавливающий наименования фичей и таргетов в .xlsx файле 
    '''
    cat_names = list(names['features']["categorial"].values()); cat_names_doc = list(names['features']["categorial"].keys())
    num_names = list(names['features']["numerical"].values()); num_names_doc = list(names['features']["numerical"].keys())
    targets_names = list(names['targets'].values()); target_names_doc = list(names['targets'].keys())
    data = pd.read_excel(patch, skiprows=1)
    data = data[cat_names+num_names+targets_names]
    data = data.rename(columns=dict(zip(cat_names+num_names+targets_names, cat_names_doc+num_names_doc+target_names_doc)))
    data.index = [str(uuid.uuid4()) for _ in range(len(data))]  # генерим сложные случайные ключи
    data["is_italic"] = data["is_italic"].replace({"есть": 1, "нет": 0}).infer_objects(copy=False)
    data["font_type"] = data["font_type"].replace({"антиква": 'antiqua', "гротеск": 'grotesque', "разностильные шрифты": 'mixed', "рукописный шрифт": 'handwritten',"логотип": 'logo'}).infer_objects(copy=False)
    data["calc_type"] = data["calc_type"].replace({"новый": 'new', "UPD": 'upd', "тех UPD": 'tech_upd', "лого": 'logo', "кастом": 'custom', "кириллизация": 'cyrillization'}).infer_objects(copy=False)
    for index, row in data[target_names_doc].iterrows():        
        if all(list(pd.isna(row))):
            data.drop(index=index,inplace=True)  # удаляем записи, если таргет вектор пуст
    categorial_features = data[cat_names_doc]
    numerical_features = data[num_names_doc]
    targets = data[target_names_doc]
    return {"categorial_features": categorial_features, 'numerical_features': numerical_features, "targets": targets, "all_data": data}

def gap_matrix(data: pd.DataFrame):
    plt.figure(figsize=(8, 6))
    sns.heatmap(data.isnull(), cmap='viridis', cbar=False, yticklabels=False)
    plt.title('gap heat map')
    plt.xlabel('rows')
    plt.ylabel('index')
    plt.show()

def correlation_matrix(data: pd.DataFrame):
    '''
    draws correlation matrix
    '''
    correlation_matrix = data.corr()
    plt.figure(figsize=(6, 6))
    hmap = sns.heatmap(correlation_matrix, annot=False, fmt='.2f', cmap='coolwarm', square=True)
    hmap.set_xticklabels(hmap.get_xmajorticklabels(), rotation=90)
    hmap.set_yticklabels(hmap.get_ymajorticklabels(), rotation=0)
    plt.title('correlation matrix')
    plt.show()

def OHE(data: pd.DataFrame) -> pd.DataFrame:
    '''
    data должен содержать все конечные ключи json объектов doc.doc
    '''
    cat_names = list(doc.doc['features']["categorial"].keys())
    num_names = list(doc.doc['features']["numerical"].keys())
    targets_names = list(doc.doc['targets'].keys())
    header = cat_names + num_names + targets_names
    df_operational = data[header]
    temp_cat_feat = doc.combines_of_cat_features
    indexes_temp = [f'temp_{n}' for n in range(len(temp_cat_feat))]
    temp_cat_feat = pd.DataFrame(temp_cat_feat, columns=cat_names, index=indexes_temp)
    for column in data.columns:
        if column not in temp_cat_feat.columns:
            temp_cat_feat[column] = pd.NA
    df_operational = pd.concat([df_operational, temp_cat_feat])
    df_operational[num_names + targets_names] = df_operational[num_names + targets_names].fillna(0)
    df_operational = df_operational.fillna(0)
    df_operational[['is_italic']+num_names] = df_operational[['is_italic']+num_names].astype(int)
    # encoding
    df_operational = pd.get_dummies(df_operational, columns=cat_names, prefix=cat_names, drop_first=True)
    # define types
    df_operational = df_operational.drop(indexes_temp)
    df_operational = df_operational.replace({True: 1, False: 0}).infer_objects(copy=False)
    return {"features": df_operational.drop(targets_names,axis=1), "targets": df_operational[targets_names]}
