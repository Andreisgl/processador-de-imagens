'''Backend da página do processador de imagens. Administra entrada e saída de arquivos'''

import operacoes as ops

from flask import Flask, request, send_file, render_template
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)

# Diretório dos arquivos de entrada
INPUT_FOLDER = 'input_folder'
INPUT_FOLDER = os.path.join('./', INPUT_FOLDER)
if not os.path.exists(INPUT_FOLDER):
    os.mkdir(INPUT_FOLDER)
app.config['INPUT_FOLDER'] = INPUT_FOLDER

# Diretório dos arquivos de saída
OUTPUT_FOLDER = 'output_folder'
OUTPUT_FOLDER = os.path.join('./', OUTPUT_FOLDER)
if not os.path.exists(OUTPUT_FOLDER):
    os.mkdir(OUTPUT_FOLDER)
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER


input_file_name = ''
input_file_path = ''
option = 0


@app.route("/")
def home():
    return render_template('frontend.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    global input_file_name
    global input_file_path
    global option

    # Verificar se o arquivo original está presente
    if 'input_file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['input_file']
    input_file_name = secure_filename(file.filename)  # Secure the filename
    option = request.form.get('option')

    # Salvar o arquivo original
    input_file_path = os.path.join(app.config['INPUT_FOLDER'], input_file_name)
    file.save(input_file_path)

    # Exibir arquivo original
    #return render_template('frontend.html', input_image=f'/uploads/{input_file_name}')
    #return send_file(input_file_path, as_attachment=True) # Enviar o mesmo arquivo sem modificações




    # Salvar arquivo original
    #input_file_path = os.path.join(INPUT_FOLDER, input_file_name)
    #with open(input_file_path, 'wb') as filewrite:
    #    filewrite.write(file.stream.read())
    
    # Abrir arquivo original
    with open(input_file_path, 'rb') as fileread:
        input_file_data = fileread.read()

    # Modificar dados para arquivo de saída
    output_file_data = modificar_arquivo(input_file_data, option)

    # Definir nome do arquivo de saída
    prefixo = 'out'
    output_file_name = f'{prefixo}_{input_file_name}'
    output_file_path = os.path.join(OUTPUT_FOLDER, output_file_name)
    # Salvar arquivo de saída
    with open(output_file_path, 'wb') as filewrite:
        filewrite.write(output_file_data)
    
    #return send_file(input_file_path, as_attachment=True) # Enviar o mesmo arquivo sem modificações

    return send_file(output_file_path, as_attachment=True) # Enviar o arquivo sem modificações




@app.route('/process', methods=['POST'])
def process_file():
    global input_file_name
    global input_file_path
    global option

    # Abrir arquivo original
    with open(input_file_path, 'rb') as fileread:
        input_file_data = fileread.read()
    output_file_data = modificar_arquivo(input_file_data, option)

#
    # Salvar arquivo modificado
    prefixo = 'out'
    output_file_name = f'{prefixo}_{input_file_name}'
    output_file_path = os.path.join(OUTPUT_FOLDER, output_file_name)
#
    # Process file and option (Add your logic here)
    #processed_filename = 'processed_output.txt'
    with open(output_file_path, 'wb') as filewrite:
        filewrite.write(output_file_data)
    
    # Enviar arquivo
    return send_file(output_file_path, as_attachment=True)
    #return uploaded_file(output_file_path)

    #input_image = input_file_path
    #render_template('frontend.html')

def modificar_arquivo(entrada = b'', opcao:int = 0):
    dados = '' 
    dados = ops.resolver(str(entrada))

    return bytes(dados, 'utf-8') # Retornar o mesmo arquivo por enquanto

# Serve the uploaded files via a route
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(app.config['INPUT_FOLDER'], filename))

if __name__ == "__main__":
    app.run(debug=True)
