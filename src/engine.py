import collections
import collections.abc
collections.Mapping = collections.abc.Mapping

from experta import KnowledgeEngine, Rule, NOT
from src.models import ParametroSinal, Expressao, Contexto, Intencao, SignificadoFinal

class ClassificadorLibras(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.trace_decisoes = []

    # REGRAS DE NÍVEL 1: Deduzindo o contexto (parâmetro -> contexto)
    @Rule(ParametroSinal(mao="em_C", local="testa"))
    def contexto_cognitivo(self):
        motivo = "Regra Nível 1: Mão em 'C' na testa -> Contexto 'Cognitivo/Mental'"
        self.trace_decisoes.append(motivo)
        self.declare(Contexto(categoria="cognitivo"))

    @Rule(ParametroSinal(mao="aberta", local="peito"))
    def contexto_sentimento(self):
        motivo = "Regra Nível 1: Mão aberta no peito -> Contexto 'Sentimento/Emoção'"
        self.trace_decisoes.append(motivo)
        self.declare(Contexto(categoria="sentimento"))

    @Rule(ParametroSinal(mao="em_L", local="espaco_neutro"))
    def contexto_tempo(self):
        motivo = "Regra Nível 1: Mão em 'L' no espaço neutro -> Contexto 'Tempo/Calendário'"
        self.trace_decisoes.append(motivo)
        self.declare(Contexto(categoria="tempo"))

    # NÍVEL 2: Contexto + expressão -> intenção
    @Rule(Contexto(categoria="cognitivo"), Expressao(tipo="interrogativa"))
    def intencao_duvida_mental(self):
        motivo = "[R3] Contexto cognitivo e expressão interrogativa gera Intenção 'Dúvida Mental'"
        self.trace_decisoes.append(motivo)
        self.declare(Intencao(tipo="duvida_mental"))

    @Rule(Contexto(categoria="sentimento"), Expressao(tipo="dor_ou_tristeza"))
    def intencao_sofrimento(self):
        motivo = "[R4] Contexto Sentimento e Expressão Dor gera Intenção 'Sofrimento'"
        self.trace_decisoes.append(motivo)
        self.declare(Intencao(tipo="sofrimento"))

    # NÍVEL 3: Intenção + movimento -> significado final
    @Rule(Intencao(tipo="duvida_mental"), ParametroSinal(movimento="balancar_cabeca"))
    def significado_nao_entendi(self):
        motivo = "[R5] Dúvida Mental e Balançar cabeça significa 'Não entendi'"
        self.trace_decisoes.append(motivo)
        self.declare(SignificadoFinal(traducao="Não entendi / Estou confuso"))

    @Rule(Intencao(tipo="sofrimento"), ParametroSinal(movimento="apertar_peito"))
    def significado_angustia(self):
        motivo = "[R6] Sofrimento e Apertar o peito significa 'Angústia'"
        self.trace_decisoes.append(motivo)
        self.declare(SignificadoFinal(traducao="Angústia / Muita Tristeza"))

    # Níveis extras e resolução de conflito
    @Rule(ParametroSinal(mao="em_A", local="cabeca"))
    def contexto_saude(self):
        motivo = "[R7] Mão em 'A' na cabeça gera Contexto 'Saúde/Físico'"
        self.trace_decisoes.append(motivo)
        self.declare(Contexto(categoria="saude"))

    @Rule(Contexto(categoria="saude"), Expressao(tipo="dor_ou_tristeza"))
    def intencao_relato_dor(self):
        motivo = "[R8] Contexto Saúde e Expressão Dor gera Intenção 'Relato de Dor'"
        self.trace_decisoes.append(motivo)
        self.declare(Intencao(tipo="relato_dor"))

    @Rule(Intencao(tipo="relato_dor"), NOT(SignificadoFinal(traducao="Enxaqueca / Dor latejante")))
    def significado_dor_generica(self):
        motivo = "[R9] Relato de Dor simples significa 'Estou com dor de cabeça'"
        self.trace_decisoes.append(motivo)
        self.declare(SignificadoFinal(traducao="Estou com dor de cabeça"))

    @Rule(Intencao(tipo="relato_dor"), ParametroSinal(movimento="pulsante"), salience=100) 
    def significado_enxaqueca(self):
        motivo = "[R10] Relato de Dor e Movimento Pulsante [ALTA PRIORIDADE] -> 'Enxaqueca'"
        self.trace_decisoes.append(motivo)
        self.declare(SignificadoFinal(traducao="Enxaqueca / Dor latejante"))