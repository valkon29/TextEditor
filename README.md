# Текстовый редактор
### Что умеет?
Редактирование текста, открыть, сохранить файл, сохранить как, выход (при этом спрашивает сохранить изменения, если таковые были), copy/paste/cut. Имеется буфер обмена, в который попадет текст из команд copy & cut. Нажав на соответсвующий текс, он вставится в текущую позицию курсора (если передумали вставлять, можно просто закрыть окно буфера). При этом есть меню со всеми этими командами, где прописаны хоткеями для них. Все хоткеи используют ctrl.
### Как запустить?
```bash
python3 main.py
```
При этом можно передать файл который следует открыть сразу при запуске:
```bash
python3 main.py some_file.txt
```
Можно исппользовать абсолютный и относительный пути.

Примечание. *Работать должно как на маке, так и на линуксе, но возможно на линуксе выглядеть будет не так красиво, цвета и шрифты подгонял под мак*