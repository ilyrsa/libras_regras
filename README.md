# Classificador Estrutural de Sinais em Libras

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![Experta](https://img.shields.io/badge/Library-Experta-blue?style=for-the-badge)

> Este é um Sistema Especialista baseado em regras criado para inferir e traduzir o significado de sinais da Língua Brasileira de Sinais (Libras) a partir de parâmetros físicos e expressões faciais/corporais.

## Sumário
- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Estrutura e Arquitetura do Domínio](#-estrutura-e-arquitetura-do-domínio)
- [Modelagem dos Fatos](#-modelagem-dos-fatos)
- [Base de Regras](#-base-de-regras)
- [Casos de Teste e Validação](#-casos-de-teste-e-validação)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Como Executar](#-como-executar)
- [Autores](#-autores)

## Sobre o Projeto
Este projeto foi construído utilizando a biblioteca `experta` para modelar o domínio da Libras. O sistema recebe dados brutos simulados (como configuração de mão, ponto de articulação, movimento e expressão) e, por meio de um raciocínio em três níveis, deduz o contexto, a intenção e, por fim, traduz o sinal para o português.

## Funcionalidades
* **Inferência em Níveis:** Dedução progressiva de Contexto (Nível 1), Intenção (Nível 2) e Significado Final (Nível 3).
* **Resolução de Conflitos:** Uso de prioridades (`salience`) para diferenciar sinais parecidos (ex: distinguir uma dor de cabeça genérica de uma enxaqueca com base no tipo de movimento).
* **Trace de Decisões:** Rastreamento completo dos motivos e regras que foram ativadas até chegar à tradução final, permitindo auditoria do motor de inferência.

## Estrutura e Arquitetura do Domínio
O sistema processa os dados de entrada em camadas sequenciais até atingir uma tradução final:

1. **Nível 1 (Parâmetros → Contexto):** Recebe os fatos brutos das características físicas do sinal — Configuração de Mão (`mao`), Ponto de Articulação (`local`) e Movimento (`movimento`) — e deduz uma categoria de contexto inicial.
2. **Nível 2 (Contexto + Expressão → Intenção):** Associa o contexto deduzido no Nível 1 com a Expressão Facial ou Corporal (`Expressao`) do usuário para determinar a intenção subjacente.
3. **Nível 3 (Intenção + Movimento → Significado Final):** Combina a intenção inferida com o parâmetro de movimento para gerar a tradução do sinal para o português (`SignificadoFinal`).

## Modelagem dos Fatos (Fact)
* **`ParametroSinal`:** Contém os atributos físicos `mao`, `local` e `movimento`.
* **`Expressao`:** Contém o atributo `tipo` (ex: neutra, interrogativa, dor_ou_tristeza).
* **`Contexto`:** Fato intermediário contendo o atributo `categoria`.
* **`Intencao`:** Fato intermediário contendo o atributo `tipo`.
* **`SignificadoFinal`:** Output do sistema contendo a string de `traducao`.

## Base de Regras
O conhecimento especializado está mapeado em 10 regras de produção operadas pelo motor:

### Nível 1: Identificação de Contexto
* **Regra 1 (Cognitivo):** SE mão em 'C' E local na testa → Contexto: cognitivo.
* **Regra 2 (Sentimento):** SE mão aberta E local no peito → Contexto: sentimento.
* **Regra 7 (Saúde):** SE mão em 'A' E local na cabeça → Contexto: saude.

### Nível 2: Identificação de Intenção
* **Regra 3 (Dúvida Mental):** SE contexto cognitivo E expressão interrogativa → Intenção: duvida_mental.
* **Regra 4 (Sofrimento):** SE contexto sentimento E expressão dor_ou_tristeza → Intenção: sofrimento.
* **Regra 8 (Relato de Dor):** SE contexto saude E expressão dor_ou_tristeza → Intenção: relato_dor.

### Nível 3: Dedução do Significado Final e Resolução de Conflitos
* **Regra 5 (Não entendi):** SE intenção duvida_mental E movimento balancar_cabeca → Tradução: "Não entendi / Estou confuso".
* **Regra 6 (Angústia):** SE intenção sofrimento E movimento apertar_peito → Tradução: "Angústia / Muita Tristeza".
* **Regra 9 (Dor Genérica):** SE intenção relato_dor E NÃO houver o fato de tradução "Enxaqueca / Dor latejante" → Tradução: "Estou com dor de cabeça".
* **Regra 10 (Enxaqueca):** SE intenção relato_dor E movimento pulsante → Tradução: "Enxaqueca / Dor latejante" *(Definida com `salience=100`)*.

## Casos de Teste e Validação
O sistema foi validado por meio de três cenários que simulam diferentes fluxos de execução da memória de trabalho:

### Caso de Teste 1: Encadeamento Simples (Tradução Base)
* **Entradas:** `ParametroSinal(mao="em_C", local="testa", movimento="balancar_cabeca")`, `Expressao(tipo="interrogativa")`.
* **Funcionamento:** O motor realiza o encadeamento progressivo ativando sequencialmente a Regra 1, Regra 3 e Regra 5.
* **Resultado:** Tradução final deduzida como "Não entendi / Estou confuso".

### Caso de Teste 2: Resolução de Conflito com Atributo salience
* **Entradas:** `ParametroSinal(mao="em_A", local="cabeca", movimento="pulsante")`, `Expressao(tipo="dor_ou_tristeza")`.
* **Funcionamento:** As entradas ativam as regras de nível inicial Regra 7 e Regra 8. No Nível 3, cria-se um conflito entre a Regra 9 (genérica) e a Regra 10 (específica para enxaqueca). Graças ao parâmetro `salience=100`, a Regra 10 ganha prioridade na agenda de execução. Ao disparar, ela insere o significado final na memória, o que invalida a ativação da Regra 9 devido à restrição condicional `NOT`.
* **Resultado:** Tradução final deduzida como "Enxaqueca / Dor latejante".

### Caso de Teste 3: Ativação da Regra Genérica (Sem Conflito)
* **Entradas:** `ParametroSinal(mao="em_A", local="cabeca", movimento="nenhum")`, `Expressao(tipo="dor_ou_tristeza")`.
* **Funcionamento:** Este caso avalia o comportamento padrão do sistema quando os parâmetros de movimento específicos não são satisfeitos. O sistema executa as Regras 7 e 8 normalmente, gerando a intenção de relato de dor. No Nível 3, como o movimento inserido é neutro (nenhum), as condições da Regra 10 não são preenchidas. Consequentemente, a Regra 9 é disparada de forma limpa por ser a regra genérica ativa para o contexto de dor.
* **Resultado:** Tradução final deduzida como "Estou com dor de cabeça".

## Estrutura do Repositório
O projeto foi refatorado e modularizado para facilitar a manutenção e escalabilidade:

- `src/models.py`: Definição das classes de Fatos (`ParametroSinal`, `Expressao`, `Contexto`, etc.) usadas pelo motor clássico.
- `src/engine.py`: O Motor de Inferência Base (`ClassificadorLibras`) contendo todas as regras lógicas nítidas (crisp).
- `src/main.py`: Ponto de entrada do sistema clássico contendo os casos de teste práticos.
- `src/fuzzy_engine.py`: O Controlador Fuzzy contendo a modelagem das variáveis linguísticas (Mamdani) e regras de intensidade.
- `src/fuzzy_main.py`: Ponto de entrada do simulador fuzzy, responsável pelos testes de limite, defuzzificação e interpretação clínica.
- `requirements.txt`: Dependências unificadas necessárias para a execução do projeto (incluindo `experta` e `scikit-fuzzy`).

## Mini-Projeto 2 (Controlador Fuzzy)
Como evolução do domínio (Caminho B), o projeto agora conta com um Controlador Fuzzy (Mamdani) focado em quantificar a **Intensidade da Dor** em sinais de saúde. 
Enquanto o motor de inferência nítido (experta) avalia se é "Dor Genérica" ou "Enxaqueca", o motor Fuzzy analisa graus de fluidez:
* **Entradas:** `velocidade` do movimento (0-10) e tensão da `expressao` facial (0-10).
* **Saída Defuzzificada:** Intensidade da `dor` (0-10), variando de leve a enxaqueca severa.
* **Base de Regras:** 9 regras fuzzy que cobrem 100% do espaço de inferência sem lacunas.

## Como Executar

Siga os passos abaixo para rodar os testes do motor de inferência localmente:

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/ilyrsa/libras_regras.git](https://github.com/ilyrsa/libras_regras.git)
   cd libras_regras

2. **Crie e ative um ambiente virtual (Recomendado):**
   ```bash
   python -m venv venv

    # No Linux/Mac:
    source venv/bin/activate  

    # No Windows:
    venv\Scripts\activate

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt

   
4. **Execute o sistema:**
   ```bash
   python -m src.main

### Como Executar o Controlador Fuzzy
Após ativar seu ambiente virtual e instalar as dependências do `requirements.txt`, execute o simulador fuzzy com os 3 casos de teste comentados:
    ```bash
    python -m src.fuzzy_main
    ```

---

## Autores

Desenvolvido por [@ilyrsa](https://github.com/ilyrsa) e [@luislrl](https://github.com/luislrl).

---
