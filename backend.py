'''Backend da página do processador de imagens. Administra entrada e saída de arquivos'''

import operacoes as ops

from flask import Flask, request, send_file, render_template
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)

# Diretório dos arquivos de entrada
DIR_ENTRADA = 'dir_entrada'
DIR_ENTRADA = os.path.join('./', DIR_ENTRADA)
if not os.path.exists(DIR_ENTRADA):
    os.mkdir(DIR_ENTRADA)
app.config['INPUT_FOLDER'] = DIR_ENTRADA

# Diretório dos arquivos de saída
DIR_SAÍDA = 'dir_saida'
DIR_SAÍDA = os.path.join('./', DIR_SAÍDA)
if not os.path.exists(DIR_SAÍDA):
    os.mkdir(DIR_SAÍDA)
app.config['DIR_SAIDA'] = DIR_SAÍDA


entrada_arquivo_nome = ''
entrada_arquivo_path = ''
#option = 0


@app.route("/")
def home():
    return render_template('frontend.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    global entrada_arquivo_nome
    global entrada_arquivo_path

    # Verificar se o arquivo original está presente
    if 'input_file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['input_file']
    entrada_arquivo_nome = secure_filename(file.filename)  # Validar nome de arquivo

    # Salvar o arquivo original
    entrada_arquivo_path = os.path.join(app.config['INPUT_FOLDER'], entrada_arquivo_nome)
    file.save(entrada_arquivo_path)
    
    # Abrir arquivo original
    with open(entrada_arquivo_path, 'rb') as fileread:
        input_file_data = fileread.read()

    # Modificar dados para arquivo de saída
    output_file_data = modificar_arquivo(input_file_data)

    # Definir nome do arquivo de saída
    prefixo = 'out'
    output_file_name = f'{prefixo}_{entrada_arquivo_nome}'
    output_file_path = os.path.join(DIR_SAÍDA, output_file_name)
    # Salvar arquivo de saída
    with open(output_file_path, 'wb') as filewrite:
        filewrite.write(output_file_data)
    
    #return send_file(input_file_path, as_attachment=True) # Enviar o mesmo arquivo sem modificações
    return send_file(output_file_path, as_attachment=True) # Enviar o arquivo sem modificações

def modificar_arquivo(entrada = b''):
    dados = '' 
    dados = ops.resolver(entrada.decode('utf-8'))

    return bytes(dados, 'utf-8') # Retornar o mesmo arquivo por enquanto

if __name__ == "__main__":
    app.run(debug=True)
