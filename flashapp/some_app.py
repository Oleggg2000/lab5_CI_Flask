from flask import Flask
from flask import render_template

from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField

from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired

from werkzeug.utils import secure_filename
import os

app = Flask(__name__)


@app.route("/")
def hello():
    return " <html><head></head> <body> <i><h1>Hello World!</h1></i> </body></html>"


@app.route("/data_to")
def data_to():
    some_pars = {'user':'Ivan','color':'red'}
    some_str = 'Hello my dear friends!'
    some_value = 10
    return render_template('simple.html', some_str=some_str, some_value=some_value, some_pars=some_pars)


# используем капчу и полученные секретные ключи с сайта google
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LcrEfoUAAAAAEUT-G_eQNnVjvfzRLHRKyOKTS5I'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LcrEfoUAAAAAHrgRuynjStzi9hWbL1s2LgpMxGY'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}

# создаем форму для загрузки файла
class NetForm(FlaskForm):
    openid = StringField('openid', validators = [DataRequired()])
    upload = FileField('Load image', validators=[
    FileRequired(),
    FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    recaptcha = RecaptchaField()
    submit = SubmitField('send')
# функция обработки запросов на адрес 127.0.0.1:5000/net
# модуль проверки и преобразование имени файла
# для устранения в имени символов типа / и т.д.

# подключаем наш модуль и переименовываем
# для исключения конфликта имен
import net as neuronet

# метод обработки запроса GET и POST от клиента
@app.route("/net",methods=['GET', 'POST'])
def net():
    form = NetForm()
    # обнуляем переменные передаваемые в форму
    filename=None
    neurodic = {}
    # проверяем нажатие сабмит и валидацию введенных данных
    if form.validate_on_submit():
    # файлы с изображениями читаются из каталога static
        filename = os.path.join('./static', secure_filename(form.upload.data.filename))
        fcount, fimage = neuronet.read_image_files(10,'./static')
        # передаем все изображения в каталоге на классификацию
        # можете изменить немного код и передать только загруженный файл
        decode = neuronet.getresult(fimage)
        # записываем в словарь данные классификации
        for elem in decode:
            neurodic[elem[0][1]] = elem[0][2]
            # сохраняем загруженный файл
            form.upload.data.save(filename)
            # передаем форму в шаблон, так же передаем имя файла и результат работы нейронной
            # сети если был нажат сабмит, либо передадим falsy значения
    return render_template('net.html',form=form,image_name=filename,neurodic=neurodic)




if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)