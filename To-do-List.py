import tkinter as tk
from tkinter import messagebox
import os

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ту-Ду-Лист")
        # Папка для хранения задач
        self.tasks_folder = "tasks"
        os.makedirs(self.tasks_folder, exist_ok=True)  # Создаём папку, если она не существует
        # Список для хранения задач
        self.tasks = []
        # Создание фрейма для ввода новой задачи
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)
        # Создание списка задач (Listbox) для отображения задач
        self.task_listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE, width=60, height=15)
        self.task_listbox.pack(pady=10)
        # Поле ввода для новой задачи
        self.task_entry = tk.Entry(self.frame, width=40)
        self.task_entry.pack(side=tk.LEFT, padx=10)
        self.task_entry.bind('<Return>', self.add_task)
        # Кнопка для добавления задачи
        self.add_task_button = tk.Button(self.frame, text="Это нам надо!", command=self.add_task)
        self.add_task_button.pack(side=tk.LEFT)
        # Кнопка для удаления выполненных задач
        self.complete_task_button = tk.Button(self.root, text="Это нам больше не нужно!", command=self.delete_completed_tasks)
        self.complete_task_button.pack(pady=10)
        # Привязка клавиши DEL для удаления задач
        self.root.bind('<Delete>', self.delete_completed_tasks)
        # Загрузка задач из файлов при запуске
        self.load_tasks()
        # Закрытие приложения с сохранением задач
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def add_task(self, event=None):
        task_text = self.task_entry.get()
        if task_text:
            # Заменяем недопустимые символы в имени файла
            safe_task_name = ''.join(c for c in task_text if c.isalnum() or c in (' ', '_')).rstrip()
            task_filename = os.path.join(self.tasks_folder, f"{safe_task_name}.txt")
            with open(task_filename, 'w') as file:
                file.write(task_text)  # Сохраняем задачу в отдельный файл
            self.tasks.append(task_text)  # Добавляем текст задачи в список
            self.update_task_list()  # Обновляем отображение задач
            self.task_entry.delete(0, tk.END)  # Очищаем поле ввода
        else:
            messagebox.showwarning("ВНИМАНИЕ!!!!!!", "Ты хоть что-то написал бы!")

    def delete_completed_tasks(self, event=None):
        selected_indices = self.task_listbox.curselection()
        if selected_indices:
            for index in reversed(selected_indices):
                task_filename = os.path.join(self.tasks_folder, f"{self.tasks[index]}.txt")
                if os.path.exists(task_filename):
                    os.remove(task_filename)  # Удаляем файл задачи
                del self.tasks[index]  # Удаляем задачу из списка
            self.update_task_list()  # Обновляем отображение задач
        else:
            messagebox.showwarning("ВНИМАНИЕ!!!!!!", "А что удалять то?")

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)  # Очищаем Listbox перед обновлением
        for i, task in enumerate(self.tasks):
            task_numbered = f"{i + 1}. {task}"  # Нумеруем задачи
            self.task_listbox.insert(tk.END, task_numbered)  # Добавляем каждую задачу в Listbox

    def load_tasks(self):
        for filename in os.listdir(self.tasks_folder):
            if filename.endswith('.txt'):
                with open(os.path.join(self.tasks_folder, filename), 'r') as file:
                    task_text = file.read().strip()
                    self.tasks.append(task_text)  # Загружаем задачу из файла
        self.update_task_list()  # Обновляем отображение задач

    def on_closing(self):
        self.root.destroy()  # Закрываем приложение

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()


