import pandas as pd
import numpy as np
import re
import matplotlib
from matplotlib import pyplot as plt

works = pd.read_csv("works.csv", header=0, index_col=False)

law = r'(.*юри.*)|(.*адвокат.*)'
finance = r'(.*эконом.*)|(.*банк.*)|(.*финанс.*)|(.*бухгалтер.*)'
administration = r'(.*менедж.*)|(.*директ.*)|(.*секретар.*)|(.*управ.*)'
technic = r'(.*техн.*)|(.*инженер.*)|(.*разработ.*)|(.*меха.*)|(.*матем.*)'
trade = r'(.*прода.*)|(.*касси.*)|(.*маркето.*)'
studies = r'(.*педагог.*)|(.*преподават.*)|(.*учител.*)|(.*воспита.*)'

# Из нашего файла works.csv выбираем всех менеджеров, у которых написана их квалификация.
managers = works[works.jobTitle.str.contains(r'.*менеджер.*', case=False, flags=re.IGNORECASE, na=False)]
managers = managers[~managers.qualification.isna()]
total_managers = managers.shape[0]


def get_managers_qualification(qualification_regex):
    return managers[managers.qualification.str.contains(qualification_regex, case=False, flags=re.IGNORECASE, na=False)]


# Далее создаём переменные, в которых будет хранится список менеджеров с определённой квалификацией

# Менеджеры с образованием в сфере юриспруденции
law_managers = get_managers_qualification(law)
# Менеджеры в сфере финансов
finance_managers = get_managers_qualification(finance)
# Менеджеры в управленческой сфере
administration_managers = get_managers_qualification(administration)
# Менеджеры в сфере торговли
trade_managers = get_managers_qualification(trade)
# Менеджеры в технической сфере
technic_managers = get_managers_qualification(technic)
# Менеджеры в сфере педагогики
studies_managers = get_managers_qualification(studies)

count_by_name = {'Юриспруденция': law_managers.shape[0], 'Экономика': finance_managers.shape[0],
                 'Управление': administration_managers.shape[0], 'Торговля': trade_managers.shape[0],
                 'Инженеры и технологи': technic_managers.shape[0], 'Педагоги': studies_managers.shape[0]}

# Далее создадим нам нужно выделить сферу другое. В неё войдут описание квалификаций по типу: "бакалавр"
# и люди с профессиями, которых  мало, чтобы выделить их в одну отдельную группу

other_managers = managers.copy()
for df in [law_managers, finance_managers, administration_managers, trade_managers, technic_managers, studies_managers]:
    other_managers = pd.merge(other_managers, df, indicator=True, how='outer') \
        .query('_merge=="left_only"') \
        .drop('_merge', axis=1)

vague_qualification_count = other_managers[~other_managers.qualification.str
        .contains('( *бакалавр *)|( *специалист *)|( *магистр *)', case=False, flags=re.IGNORECASE)].shape[0]

misc_qs_count = other_managers.shape[0] - vague_qualification_count
count_by_name[r'Бакалавр/Специалист/Магистр'] = vague_qualification_count
count_by_name['Другое'] = misc_qs_count

# Выводим круговую диаграмму (piechart), в которой отобразим всё вышесделанное
plt.pie(list(count_by_name.values()), labels=list(count_by_name.keys()))
plt.show()
