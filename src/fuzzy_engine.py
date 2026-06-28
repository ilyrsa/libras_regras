import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# -> Modelagem fuzzy 
# Antecedentes, em escala de 0 a 10
velocidade = ctrl.Antecedent(np.arange(0, 11, 1), 'velocidade')
expressao = ctrl.Antecedent(np.arange(0, 11, 1), 'expressao')

#Consequente, em escala de 0 a 10
dor = ctrl.Consequent(np.arange(0, 11, 1), 'dor')

# Funções de Pertinência (3 termos justificados pelo domínio)
velocidade['lenta'] = fuzz.trimf(velocidade.universe, [0, 0, 5])
velocidade['normal'] = fuzz.trimf(velocidade.universe, [0, 5, 10])
velocidade['rapida'] = fuzz.trimf(velocidade.universe, [5, 10, 10])

expressao['neutra'] = fuzz.trimf(expressao.universe, [0, 0, 5])
expressao['tensa'] = fuzz.trimf(expressao.universe, [0, 5, 10])
expressao['intensa'] = fuzz.trimf(expressao.universe, [5, 10, 10])

dor['leve'] = fuzz.trimf(dor.universe, [0, 0, 5])
dor['moderada'] = fuzz.trimf(dor.universe, [0, 5, 10])
dor['severa'] = fuzz.trimf(dor.universe, [5, 10, 10])

# Base de regras
# 9 regras cobrindo o espaço de entradas
regras = [
    ctrl.Rule(velocidade['lenta'] & expressao['neutra'], dor['leve']),
    ctrl.Rule(velocidade['lenta'] & expressao['tensa'], dor['leve']),
    ctrl.Rule(velocidade['lenta'] & expressao['intensa'], dor['moderada']),
    
    ctrl.Rule(velocidade['normal'] & expressao['neutra'], dor['leve']),
    ctrl.Rule(velocidade['normal'] & expressao['tensa'], dor['moderada']),
    ctrl.Rule(velocidade['normal'] & expressao['intensa'], dor['severa']),
    
    ctrl.Rule(velocidade['rapida'] & expressao['neutra'], dor['moderada']),
    ctrl.Rule(velocidade['rapida'] & expressao['tensa'], dor['severa']),
    ctrl.Rule(velocidade['rapida'] & expressao['intensa'], dor['severa'])
]

# Controlador Mamdani
sistema_controle = ctrl.ControlSystem(regras)

