from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/automate', methods=['POST'])
def automate():
    data = request.json
    platform = data.get('platform')
    options = data.get('options')
    
    if platform == 'Magazine Luiza':
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
            driver.get("https://www.magazinevoce.com.br/login/")
            time.sleep(2)  # Aguarde até a página carregar
            
            try:
                login_input = driver.find_element(By.XPATH, '//*[@id="email"]')
                login_input.send_keys('07216945948')
            except Exception as e:
                print('Elemento "Login" não localizado')
                return jsonify({'status': 'fail', 'message': 'Elemento "Login" não localizado'})
            
            try:
                password_input = driver.find_element(By.XPATH, '//*[@id="password"]')
                password_input.send_keys('2004juni')
            except Exception as e:
                print('Elemento "Senha" não localizado')
                return jsonify({'status': 'fail', 'message': 'Elemento "Senha" não localizado'})
            
            try:
                login_button = driver.find_element(By.XPATH, '//*[@id="login"]/div[2]/div/div[2]/form/fieldset/div[6]/button')
                login_button.click()
            except Exception as e:
                print('Elemento "Botão de login" não localizado')
                return jsonify({'status': 'fail', 'message': 'Elemento "Botão de login" não localizado'})
            
            time.sleep(3)  # Aguarde até a próxima página carregar
            driver.quit()
            return jsonify({'status': 'success', 'message': 'Automação concluída com sucesso'})
        except Exception as e:
            return jsonify({'status': 'fail', 'message': str(e)})
    else:
        return jsonify({'status': 'fail', 'message': 'Plataforma não suportada'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
