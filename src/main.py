from src.engine import ClassificadorLibras
from src.models import ParametroSinal, Expressao, SignificadoFinal

def executar_teste(nome_teste, engine, fatos_iniciais):
    print(f"\n--- {nome_teste} ---")
    engine.reset()
    engine.trace_decisoes.clear()
    
    for fato in fatos_iniciais:
        engine.declare(fato)
        
    engine.run()
    
    print("Rastro de decisões (Trace):")
    for decisao in engine.trace_decisoes:
        print(f" -> {decisao}")
        
    print("\nTradução Final Encontrada:")
    traducao_encontrada = False
    for fato in engine.facts.values():
        if isinstance(fato, SignificadoFinal):
            print(f" {fato['traducao']}")
            traducao_encontrada = True
            
    if not traducao_encontrada:
        print(" Nenhuma tradução final deduzida.")

if __name__ == "__main__":
    motor = ClassificadorLibras()
    
    # Caso 1: Testando nível 1
    executar_teste(
        "TESTE 1: Nível 1 - Contexto Cognitivo", 
        motor, 
        [ParametroSinal(mao="em_C", local="testa", movimento="nenhum")]
    )
    
    # Caso 2: Intenção e Movimento
    executar_teste(
        "TESTE 2: Dúvida Mental", 
        motor, 
        [
            ParametroSinal(mao="em_C", local="testa", movimento="balancar_cabeca"),
            Expressao(tipo="interrogativa")
        ]
    )

    # Caso 3: Resolução de conflito com salience
    executar_teste(
        "TESTE 3: Conflito (Enxaqueca vs Dor Genérica)", 
        motor, 
        [
            ParametroSinal(mao="em_A", local="cabeca", movimento="pulsante"),
            Expressao(tipo="dor_ou_tristeza")
        ]
    )

    # Caso 4: Regra genérica (sem conflito)
    executar_teste(
        "TESTE 4: Dor Genérica", 
        motor, 
        [
            ParametroSinal(mao="em_A", local="cabeca", movimento="nenhum"),
            Expressao(tipo="dor_ou_tristeza")
        ]
    )