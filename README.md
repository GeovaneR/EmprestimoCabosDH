# 📍 Sistema de Empréstimo de Cabos - Dom Helder Centro Universitário

**Sistema desenvolvido como parte das atividades de estágio na Dom Helder Centro Universitário**


![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Flet](https://img.shields.io/badge/Flet-0.1.4-green)

## 📋 Sobre o Projeto

Sistema desenvolvido para o controle de empréstimos de cabos para alunos na Dom Helder Centro Universitário, como parte das atividades de estágio supervisionado.

**Orientador:** Yury Rhaian Nery 
**Estagiário:** Geovane Soares Ramos

**Período:** 30/04/2025 - 03/05/2025

## 🚀 Como Executar

### Pré-requisitos
- Python 3.7 ou superior
- Biblioteca Flet

```bash
pip install flet
```

### Instruções
1. Clone o repositório ou baixe os arquivos
2. Certifique-se que o arquivo "Logo.png" está na mesma pasta do script
3. Execute:

```bash
python emprestimo_cabos.py
```

## 🎯 Funcionalidades Principais

### ✨ Novo Empréstimo
- Cadastro de alunos com nome e matrícula
- Seleção de cabos disponíveis (1-9)
- Registro automático de data e hora

### 🔄 Devolução
- Seleção simplificada por cabo e nome do aluno
- Registro automático da data/hora de devolução
- Atualização instantânea do status

### 📜 Histórico Completo
- Visualização de todos os empréstimos realizados
- Status visual por cores (ativo/devolvido)
- Informações completas de cada transação
- Filtragem de empréstimos específicos por nome, matrícula ou número do cabo
- Permite remover empréstimos mediante autenticação por senha de administrador

## 🗃️ Estrutura de Dados

Os dados são armazenados em `emprestimos.json` seguindo o padrão:

```json
{
  "nome": "Nome do Aluno",
  "matricula": "D12345",
  "numCabo": "3",
  "data": "03/05/2025 14:30",
  "status": "Ativo",
  "dataDevolucao": "04/05/2025 09:15"
}
```

## ⚙️ Configuração Institucional

Os parâmetros estão ajustados para atender às normas da Dom Helder:

```python
# Configurações específicas Dom Helder
COR_PRIMARIA = "#e02444"  # Vermelho institucional
CABOS_DISPONIVEIS = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
```

## 📌 Termos de Uso

- Sistema desenvolvido exclusivamente para uso interno da Dom Helder
- Dados são armazenados localmente conforme política de segurança da instituição
- Uso autorizado apenas por funcionários do setor responsável

## 📞 Suporte Técnico

Setor de TI - Dom Helder Centro Universitário  
📞 (31) 2125-8800  
📧 geovane.ramos@domhelder.edu.br  

---

**Desenvolvido por** Geovane Soares Ramos
**Estagiário de** Ciência da Computação 
**Copyright** - © 2025  
*"Sapientia et Virtus"*
