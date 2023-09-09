from flask import Flask, render_template
import pandas as pd
import pretty_html_table as pht
import matplotlib.pyplot as plt

application = Flask(__name__)

@application.route('/index.php')
@application.route('/')
def get_index():
    
    # Функция формирования дата-фрейма из эксель таблицы платформ с сайта ЦБ
    def get_data_frame_from_cbr_platform_list():
        
        # получаем фрейм из файла эксель по ссылке
        df = pd.read_excel(r'https://cbr.ru/vfs/finmarkets/files/supervision/list_invest_platform_op.xlsx')
        
        # переименовываем столбцы
        df.rename(columns = {'Unnamed: 0':'Дата включения сведений об операторе инвестиционной платформы в реестр',
                             'Unnamed: 1':'Полное фирменное наименование на русском языке',
                             'Unnamed: 2':'Сокращенное фирменное наименование на русском языке (при наличии)',
                             'Unnamed: 3':'Основной государственный регистрационный номер (ОГРН)',
                             'Unnamed: 4':'Идентификационный номер налогоплательщика (ИНН)',
                             'Unnamed: 5':'Адрес, указанный в едином государственном реестре юридических лиц',
                             'Unnamed: 6':'Адрес сайта в информационно-телекоммуникационной сети \n«Интернет», который используется оператором инвестиционной платформы для предоставления доступа к инвестиционной платформе',
                             'Unnamed: 7':'Номер контактного телефона',
                             'Unnamed: 8':'Адрес электронной почты'}, inplace = True)
        
        # удаляем первые лишние строки 0-3 из поступившего фрейма, заменяем поступивший фрейм на новый – True
        df.drop(labels = [0,1,2,3], axis = 0, inplace = True)
        
        
        # делаем столбец с порядковыми номерами строк
        df['Порядковый номер'] = [str(i) for i in range(1, df.shape[0] + 1)] 
        
        # Столбец с порядковым номером меняем местами с другими столбцами и переводим его на первое место
        df = df[['Порядковый номер'] + df.columns[:-1].tolist()]
        
        # Всегда, когда надо присвоить что-то фрейму, перед присваиванием лучше вызвать df.copy(), чтобы избежать неоднозначностей
        df = df.copy()
        
        return df
    
    # Функция формирования красивой таблицы из дата-фрейма
    def get_table_from_data_frame():
        
        result_table_of_platforms = pht.build_table(get_data_frame_from_cbr_platform_list(), 'blue_light', font_size = 'small', font_family = 'Arial')
        
        return result_table_of_platforms 
    
    # Функция формирования графика распределения платформ по годам
    def get_figure_of_years_platforms_from_data_frame():
        
        number_of_2020 = 0
        number_of_2021 = 0
        number_of_2022 = 0
        number_of_2023 = 0
        number_of_2024 = 0
        
        # Получаем таблицу цифровых платформ
        df = get_data_frame_from_cbr_platform_list()
        
        
        # Если в таблице находятся сведения о годах, то распределяем их в соответствующие переменные, сообразно их количеству
        for row in df['Дата включения сведений об операторе инвестиционной платформы в реестр']:
            if '2020' in row:
                number_of_2020 += 1
            elif '2021' in row:
                number_of_2021 += 1
            elif '2022' in row:
                number_of_2022 += 1
            elif '2023' in row:
                number_of_2023 += 1
            else:
                number_of_2024 += 1
                                
        list_of_labels = ['2020 год','2021 год','2022 год','2023 год']
        list_of_dates = [number_of_2020, number_of_2021, number_of_2022, number_of_2023]
        
        # Отступ на графике совпадает с количеством значений по оси x, т.е. с количество элементов в list_of_dates
        explode = (0.1,0.1,0.1,0.1)
        
        fig = plt.figure(figsize=(16, 8))
        fig1 = plt.figure(figsize=(16, 8))
        
        # Создание круговой диаграммы по годам
        ax1 = fig.add_subplot()
        ax1.set_title('\n Количество регистраций цифровых \n инвестиционных платформ по годам \n', fontsize = 12 )
        ax1.pie(list_of_dates, labels = list_of_labels, shadow = True, explode = explode, autopct='%1.1f%%')
        ax1.legend([list_of_labels[0] + ' - ' + str(list_of_dates[0]), list_of_labels[1] + ' - ' + str(list_of_dates[1]),
                    list_of_labels[2] + ' - ' + str(list_of_dates[2]), list_of_labels[3] + ' - ' + str(list_of_dates[3])])
        fig.savefig('static/img/figure_of_years.png', dpi=300)
        
        
        # Создание графика по годам
        ax2 = fig1.add_subplot()
        ax2.text('2020 год', number_of_2020, str(number_of_2020))
        ax2.text('2021 год', number_of_2021, str(number_of_2021))
        ax2.text('2022 год', number_of_2022, str(number_of_2022))
        ax2.text('2023 год', number_of_2023, str(number_of_2023))
        ax2.set_title('\n Динамика распределения количества регистраций \n цифровых инвестиционных платформ по годам \n', fontsize = 12)
        ax2.set(ylabel = ('Количество регистраций'))
        ax2.plot(list_of_labels, list_of_dates, color='r', marker='o')
        ax2.grid()
        fig1.savefig('static/img/figure_of_years_2.png', dpi=300)
        
    
        total_platforms = sum(list_of_dates)    
    
        return 'static/img/figure_of_years.png','static/img/figure_of_years_2.png', total_platforms    
    
    # Функция формирования графика распределения регистраций цифровых инвестиционных платформ по городам России
    def get_figure_of_cities_platforms_from_data_frame():
        
        # Получаем таблицу цифровых инвестиционных платформ
        df = get_data_frame_from_cbr_platform_list()
        
        all_list_of_cities_from_df = []
        unique_city_names = []

        # Каждую строку разделяем по запятой. Получаем из строки список. Затем, берем второй элемент в списке с наименованием города и добавляем его в список городов
        # Проходимся по всем строкам столбца
        for row in df['Адрес, указанный в едином государственном реестре юридических лиц']:
            all_list_of_cities_from_df.append(row.split(',')[1])
        
        # Запускаем генератор списка, в котором формируем перечень городов, по одному упоминанию для каждого города. Данные сведения необходимы для создания графика.                
        unique_city_names = [city for city in all_list_of_cities_from_df if city not in unique_city_names]
                
        # Запускаем генератор словаря, где каждому городу присваиваем количество его упоминаний в общем списке городов all_list_of_cities_from_df
        unique_city_names_with_numbers = {city : all_list_of_cities_from_df.count(city) for city in all_list_of_cities_from_df}
                
        fig = plt.figure(figsize=(16, 8))
        
        
        # Создание гистрограммы распределения регистраций цифровых инвестиционных платформ по городам России
        ax1 = fig.add_subplot()
        ax1.set_title('\n Распределение количества регистраций цифровых инвестиционных платформ \n по городам \n', fontsize = 12 )
        ax1.bar(unique_city_names_with_numbers.keys(), unique_city_names_with_numbers.values())
        ax1.set_xticklabels(unique_city_names_with_numbers.keys(), rotation=30, ha='right', size = 8)
        ax1.set_ylabel('Количество регистраций')
        ax1.grid()
        for key in unique_city_names_with_numbers.keys():
                # Выводим значения количества городов на график к каждому столбцу диаграммы графически приподнимая значение выше на 1 ед.
                ax1.text(key, unique_city_names_with_numbers[key] + 1, unique_city_names_with_numbers[key])
        
        fig.savefig('static/img/figure_of_cities.png', dpi=300)
        
        # Возвращаем картинку гистограммы в качестве результата работы функции
        return 'static/img/figure_of_cities.png'
            
    def get_figure_numbers_of_legal_entities_from_data_frame():
        
        # Получаем таблицу цифровых инвестиционных платформ
        df = get_data_frame_from_cbr_platform_list()
        
        
        # ОБъявляем 2 переменных, в которых хранятся значения количества акционерных обществ и обществ с ограниченной ответственностью
        number_of_joint_stock_companies = 0
        number_of_limited_liability_companies = 0
        
        # Проходимся по всем строкам столбца, распределяем типы юридических лиц в соответствующие переменные
        for row in df['Полное фирменное наименование на русском языке']:
            if 'акционерное' in row.lower():
                number_of_joint_stock_companies += 1
            elif 'ограниченной' in row.lower():
                number_of_limited_liability_companies += 1
                         
        
        list_of_labels = ['Акционерные общества','Общества с ограниченной ответственностью']
        list_of_dates = [number_of_joint_stock_companies, number_of_limited_liability_companies]
               
        # Отступ на графике совпадает с количеством значений по оси x, т.е. с количество элементов в list_of_dates
        explode = (0.1, 0.1)
        
        fig = plt.figure(figsize=(16, 8))
        
        
        # Создание круговой диаграммы по типам юридических лиц: акционерные общества и общества с ограниченной ответственностью
        ax1 = fig.add_subplot()
        ax1.set_title('\n Распределение количества юридических лиц по типам: акционерные общества \n и общества с ограниченной ответственностью \n', fontsize = 12 )
        ax1.pie(list_of_dates, labels = list_of_labels, shadow = True, explode = explode, autopct='%1.1f%%')
        ax1.legend([str(list_of_labels[0]) +' - '+ str(list_of_dates[0]), str(list_of_labels[1]) + ' - ' + str(list_of_dates[1])])
        fig.savefig('static/img/figure_of_legal_entities.png', dpi=300)
        

        return 'static/img/figure_of_legal_entities.png'
    
    
    
    
    return render_template('index.php', table_of_platforms = get_table_from_data_frame(), 
                           url_figure_of_years = get_figure_of_years_platforms_from_data_frame(),
                           url_figure_of_cities = get_figure_of_cities_platforms_from_data_frame(),
                           total_platforms = get_figure_of_years_platforms_from_data_frame(),
                           url_figure_of_number_of_cities = get_figure_of_cities_platforms_from_data_frame(),
                           url_figure_of_legal_entities = get_figure_numbers_of_legal_entities_from_data_frame())


if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)