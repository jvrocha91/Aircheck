from flask import Flask, jsonify, request, render_template


app = Flask(__name__)

# Função para determinar o índice de qualidade do ar com base no valor e nos limites fornecidos.
def indice_qualidade_ar(valor, limites):
    for i, (minimo, maximo) in enumerate(limites):
        if minimo <= valor <= maximo:
            return i + 1
    return -1

# Função para obter os efeitos na saúde relacionados à classificação de qualidade do ar.
def imprime_efeitos_saude(classificacao):
    efeitos = {
        1: "N1 - Boa: A qualidade do ar é considerada satisfatória e a poluição do ar apresenta pouco ou nenhum risco.",
        2: "N2 - Moderada: Pessoas de grupos sensíveis (crianças, idosos e pessoas com doenças respiratórias e cardíacas) podem apresentar sintomas como tosse seca e cansaço. A população, em geral, não é afetada.",
        3: "N3 - Ruim: Toda a população pode apresentar sintomas como tosse seca, cansaço, ardor nos olhos, nariz e garganta. Pessoas de grupos sensíveis (crianças, idosos e pessoas com doenças respiratórias e cardíacas) podem apresentar efeitos mais sérios na saúde.",
        4: "N4 - Muito Ruim: Toda a população pode apresentar agravamento dos sintomas como tosse seca, cansaço, ardor nos olhos, nariz e garganta e ainda falta de ar e respiração ofegante. Efeitos ainda mais graves à saúde de grupos sensíveis (crianças, idosos e pessoas com doenças respiratórias e cardíacas).",
        5: "N5 - Péssima: Toda a população pode apresentar sérios riscos de manifestações de doenças respiratórias e cardiovasculares. Aumento de mortes prematuras em pessoas de grupos sensíveis."
    }
    return efeitos[classificacao]

@app.route('/qualidade_ar', methods=['POST'])
def qualidade_ar():
    data = request.json
    
    # Verificar se todos os campos necessários estão presentes
    for field in ['MP10', 'MP25', 'O3', 'CO', 'NO2', 'SO2']:
        if field not in data:
            return jsonify({'error': f'O campo {field} está faltando.'}), 400

        # Verificar se os campos são números
        if not isinstance(data[field], (int, float)):
            return jsonify({'error': f'O campo {field} deve ser um número.'}), 400
    
    # Verificar se todos os campos necessários estão presentes
    for field in ['MP10', 'MP25', 'O3', 'CO', 'NO2', 'SO2']:
        if field not in data:
            return jsonify({'error': f'O campo {field} está faltando.'}), 400
        
        # Verificar se os campos são números
        if not isinstance(data[field], (int, float)):
            return jsonify({'error': f'O campo {field} deve ser um número.'}), 400
        
    limites = [
        [(0, 50), (50, 100), (100, 150), (150, 250), (250, float('inf'))],
        [(0, 25), (25, 50), (50, 75), (75, 125), (125, float('inf'))],
        [(0, 100), (100, 130), (130, 160), (160, 200), (200, float('inf'))],
        [(0, 9), (9, 11), (11, 13), (13, 15), (15, float('inf'))],
        [(0, 200), (200, 240), (240, 320), (320, 1130), (1130, float('inf'))],
        [(0, 20), (20, 40), (40, 365), (365, 800), (800, float('inf'))],
    ]
    
    indices = [
        indice_qualidade_ar(data['MP10'], limites[0]),
        indice_qualidade_ar(data['MP25'], limites[1]),
        indice_qualidade_ar(data['O3'], limites[2]),
        indice_qualidade_ar(data['CO'], limites[3]),
        indice_qualidade_ar(data['NO2'], limites[4]),
        indice_qualidade_ar(data['SO2'], limites[5]),
    ]

    qualidade_ar = max(indices)
    qualificacoes = ["Boa", "Moderada", "Ruim", "Muito Ruim", "Péssima"]

    return render_template('qualidade_ar.html', qualidade_ar=qualificacoes[qualidade_ar - 1], efeitos_saude=imprime_efeitos_saude(qualidade_ar))


if __name__ == '__main__':
    app.run(debug=True)

       
