from skfuzzy import control as ctrl
from src.fuzzy_engine import sistema_controle

def executar_caso_teste(nome, vel, expr):
    print(f"\n--- {nome} ---")
    print(f"Entradas -> Velocidade: {vel}/10 | Expressão Facial: {expr}/10")

    # Simulacao e injecao de entradas
    simulacao = ctrl.ControlSystemSimulation(sistema_controle)
    simulacao.input['velocidade'] = vel
    simulacao.input['expressao'] = expr

    # Processa inferencia e defuzzificacao
    simulacao.compute()
    resultado = simulacao.output['dor']
    
    print(f"Saída Defuzzificada (Intensidade da Dor): {resultado:.2f}/10")

    # Interpretaacao comentada
    if resultado <= 3.5:
        print("Interpretação: Dor de cabeça muito leve, apenas um incômodo passageiro.")
    elif resultado <= 7.0:
        print("Interpretação: Dor moderada, sinalizando uma dor de cabeça contínua.")
    else:
        print("Interpretação: Caso extremo de dor, sinalizando uma Enxaqueca Severa.")

if __name__ == "__main__":
    print("Iniciando Controlador Fuzzy (Mamdani) - Domínio: Libras (Intensidade de Dor)")
    
    # Caso 1: Movimento lento, rosto neutro
    executar_caso_teste("CASO 1: Sinal Suave", vel=2.0, expr=2.0)
    
    # Caso 2: Movimento normal, rosto muito tenso
    executar_caso_teste("CASO 2: Expressão de Desconforto", vel=5.0, expr=8.0)
    
    # Caso 3: Movimento rápido, rosto muito
    executar_caso_teste("CASO 3: Relato de Enxaqueca", vel=9.5, expr=9.5)

