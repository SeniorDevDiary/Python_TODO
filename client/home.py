from nicegui import ui
import httpx

API_BASE = "http://localhost:8000"

todos = []

def refresh_todos():
    global todos
    response = httpx.get(f"{API_BASE}/todos/")
    if response.status_code == 200:
        todos = response.json()
        update_todo_list()

def update_todo_list():
    todo_container.clear()
    for todo in todos:
        with todo_container:
            with ui.row().classes('items-center'):
                ui.label(todo['title']).style('min-width: 200px')
                ui.button('❌', on_click=lambda t=todo: delete_todo(t['id']))

def add_todo(title: str):
    response = httpx.post(f"{API_BASE}/todos/", json={
        "title": title,
        "description": ""
    })
    if response.status_code == 200:
        refresh_todos()

def delete_todo(todo_id: int):
    response = httpx.delete(f"{API_BASE}/todos/{todo_id}")
    if response.status_code == 200:
        refresh_todos()

ui.label('📝 TODO App (NiceGUI + FastAPI)').classes('text-2xl font-bold')

with ui.row():
    new_title = ui.input(placeholder='Enter a todo title').style('width: 300px')
    ui.button('Add', on_click=lambda: add_todo(new_title.value))

todo_container = ui.column()
refresh_todos()

ui.run()
