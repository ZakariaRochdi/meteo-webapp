from flask import Flask, render_template, request
import os
import requests
import urllib.parse  # pour encoder les noms de villes avec accents

app = Flask(__name__)

# 🔑 Remplace ici par ta propre clé API
API_KEY = '4d081dc7cbc149c1444c8db6170e4cc2'

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None

    if request.method == 'POST':
        city = request.form['city'].strip()

        if city:  # s'assurer que la ville n'est pas vide
            city_encoded = urllib.parse.quote(city)
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city_encoded}&appid={API_KEY}&units=metric&lang=fr'

            try:
                response = requests.get(url)
                data = response.json()

                if response.status_code == 200:
                    weather = {
                        'ville': data['name'],
                        'pays': data['sys']['country'],
                        'temp': data['main']['temp'],
                        'humidite': data['main']['humidity'],
                        'vent': data['wind']['speed'],
                        'description': data['weather'][0]['description'],
                        'precipitations': 0
                    }

                    # Précipitations (s'il y en a)
                    if 'rain' in data and '1h' in data['rain']:
                        weather['precipitations'] = data['rain']['1h']
                    elif 'snow' in data and '1h' in data['snow']:
                        weather['precipitations'] = data['snow']['1h']

                else:
                    weather = {'error': f"Ville non trouvée ou erreur API : {data.get('message', 'Inconnue')}"}

            except Exception as e:
                weather = {'error': f"Erreur de connexion : {str(e)}"}

    return render_template('index.html', weather=weather)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

