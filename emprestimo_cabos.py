import flet as ft
from flet import *
from datetime import datetime, timedelta
import json
import os
import re
import time
import threading
from typing import List, Dict, Optional, Set

# ===== CONSTANTES =====
JSON_FILE = "emprestimos.json"
CABOS_DISPONIVEIS = ["1", "2", "3", "4", "5", "6", "7", "8"]
TEMPO_EMPRESTIMO_EXPIRADO = 10  # 30 minutos em segundos

# ===== FUNÇÕES DE DADOS =====
def carregar_emprestimos() -> List[Dict]:
    """Carrega empréstimos do arquivo JSON."""
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def salvar_emprestimos(emprestimos: List[Dict]) -> None:
    """Salva empréstimos no arquivo JSON."""
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(emprestimos, f, ensure_ascii=False, indent=4)

# ===== FUNÇÕES DE VALIDAÇÃO =====
def validar_matricula(matricula: str) -> bool:
    """Valida formato da matrícula (ex: e12345 ou d54321)."""
    return re.match(r'^[ed]\d{5}$', matricula.lower()) is not None

def formatar_matricula(matricula: str) -> str:
    """Garante que a matrícula está em minúsculas (ex: e12345)."""
    if matricula and matricula[0].isalpha():
        return matricula[0].lower() + matricula[1:]
    return matricula

# ===== LÓGICA DE EMPRÉSTIMOS =====
def cabos_disponiveis(emprestimos: List[Dict]) -> List[str]:
    """Retorna cabos não emprestados."""
    emprestados = [e["numCabo"] for e in emprestimos if e["status"] == "Ativo"]
    return [c for c in CABOS_DISPONIVEIS if c not in emprestados]

def emprestimo_expirado(emprestimo: Dict) -> bool:
    """Verifica se um empréstimo está expirado."""
    if emprestimo["status"] != "Ativo":
        return False
    data_emprestimo = datetime.strptime(emprestimo["data"], "%d/%m/%Y %H:%M")
    tempo_decorrido = (datetime.now() - data_emprestimo).total_seconds()
    return tempo_decorrido >= TEMPO_EMPRESTIMO_EXPIRADO

# ===== THREAD DE VERIFICAÇÃO =====
def verificar_emprestimos_expirados(page: ft.Page, emprestimos: List[Dict], stop_event: threading.Event):
    """Verifica empréstimos expirados em segundo plano."""
    alertas_mostrados: Set[str] = set()
    while not stop_event.is_set():
        time.sleep(60)  # Verifica a cada 1 minuto
        for emprestimo in emprestimos:
            if emprestimo_expirado(emprestimo):
                id_emprestimo = f"{emprestimo['numCabo']}-{emprestimo['data']}"
                if id_emprestimo not in alertas_mostrados:
                    alertas_mostrados.add(id_emprestimo)
                    mostrar_alerta_expiração(page, emprestimo)

def mostrar_alerta_expiração(page: ft.Page, emprestimo: Dict):
    """Mostra alerta de empréstimo expirado."""
    dlg = ft.AlertDialog(
        title=ft.Text("Alerta de Empréstimo"),
        content=ft.Text(f"ATENÇÃO: O cabo {emprestimo['numCabo']} - {emprestimo['nome']} expirou!"),
        )
    page.open(dlg)
    page.update()

# ===== INTERFACE DO USUÁRIO =====
def criar_app_bar() -> ft.AppBar:
    """Cria a barra superior do app."""
    return ft.AppBar(
        leading=ft.Container(ft.Image("Logo.png"), margin=ft.margin.only(left=20)),
        title=ft.Text("Empréstimo Cabos DH", color=ft.Colors.WHITE),
        center_title=True,
        bgcolor="#e02444",
    )

def criar_navigation_rail(on_nav_change, page: ft.Page, emprestimos: List[Dict], body_content: ft.Column) -> ft.NavigationRail:
    """Cria o menu lateral de navegação."""
    return ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=250,
        min_extended_width=550,
        leading=ft.FloatingActionButton(
            icon=ft.icons.CREATE_OUTLINED,
            text="Novo Empréstimo",
            on_click=lambda e: mostrar_tela_novo_emprestimo(e, page, emprestimos, body_content),
        ),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(icon=ft.icons.SYNC_OUTLINED, label="Devolução"),
            ft.NavigationRailDestination(icon=ft.icons.HISTORY_OUTLINED, label="Histórico"),
        ],
        on_change=on_nav_change,
    )

# ===== TELAS DA APLICAÇÃO =====
def mostrar_tela_novo_emprestimo(e, page: ft.Page, emprestimos: List[Dict], body_content: ft.Column):
    """Mostra o formulário de novo empréstimo."""
    t = ft.Text()
    nome = ft.TextField(label="Nome", width=400, autofocus=True)
    matricula = ft.TextField(
        label="Matrícula",
        width=400,
        hint_text="Ex: e12345 ou d54321",
        input_filter=ft.InputFilter(allow=True, regex_string=r"[edED0-9]", replacement_string=""),
        max_length=6,
        on_change=lambda e: validar_e_formatar_matricula(e),
    )
    num_cabo = ft.Dropdown(
        label="Código do Cabo",
        options=[ft.dropdown.Option(c) for c in cabos_disponiveis(emprestimos)],
        width=205,
    )

    def validar_e_formatar_matricula(e):
        """Valida e formata a matrícula em tempo real."""
        matricula.value = formatar_matricula(matricula.value)
        if not validar_matricula(matricula.value):
            matricula.error_text = "Formato inválido (ex: e12345 ou d54321)"
        else:
            matricula.error_text = None
        matricula.update()
    
    def registrar_emprestimo(e):
        """Registra um novo empréstimo."""
        if not nome.value or not matricula.value or not num_cabo.value:
            page.open(ft.SnackBar(ft.Text("Preencha todos os campos!", text_align="center")))
            page.update()
            return

        if not validar_matricula(matricula.value):
            page.open(ft.SnackBar(ft.Text("Matrícula inválida!",text_align="center")))
            page.update()
            return

        novo_emprestimo = {
            "nome": nome.value,
            "matricula": matricula.value,
            "numCabo": num_cabo.value,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "status": "Ativo"
        }
        emprestimos.append(novo_emprestimo)
        salvar_emprestimos(emprestimos)

        t.value = f"Registrado: {nome.value} - Cabo {num_cabo.value}"
        page.update()

    body_content.controls = [
        ft.Text("Novo Empréstimo", size=20, weight="bold"),
        t, nome, matricula, num_cabo,
        ft.ElevatedButton("Registrar", on_click=registrar_emprestimo),
    ]
    page.update()

def mostrar_tela_devolucao(e, page: ft.Page, emprestimos: List[Dict], body_content: ft.Column):
    """Mostra a tela de devolução de empréstimos."""
    emprestimos_ativos = [e for e in emprestimos if e["status"] == "Ativo"]

    if not emprestimos_ativos:
        body_content.controls = [
            ft.Text("Devolução", size=20, weight="bold"),
            ft.Text("Nenhum empréstimo ativo.", color="red"),
        ]
        page.update()
        return

    dropdown_cabos = ft.Dropdown(
        label="Selecione o cabo para devolução",
        options=[ft.dropdown.Option(f"{e['numCabo']} - {e['nome']}") for e in emprestimos_ativos],
        width=400,
    )

    def confirmar_devolucao(e):
        selected = dropdown_cabos.value
        if not selected:
            page.open(ft.SnackBar(ft.Text("Selecione um cabo!", text_align="center")))
            page.update()
            return

        num_cabo = selected.split(" - ")[0]
        for e in emprestimos:
            if e["numCabo"] == num_cabo and e["status"] == "Ativo":
                e["status"] = "Devolvido"
                e["dataDevolucao"] = datetime.now().strftime("%d/%m/%Y %H:%M")
                salvar_emprestimos(emprestimos)
                break

        page.open(ft.SnackBar(ft.Text(f"Cabo {num_cabo} devolvido!", text_align="center")))
        print(f"Cabo {num_cabo} devolvido!")
        page.update()
        mostrar_tela_devolucao(e, page, emprestimos, body_content)

    body_content.controls = [
        ft.Text("Devolução", size=20, weight="bold"),
        dropdown_cabos,
        ft.ElevatedButton("Confirmar Devolução", on_click=confirmar_devolucao, bgcolor="green"),
    ]
    page.update()

def mostrar_tela_historico(e, page: ft.Page, emprestimos: List[Dict], body_content: ft.Column):
    """Mostra o histórico em 3 cards por linha com scroll."""
    if not emprestimos:
        body_content.controls = [
            ft.Text("Histórico", size=20, weight="bold"),
            ft.Text("Nenhum empréstimo registrado.", color="red"),
        ]
        page.update()
        return

    # Cria os cartões organizados em linhas de 3
    cards = []
    current_row = ft.Row(spacing=20, wrap=True)  # Quebra automaticamente em várias linhas

    for i, emprestimo in enumerate(emprestimos):
        expirado = emprestimo_expirado(emprestimo)
        card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(f"Nome: {emprestimo['nome']}"),
                    ft.Text(f"Matrícula: {emprestimo['matricula']}"),
                    ft.Text(f"Cabo: {emprestimo['numCabo']}"),
                    ft.Text(f"Data: {emprestimo['data']}"),
                    ft.Text(f"Devolução: {emprestimo.get('dataDevolucao', 'Pendente')}"),
                    ft.Text(
                        f"Status: {emprestimo['status']}" + (" (Expirado)" if expirado else ""),
                        color="orange" if expirado else ("green" if emprestimo['status'] == "Ativo" else "red"),
                    ),
                ]),
                margin=10,
                padding=10,
                width=300,  # Largura fixa para cada card
            )
        )

        current_row.controls.append(card)

        # Quebra a linha a cada 3 cards
        if (i + 1) % 3 == 0:
            cards.append(current_row)
            current_row = ft.Row(spacing=20, wrap=True)

    # Adiciona a última linha (se não estiver completa)
    if current_row.controls:
        cards.append(current_row)

    # Adiciona scroll à coluna principal
    body_content.controls = [
        ft.Text("Histórico de Empréstimos", size=20, weight="bold"),
        ft.Column(
            controls=cards,
            scroll="auto",  # Habilita a rolagem
            expand=True,    # Ocupa todo o espaço vertical
        ),
    ]
    page.update()


# ===== FUNÇÃO PRINCIPAL =====
def main(page: ft.Page):
    page.title = "Empréstimo de Cabos"
    emprestimos = carregar_emprestimos()
    page.window.maximized = True  
    page.window.width = 1350

    # Thread para verificar empréstimos expirados
    stop_event = threading.Event()
    threading.Thread(
        target=verificar_emprestimos_expirados,
        args=(page, emprestimos, stop_event),
        daemon=True,
    ).start()

    # Configuração da UI
    page.appbar = criar_app_bar()
    body_content = ft.Column([ft.Text("Selecione uma opção no menu!")], expand=True)

    def on_nav_change(e):
        if e.control.selected_index == 0:
            mostrar_tela_devolucao(e, page, emprestimos, body_content)
        elif e.control.selected_index == 1:
            mostrar_tela_historico(e, page, emprestimos, body_content)

    rail = criar_navigation_rail(on_nav_change, page, emprestimos, body_content)

    page.add(
        ft.Row([rail, ft.VerticalDivider(width=1), body_content], expand=True)
    )

    # Encerra a thread ao fechar o app
    page.on_close = lambda: stop_event.set()


ft.app(target=main)