# Corretor Ortográfico Web

Este é um projeto de corretor ortográfico desenvolvido como parte da disciplina de Processamento de Linguagem Natural. O sistema funciona como um chatbot que verifica e corrige erros ortográficos em textos em português.

## Descrição

O sistema consiste em:
- Backend em Python usando Flask
- Frontend em HTML/JavaScript
- Corretor ortográfico baseado em:
  - Distância de Levenshtein para encontrar palavras similares
  - Corpus de referência para verificação estatística
  - Preservação de capitalização e pontuação

## Estrutura do Projeto
```
projeto/
  ├── app.py              # Aplicação Flask (servidor)
  ├── corretor.py         # Implementação do corretor ortográfico
  ├── vocab.txt          # Corpus de referência 
  └── templates/
      └── index.html     # Interface web
```

## Requisitos

- Python 3.x
- Flask

## Instalação

1. Clone o repositório ou baixe os arquivos
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Execução

1. Execute o servidor Flask:
```bash
python app.py
```

2. Acesse a aplicação em:
```
http://localhost:5000
```

## Uso

1. Digite um texto na caixa de texto
2. Clique em "Verificar"
3. O sistema irá:
   - Mostrar "Parabéns, sua frase está gramaticalmente correta" se não houver erros
   - Ou sugerir correções para palavras com possíveis erros ortográficos

## Tecnologias Utilizadas

- Python
- Flask
- HTML/JavaScript
- Algoritmo de Levenshtein
- Processamento de Linguagem Natural básico