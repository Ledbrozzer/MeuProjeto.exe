# venv\Scripts\activate  -- Ativar ambiente virtual
# pip install flask pandas openpyxl werkzeug
# pip show flask  -- Verificar se flask foi instalado corretamente
# pip install xlsxwriter
# pip install lxml
# pip install openpyxl
# pip install openpyxl==3.0.10
# python app/controller/Server.py
# pip install pyinstaller
# pyinstaller --onefile --name MeuProjeto app/controller/Server.py
# pyinstaller --onefile --add-data "../view/index.html;view" --add-data "../view/App.html;view" --add-data "../view/css;view/css" --add-data "../view/js;view/js" --add-data "../model/StreamLit_App.py;model" --name MeuProjeto Server.py
# cd dist
# .\MeuProjeto.exe
# pyinstaller --onefile --add-data "../view/index.html;view" --add-data "../view/App.html;view" --add-data "../view/css/log_style.css;view/css" --add-data "../view/css/reset.css;view/css" --add-data "../view/css/responsive.css;view/css" --add-data "../view/css/style.css;view/css" --add-data "../view/js;view/js" --add-data "../model/StreamLit_App.py;model" --name MeuProjeto Server.py
# pyinstaller --onefile --add-data "../view/index.html;view" --add-data "../view/App.html;view" --add-data "../view/css/log_style.css;view/css" --add-data "../view/css/reset.css;view/css" --add-data "../view/css/responsive.css;view/css" --add-data "../view/css/style.css;view/css" --add-data "../view/js;view/js" --add-data "../model/StreamLit_App.py;model" --name MeuProjeto Server.py
#pyinstaller MeuProjeto.spec
import os
import sys
import webbrowser
from flask import Flask, request, jsonify, send_file, redirect, url_for, render_template_string, send_from_directory
from werkzeug.utils import secure_filename
import pandas as pd
import io
from openpyxl import Workbook

app = Flask(__name__)

def get_file_path(filename):
    if getattr(sys, 'frozen', False):  # Executável criado com PyInstaller
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)

@app.route('/')
def index():
    file_path = get_file_path('view/index.html')
    print(f"Tentando abrir: {file_path}")
    with open(file_path, encoding='utf-8') as f:
        content = f.read()
    return render_template_string(content)

@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['usuario']
    senha = request.form['senha']
    # Credenciais-exemplo
    users = {"Jose Mario": "1234", "Saulo": "5678", "Gesse": "9123"}
    
    if usuario in users and users[usuario] == senha:
        return redirect(url_for('app_page'))
    else:
        return 'Credenciais inválidas!'

@app.route('/app')
def app_page():
    file_path = get_file_path('view/App.html')
    print(f"Tentando abrir: {file_path}")
    with open(file_path, encoding='utf-8') as f:
        content = f.read()
    return render_template_string(content)

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(get_file_path('view/css'), filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory(get_file_path('view/js'), filename)

@app.route('/process_csv', methods=['POST'])
def process_csv():
    try:
        data = request.json['data']
        df = pd.read_csv(io.StringIO(data), delimiter=';', on_bad_lines='skip')
        # Remover colunas indesejadas
        colunas_para_excluir = ["Requisição", "Hora Abast.", "Obs.", "Abast. Externo", "Combustível"]
        colunas_existentes = [col for col in colunas_para_excluir if col in df.columns]
        if colunas_existentes:
            df = df.drop(columns=colunas_existentes)
        # Converter colunas para numérico
        df['Km Rodados'] = pd.to_numeric(df['Km Rodados'], errors='coerce')
        df['Litros'] = pd.to_numeric(df['Litros'].astype(str).str.replace(',', '').str[:-2], errors='coerce')
        df['Vlr. Total'] = pd.to_numeric(df['Vlr. Total'].astype(str).str.replace(',', ''), errors='coerce')
        df['Horim. Equip.'] = pd.to_numeric(df['Horim. Equip.'], errors='coerce')
        # Calcular colunas adicionais
        df['Km por Litro'] = df['Km Rodados'] / df['Litros']
        df['Lucro'] = df['Km Rodados'] - df['Vlr. Total']
        df['Horim por Litro'] = df['Horim. Equip.'] / df['Litros']
        # Convertendo resultados para HTML
        result_html = df.to_html()
        return jsonify(result=result_html)
    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route('/export_excel', methods=['POST'])
def export_excel():
    try:
        data = request.json['data']
        df = pd.read_html(io.StringIO(data))[0]
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Dados Filtrados')
        output.seek(0)
        response = send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='dados_filtrados.xlsx'
        )
        return response
    except Exception as e:
        return jsonify(error=str(e)), 400

if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5001")
    app.run(debug=True, port=5001)