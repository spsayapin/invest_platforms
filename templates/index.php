<!DOCTYPE html>
<html lang="en">
<head>
  <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/style.css') }}" />
  <title>Структурный анализ реестра инвестиционных платформ России</title>
</head>
<body>

<div class="menu-wrapper">
    <ul class="menu">
        <li><a href="/">Главная</a>
        </li>
        <li><a href="https://cbr.ru/">Центральный банк РФ</a>
        </li>
        <li><a href="https://cbr.ru/queries/unidbquery/file/90134/2492">Раскрытие информации оператора инвестиционной платформы</a>
        </li>
        <li><a href="https://cbr.ru/queries/unidbquery/file/90134/1218">О порядке ведения реестра операторов</a>
        </li>
    </ul>
</div>

  <p>{{ table_of_platforms }}</p>
  <img src="{{ url_figure_of_years[0] }}" height="450"/>
  <img src="{{ url_figure_of_years[1] }}" height="450"/>
  <img src="{{ url_figure_of_number_of_cities }}" height="450"/>
  <img src="{{ url_figure_of_legal_entities }}" height="450"/>
</body>
</html>