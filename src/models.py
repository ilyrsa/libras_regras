from experta import Fact

class ParametroSinal(Fact):
    """
    Recebe os dados físicos do sinal bruto.
    Campos esperados: mao (configuração), local (ponto de articulação), movimento.
    """
    pass

class Expressao(Fact):
    """
    Recebe a expressão do rosto ou corporal.
    Campos esperados: tipo (exemplos: neutra, interrogativa, dor).
    """
    pass

class Contexto(Fact):
    """
    Fato intermediário (Nível 2). Gerado após interpretar os parâmetros físicos.
    Campos esperados: categoria (exemplos: tempo, sentimento, cognitivo).
    """
    pass

class Intencao(Fact):
    pass

class SignificadoFinal(Fact):
    """
    A saída final do sistema (Nível 3).
    Campos esperados: traducao (a palavra ou frase em português).
    """
    pass