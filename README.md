# Classificador Estrutural de Sinais em Libras

Este repositório contém um Sistema Baseado em Conhecimento (SBC) desenvolvido como miniprojeto para a disciplina de Sistemas Baseados em Conhecimento. O objetivo do sistema é classificar e traduzir sinais da Língua Brasileira de Sinais (Libras) a partir de parâmetros estruturais isolados, simulando o processamento de dados que poderiam advir de sensores computacionais, como câmeras ou luvas digitais.

O motor de inferência foi construído em Python utilizando a biblioteca experta, aplicando o método de encadeamento progressivo (forward chaining) estruturado em três níveis de abstração.

## Estrutura e Arquitetura do Domínio

O sistema processa os dados de entrada em camadas sequenciais até atingir uma tradução final:

1. Nível 1 (Parâmetros → Contexto): Recebe os fatos brutos das características físicas do sinal — Configuração de Mão (mao), Ponto de Articulação (local) e Movimento (movimento) — e deduz uma categoria de contexto inicial.

2. Nível 2 (Contexto + Expressão → Intenção): Associa o contexto deduzido no Nível 1 com a Expressão Facial ou Corporal (Expressao) do usuário para determinar a intenção subjacente.

3. Nível 3 (Intenção + Movimento → Significado Final): Combina a intenção inferida com o parâmetro de movimento para gerar a tradução do sinal para o português (SignificadoFinal).

## Modelagem dos Fatos (Fact)

● ParametroSinal: Contém os atributos físicos mao, local e movimento.

● Expressao: Contém o atributo tipo (ex: neutra, interrogativa, dor_ou_tristeza).

● Contexto: Fato intermediário contendo o atributo categoria.

● Intenção: Fato intermediário contendo o atributo tipo.

● SignificadoFinal: Output do sistema contendo a string de traducao.

## Base de Regras

O conhecimento especializado está mapeado em 10 regras de produção operadas pelo motor:

## Nível 1: Identificação de Contexto

● Regra 1 (Cognitivo): SE mão em 'C' E local na testa → Contexto: cognitivo.

● Regra 2 (Sentimento): SE mão aberta E local no peito → Contexto: sentimento.

● Regra 7 (Saúde): SE mão em 'A' E local na cabeça → Contexto: saude.

## Nível 2: Identificação de Intenção

● Regra 3 (Dúvida Mental): SE contexto cognitivo E expressão interrogativa → Intenção: duvida_mental.

● Regra 4 (Sofrimento): SE contexto sentimento E expressão dor_ou_tristeza → Intenção: sofrimento.

● Regra 8 (Relato de Dor): SE contexto saude E expressão dor_ou_tristeza → Intenção: relato_dor.

## Nível 3: Dedução do Significado Final e Resolução de Conflitos

● Regra 5 (Não entendi): SE intenção duvida_mental E movimento balancar_cabeca → Tradução: "Não entendi / Estou confuso".

● Regra 6 (Angústia): SE intenção sofrimento E movimento apertar_peito → Tradução: "Angústia / Muita Tristeza".

● Regra 9 (Dor Genérica): SE intenção relato_dor E NÃO houver o fato de tradução "Enxaqueca / Dor latejante" → Tradução: "Estou com dor de cabeça".

● Regra 10 (Enxaqueca): SE intenção relato_dor E movimento pulsante → Tradução: "Enxaqueca / Dor latejante" (Definida com salience=100).

## Casos de Teste e Validação

O sistema foi validado por meio de três cenários que simulam diferentes fluxos de execução da memória de trabalho:

## Caso de Teste 1: Encadeamento Simples (Tradução Base)

● Entradas: ParametroSinal(mao="em_C", local="testa", movimento="balancar_cabeca"), Expressao(tipo="interrogativa").

● Funcionamento: O motor realiza o encadeamento progressivo ativando sequencialmente as regras Regra 1, Regra 3 e Regra 5.

● Resultado: Tradução final deduzida como "Não entendi / Estou confuso".

## Caso de Teste 2: Resolução de Conflito com Atributo salience

● Entradas: ParametroSinal(mao="em_A", local="head", movimento="pulsante"), Expressao(tipo="dor_ou_tristeza").

● Funcionamento: As entradas ativam as regras de nível inicial Regra 7 e Regra 8. No Nível 3, cria-se um conflito entre a Regra 9 (genérica) e a Regra 10 (específica para enxaqueca). Graças ao parâmetro salience=100, a Regra 10 ganha prioridade na agenda de execução. Ao disparar, ela insere o significado final na memória, o que invalida a ativação da Regra 9 devido à restrição condicional NOT.

● Resultado: Tradução final deduzida como "Enxaqueca / Dor latejante".

## Caso de Teste 3: Ativação da Regra Genérica (Sem Conflito)

● Entradas: ParametroSinal(mao="em_A", local="cabeca", movimento="nenhum"), Expressao(tipo="dor_ou_tristeza").

● Funcionamento: Este caso avalia o comportamento padrão do sistema quando os parâmetros de movimento específicos não são satisfeitos. O sistema executa as Regras 7 e 8 normalmente, gerando a intenção de relato de dor. No Nível 3, como o movimento inserido é neutro (nenhum), as condições da Regra 10 não são preenchidas. Consequentemente, a Regra 9 é disparada de forma limpa por ser a regra genérica ativa para o contexto de dor.

● Resultado: Tradução final deduzida como "Estou com dor de cabeça".
