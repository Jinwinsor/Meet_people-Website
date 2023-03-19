from datetime import datetime, timedelta
from flask import Flask, render_template, redirect, request, session, flash, jsonify
from flask_app import app
import requests
from flask_app.models import user, post
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user')
def home():
    return redirect('/')


@app.route('/user/register', methods=['POST'])
def register():
    # Check it's right register form?
    if not User.validate_user(request.form):
        return redirect('/user')

    # Check the password form
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    print(data)

    # Save the new inform from a user and save the data
    user_id = User.save(data)
    session['user_id'] = user_id

    flash("You are logged in!", "success")
    return redirect('/dashboard')


@app.route('/user/login', methods=['POST'])
def login():

    # Let login through email.
    # Take ONE through the email
    data = {
        'email': request.form['email']
    }

    # (1)Email check
    user = User.getOneByEmail(data)

    if not user:
        flash("Invalid email", "login")
        return redirect('/user')

    # (2)Password check
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email or Password", "login")
        return redirect('/user')

    session['user_id'] = user.id

    if 'user_id' in session:
        return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('user')


# ========= WEATHER API =======


@app.route('/weather', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        city = request.form.get('city')
        api_key = '09c145a4b2a12f4ce9704c8c1d164268'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        response = requests.get(url)
        weather_data = response.json()
        if weather_data.get("cod") != 200:
            session['weather_data'] = {'error': "City not found"}
        else:
            session['weather_data'] = weather_data
        return redirect('/dashboard')
    return redirect('/dashboard')

# ==========FORECAST APP

# @app.route('/forecast', methods=['POST'])
# def forecast():
#     weather_data = ''
#     error = False
#     city_name = request.form.get('cityName')
#     if city_name:
#         api_key = 'My_api_key'
#         url = f'http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}&units=metric'
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             daily_forecast = {}
#             for forecast in data['list']:
#                 forecast_date = datetime.fromtimestamp(forecast['dt']).date()
#                 if forecast_date not in daily_forecast:
#                     daily_forecast[forecast_date] = {
#                         'min_temp': forecast['main']['temp'],
#                         'max_temp': forecast['main']['temp'],
#                         'description': forecast['weather'][0]['description'],
#                         'humidity': forecast['main']['humidity'],
#                         'wind': forecast['wind']['speed'],
#                         'feels_like': forecast['main']['feels_like'],
#                         'icon_url': f"http://openweathermap.org/img/wn/{forecast['weather'][0]['icon']}.png"
#                     }
#                 # else:
#                 #     daily_forecast[forecast_date]['min_temp'] = min(
#                 #         daily_forecast[forecast_date]['min_temp'], forecast['main']['temp'])
#                 #     daily_forecast[forecast_date]['max_temp'] = max(
#                 #         daily_forecast[forecast_date]['max_temp'], forecast['main']['temp'])

#             weather_data = {
#                 'city_name': city_name,
#                 'forecast': []
#             }
#             today = datetime.today().date()
#             for i in range(1):
#                 # 날짜 하나씩 증가시켜서 총  5일 만들기 (using timedelta) .
#                 forecast_date = today + timedelta(days=i)
#                 if forecast_date in daily_forecast:
#                     my_data = daily_forecast[forecast_date]
#                     average_temp = round(
#                         ((my_data['min_temp']) + (my_data['max_temp']))/2)
#                     forecast = {
#                         'date': forecast_date.strftime('%A, %B, %d'),
#                         'temperature': average_temp,
#                         'description': my_data['description'],
#                         'humidity': my_data['humidity'],
#                         'wind': my_data['wind'],
#                         'feels_like': my_data['feels_like'],
#                         'icon_url': my_data['icon_url']
#                     }
#                     weather_data['forecast'].append(forecast)
#         else:
#             error = True
#     else:
#         error = True
#     if error:
#         flash('Unable to get weather data for the city provided. Try again', 'error')
#     else:
#         session['weather_data'] = weather_data
#     return redirect('/dashboard')
