'''Neste arquivo estão localizados os métodos de alteração de arquivo'''

from asteval import Interpreter


def resolver(dados:str):
    saida = 'testeeee'

    print('ARQUIVO DE ENTRADA')
    print(dados)
    print('FIM/ARQUIVO DE ENTRADA')

    linhas = dados.splitlines()
    resultados = []

    for linha in linhas:
        resultados.append(avaliar_expressao(linha))


    saida = ''

    # Passar resultados para string
    comp = len(resultados)
    for i, r in enumerate(resultados):
        saida += str(r)
        if i < comp-1:
            saida += '\n'



    return saida


def avaliar_expressao(expression):
    ae = Interpreter()
    return ae(expression)

    


    