import flet as ft
from flet import *
from datetime import datetime
import json
import os

JSON_FILE = "emprestimos.json"

def main(page: ft.Page):
    page.title = "Empréstimo de Cabos"

    # Carrega os empréstimos do arquivo JSON ao iniciar
    def load_emprestimos():
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    # Salva os empréstimos no arquivo JSON
    def save_emprestimos():
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(emprestimos, f, ensure_ascii=False, indent=4)

    # Inicializa a lista de empréstimos carregando do arquivo
    emprestimos = load_emprestimos()
    cabos = ["1", "2", "3", "4", "5", "6", "7", "8"]

    def update_body(content):
        body_content.controls.clear()
        body_content.controls.append(content)  
        page.update()

    def get_cabos_disponiveis():
        disponiveis = [i["numCabo"] for i in emprestimos if i["status"] == "Ativo"]
        return [c for c in cabos if c not in disponiveis]

    def new_emprestimo(e):
        t = ft.Text()
        nome = ft.TextField(
            label="Nome",
            width=400
            )
        
        matricula = ft.TextField(
            label="Matrícula",
            width=400
            )
        
        numCabo = ft.Dropdown(
            label="Número do Cabo",
            options=[ft.dropdown.Option(c) for c in get_cabos_disponiveis()],
            width=205
            
        )

        def save_emprestimo(e):
            if not nome.value or not matricula.value or not numCabo.value:
                page.snack_bar = ft.SnackBar(ft.Text("Preencha todos os campos!"))
                page.snack_bar.open = True
                page.update()
                return

            cabo_emprestado = any(
                e["numCabo"] == numCabo.value and e["status"] == "Ativo" 
                for e in emprestimos
            )
    
            if cabo_emprestado:
                page.snack_bar = ft.SnackBar(ft.Text(f"Erro: O cabo {numCabo.value} já está emprestado!"))
                page.snack_bar.open = True
                page.update()
                return

            novo_emprestimo = {
                "nome": nome.value,
                "matricula": matricula.value,
                "numCabo": numCabo.value,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "status": "Ativo"
            }
            
            emprestimos.append(novo_emprestimo)
            save_emprestimos()  # Salva no arquivo JSON
            
            t.value = f"Registrado: '{nome.value}' - Cabo '{numCabo.value}'"
            page.update()

        button = ft.ElevatedButton(
            "Registrar",
            on_click=save_emprestimo,
        )

        update_body(
            ft.Column(
                controls=[
                    ft.Text("Novo Empréstimo", size=20, weight="bold"),
                    t, nome, matricula, numCabo, button
                ],
                spacing=10
            )
        )

    def devolucao_emprestimo(e):
        emprestimos_ativos = [i for i in emprestimos if i["status"] == "Ativo"]

        if not emprestimos_ativos:
            update_body(
                ft.Column(
                    controls=[
                        ft.Text("Devolução de Empréstimos", size=20, weight="bold"),
                        ft.Text("Não há empréstimos ativos no momento.", color="red")
                    ],
                    spacing=15
                )
            )
            return

        selection_cabos = ft.Dropdown(
            label="Selecione o cabo para devolução",
            options=[ft.dropdown.Option(f'{i["numCabo"]} - {i["nome"]}') for i in emprestimos_ativos],
            width=205
        )

        def confirm_devolucao(e):
            selected = selection_cabos.value
            if not selected:
                page.snack_bar = ft.SnackBar(ft.Text("Selecione um cabo para devolução!"))
                page.snack_bar.open = True
                page.update()
                return
            
            num_cabo = selected.split(" - ")[0]
            
            for emprestimo in emprestimos:
                if emprestimo["numCabo"] == num_cabo and emprestimo["status"] == "Ativo":
                    emprestimo["status"] = "Devolvido"
                    emprestimo["dataDevolucao"] = datetime.now().strftime("%d/%m/%Y %H:%M")
                    save_emprestimos()  # Salva no arquivo JSON
                    break
                
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Cabo {num_cabo} devolvido com sucesso!"),
                behavior=ft.SnackBarBehavior.FLOATING,
                action="OK",
                duration=3000
            )
            page.snack_bar.open = True
            page.update()
            devolucao_emprestimo(e)

        update_body(
            ft.Column(
                controls=[
                    ft.Text("Devolução de Empréstimos", size=20, weight="bold"),
                    selection_cabos,
                    ft.ElevatedButton(
                        "Confirmar Devolução",
                        on_click=confirm_devolucao,
                        color="white",
                        bgcolor="green"
                    )
                ],
                spacing=15
            )
        )
        
    def historico_emprestimo(e):
        rows = []
        current_row = ft.Row(spacing=20, wrap=True)

        if not emprestimos:
            update_body(
                ft.Column(
                    controls=[
                        ft.Text("Histórico de Empréstimo", size=20, weight="bold"),
                        ft.Text("Não há histórico no momento.", color="red")
                    ],
                    spacing=15
                )
            )
            return
        
        for i, emprestimo in enumerate(emprestimos):
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(f'Nome: {emprestimo["nome"]}'),
                            ft.Text(f'Matricula: {emprestimo["matricula"]}'),
                            ft.Text(f'Cabo: {emprestimo["numCabo"]}'),
                            ft.Text(f'Empréstimo: {emprestimo["data"]}'),
                            ft.Text(f'Devolução: {emprestimo.get("dataDevolucao", "Não devolvido")}'),
                            ft.Text(
                                f'Status: {emprestimo["status"]}',
                                color="green" if emprestimo['status'] == "Ativo" else "red"
                            )
                        ],
                    ),
                    margin=15,
                    width=300
                )
            )
            
            current_row.controls.append(card)
            
            if (i + 1) % 3 == 0:
                rows.append(current_row)
                current_row = ft.Row(spacing=20, wrap=True)
        
        if current_row.controls:
            rows.append(current_row)

        update_body(
            ft.Column(
                controls=[
                    ft.Text("Histórico de Empréstimos", size=20, weight="bold"),
                    *rows
                ],
                spacing=20,
                scroll="auto"
            )
        )
    
    def opcoes(e):
        if e.control.selected_index == 0:
            devolucao_emprestimo(e)
        elif e.control.selected_index == 1:
            historico_emprestimo(e)

    page.appbar = ft.AppBar(
        leading=ft.Container(
            content=ft.Image("Logo.png"),
            margin=ft.margin.only(left=20),
        ),
        title=ft.Text("Empréstimo Cabos DH", color=ft.Colors.WHITE),
        center_title=True,
        bgcolor= "#e02444",
        actions=[]
    )
    rail = ft.NavigationRail(
        selected_index=0,
        label_type= ft.NavigationRailLabelType.ALL,
        min_width=250,
        min_extended_width=550,
        leading=ft.FloatingActionButton(
            icon=ft.icons.CREATE, text="Novo Empréstimo", on_click=new_emprestimo
        ),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.SYNC_ROUNDED,
                selected_icon=icons.SYNC_ROUNDED,
                label="Devolução Empréstimo",
            ),
            ft.NavigationRailDestination(
                icon=icons.HISTORY_EDU_ROUNDED,
                selected_icon=icons.HISTORY_EDU,
                label="Historico Empréstimos",
            ),
        ],
        on_change=opcoes
    )

    body_content = ft.Column([ft.Text("Selecione uma opção no menu!")], expand=True)
        
    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                body_content,
            ],
            expand=True,
        )
    )

ft.app(target=main)