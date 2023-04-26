from flask import Flask, request, Response
from datetime import datetime, timedelta
import uuid
import random
import re
import xml.etree.ElementTree as ET

app = Flask(__name__)


# обработчик запросов по методу POST и PATH /api/xml/
@app.route('/api/xml/', methods=['POST'])
def xml():
    root = ET.fromstring(request.data)  # используется метод fromstring для получения данных запроса

    # Проверяем, что в переданном документе есть тег productInfo
    if root.find('productInfo') is not None:

        # Извлечение значений полей
        productinfo = root.find('productInfo')
        productcode = root.find('productInfo/productCode').text

        # Проверка соответствия кода продукта формату
        if re.match(r'^C\d{6}$', productcode):

            # Обработка данных и формирование XML-документа
            response = ET.Element("root")  # создается корневой элемент "root".
            productinfo_elem = ET.SubElement(response, "productInfo")  # Далее элементы помещаются внутрь этого тега по переменной
            ET.SubElement(productinfo_elem, "productCode").text = productcode
            ET.SubElement(productinfo_elem, "count").text = str(random.randrange(10, 99))
            ET.SubElement(productinfo_elem, "price").text = str(random.randrange(100, 999))
            ET.SubElement(response, "uuid").text = str(uuid.uuid1()) # Генерируется рандомный uuid

            xml_response = ET.tostring(response, encoding='UTF-8', method='xml', xml_declaration=True)
            return xml_response # Вовзращаем документ в формате XML

        # Возвращается сообщение об ошибке в случае несоответствия кода продукта паттерну "С000000"
        else:
            error_message = "<error>incorrect productCode</error>"
            return Response(error_message, mimetype='text/xml')


    # Проверяем, что в переданном документе есть тег clientInfo
    elif root.find('clientInfo') is not None:

        # Извлечение значений полей
        clientinfo = root.find('clientInfo')
        clientcode = root.find('clientInfo/clientCode').text

        # Проверка соответствия кода клиента формату
        if re.match(r'^LT\d{7}$', clientcode):

            # Обработка данных и формирование XML-документа
            response = ET.Element("root")  # создается корневой элемент "root".
            clientinfo_elem = ET.SubElement(response, "clientInfo")
            ET.SubElement(clientinfo_elem, "clientCode").text = clientcode # Далее элементы помещаются внутрь этого тега по переменной
            ET.SubElement(clientinfo_elem, "cardNumber").text = str(
                random.randint(10 ** 15, 10 ** 16 - 1)) # Таким образом рандомизируется 16-ти значное число
            ET.SubElement(clientinfo_elem, "balance").text = str(random.randrange(1000, 9999))
            ET.SubElement(clientinfo_elem, "currencyCode").text = "643"
            ET.SubElement(clientinfo_elem, "endDate").text = str(time_future()) # Генерация текущей даты + 5 лет
            ET.SubElement(response, "uuid").text = str(uuid.uuid1()) # Рандомный uuid
            xml_response = ET.tostring(response, encoding='UTF-8', method='xml', xml_declaration=True)
            return xml_response # Вовзращаем документ в формате XML

        # Возвращается сообщение об ошибке в случае несоответствия кода клиента паттерну "LT0000000"
        else:
            error_message = "<error>incorrect clientCode</error>"
            return Response(error_message, mimetype='text/xml')

    # Возвращается сообщение об ошибке в случае, когда передаются некорректные теги
    else:
        error_message = "<error>incorrect tag</error>"
        return Response(error_message, mimetype='text/xml')

# Генерация текущей даты + 5 лет
def time_future():
    current_date = datetime.now()
    future_date = current_date + timedelta(days=5 * 365 + 2)
    formatted_date = future_date.strftime('%Y-%m-%d')
    return formatted_date


if __name__ == '__main__':
    app.run()  # запуск приложения
