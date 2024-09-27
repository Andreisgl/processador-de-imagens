from flask import Flask, request, send_file, render_template
import os

INPUT_FOLDER = 'input_folder'
INPUT_FOLDER = os.path.join('./', INPUT_FOLDER)
if not os.path.exists(INPUT_FOLDER):
    os.mkdir(INPUT_FOLDER)

OUTPUT_FOLDER = 'output_folder'
OUTPUT_FOLDER = os.path.join('./', OUTPUT_FOLDER)
if not os.path.exists(OUTPUT_FOLDER):
    os.mkdir(OUTPUT_FOLDER)

app = Flask(__name__)

#app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER



@app.route("/")
def home():
    return render_template('frontend.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    # Obter arquivo
    if 'input_file' not in request.files:
        return 'No file uploaded', 400
    file = request.files['input_file']
    input_file_name = file.filename # Depois adicionar informação para distinguir esse arquivo de outros
    option = request.form.get('option')


    # Salvar arquivo original
    input_file_path = os.path.join(INPUT_FOLDER, input_file_name)
    with open(input_file_path, 'wb') as filewrite:
        filewrite.write(file.stream.read())
    #return send_file(input_file_path, as_attachment=True) # Enviar o mesmo arquivo sem modificações
    

    # Abrir arquivo original
    with open(input_file_path, 'rb') as fileread:
        data = fileread.read()
    output_data = modificar_arquivo(data, option)


    # Salvar arquivo modificado
    prefixo = 'out'
    output_file_name = f'{prefixo}_{input_file_name}'
    output_file_path = os.path.join(OUTPUT_FOLDER, output_file_name)

    # Process file and option (Add your logic here)
    #processed_filename = 'processed_output.txt'
    with open(output_file_path, 'wb') as filewrite:
        filewrite.write(output_data)
    
    # Enviar arquivo
    return send_file(output_file_path, as_attachment=True)

    #render_template('frontend.html', input_image)


def modificar_arquivo(data, opcao):
    out_data = data
    return out_data


if __name__ == "__main__":
    app.run(debug=True)
