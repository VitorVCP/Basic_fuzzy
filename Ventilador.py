import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# entrada
temperatura = ctrl.Antecedent(np.arange(0, 41, 1), 'temperatura')
umidade = ctrl.Antecedent(np.arange(0, 101, 1), 'umidade')

# saída
ventilador = ctrl.Consequent(np.arange(0, 101, 1), 'ventilador')

# fuzzy da temperatura
temperatura['fria'] = fuzz.trimf(temperatura.universe, [0, 0, 20])
temperatura['media'] = fuzz.trimf(temperatura.universe, [15, 25, 35])
temperatura['quente'] = fuzz.trimf(temperatura.universe, [30, 40, 40])

# fuzzy da umidade
umidade['baixa'] = fuzz.trimf(umidade.universe, [0, 0, 50])
umidade['media'] = fuzz.trimf(umidade.universe, [25, 50, 75])
umidade['alta'] = fuzz.trimf(umidade.universe, [50, 100, 100])

# fuzzy do ventilador
ventilador['lento'] = fuzz.trimf(ventilador.universe, [0, 0, 50])
ventilador['medio'] = fuzz.trimf(ventilador.universe, [25, 50, 75])
ventilador['rapido'] = fuzz.trimf(ventilador.universe, [50, 100, 100])

# Regras
regra1 = ctrl.Rule(temperatura['fria'], ventilador['lento'])
regra2 = ctrl.Rule(temperatura['media'] & umidade['media'], ventilador['medio'])
regra3 = ctrl.Rule(temperatura['quente'] | umidade['alta'], ventilador['rapido'])

# Sistema fuzzy
controle_ventilador = ctrl.ControlSystem([regra1, regra2, regra3])
simulacao = ctrl.ControlSystemSimulation(controle_ventilador)

# Valores de entrada
simulacao.input['temperatura'] = 11
simulacao.input['umidade'] = 20

# Processamento
simulacao.compute()

# Resultado
print(f"Velocidade do ventilador: {simulacao.output['ventilador']:.2f}%")

# Mostrar gráfico
ventilador.view(sim=simulacao)

# Manter janela aberta
plt.show(block=True)

input("Pressione ENTER para sair...")