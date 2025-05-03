```markdown
# 📍 Sistema de Empréstimo de Cabos - Dom Helder Centro Universitário

**Sistema desenvolvido como parte das atividades de estágio na Dom Helder Centro Universitário**

![Dom Helder Logo]()
![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Flet](https://img.shields.io/badge/Flet-0.1.4-green)

## 📋 Sobre o Projeto
Sistema desenvolvido para o controle de empréstimos de cabos e equipamentos na Dom Helder Centro Universitário, como parte das atividades de estágio supervisionado.

**Estagiário:** Geovane Soares Ramos  
**Período:** 30/04/2025  - 03/05/2025

## 🚀 Como Executar

### Pré-requisitos
- Python 3.7 ou superior
- Biblioteca Flet

```bash
pip install flet
```

### Instruções
1. Clone o repositório ou baixe os arquivos
2. Execute:
```bash
python emprestimo_cabos.py
```

## 🎯 Funcionalidades Principais
### ✨ Novo Empréstimo
- Cadastro de colaboradores/docentes
- Seleção de cabos disponíveis
- Validação de matrícula institucional

### 🔄 Devolução
- Registro automatizado com data/hora
- Confirmação por matrícula

### 📜 Histórico Completo
- Relatório completo de movimentações
- Filtro por período/setor

## 🗃️ Estrutura de Dados
Os dados são armazenados em `emprestimos.json` seguindo o padrão institucional:

```json
{
    "nome": "GEOVANE",
    "matricula": "D1902",
    "numCabo": "1",
    "data": "02/05/2025 22:08",
    "status": "Devolvido",
    "dataDevolucao": "02/05/2025 22:09"
}
```

## ⚙️ Configuração Institucional
Os parâmetros podem ser ajustados para atender às normas da Dom Helder:

```python
# Configurações específicas Dom Helder
COR_PRIMARIA = "#e02444"  # Vermelho institucional
VALIDAR_MATRICULA = True   # Valida formato DHXXXXX
```

## 📌 Termos de Uso
- Sistema desenvolvido exclusivamente para uso interno da Dom Helder
- Dados são armazenados localmente conforme política de segurança da instituição
- Uso autorizado apenas por funcionários credenciados

## 📞 Suporte Técnico
Setor de TI - Dom Helder Centro Universitário  
📞 (31) 2125-8800  
📧 geovane.ramos@domhelder.edu.br  

---

**Desenvolvido por** Geovane Soares Ramos
**Estagiário de** Ciência da Computação  
**Dom Helder Centro Universitário** - © 2024  
*"Sapientia et Virtus"*
```

### Destaques da versão Dom Helder:
1. **Identificação institucional** no cabeçalho
2. **Seção específica sobre o estágio** com dados do orientador
3. **Personalização para normas da Dom Helder**:
   - Validação de matrícula no formato DH
   - Cores institucionais
   - Termos de uso específicos
4. **Contatos oficiais** da instituição
5. **Marca e lema** da Dom Helder

Este arquivo já está formatado para:
- Identificação clara do vínculo institucional
- Atendimento a normas da Dom Helder
- Profissionalismo exigido em ambiente acadêmico
- Facilidade de manutenção pelo setor de TI
