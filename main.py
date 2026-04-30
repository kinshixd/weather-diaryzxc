import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")

        # Поля ввода
        self.date_label = tk.Label(root, text="Дата (YYYY-MM-DD):")
        self.date_label.pack()
        self.date_entry = tk.Entry(root)
        self.date_entry.pack()

        self.temp_label = tk.Label(root, text="Температура (°C):")
        self.temp_label.pack()
        self.temp_entry = tk.Entry(root)
        self.temp_entry.pack()

        self.desc_label = tk.Label(root, text="Описание погоды:")
        self.desc_label.pack()
        self.desc_entry = tk.Entry(root)
        self.desc_entry.pack()

        self.precip_label = tk.Label(root, text="Осадки (да/нет):")
        self.precip_label.pack()
        self.precip_entry = tk.Entry(root)
        self.precip_entry.pack()

        self.add_button = tk.Button(root, text="Добавить запись", command=self.add_entry)
        self.add_button.pack()

        self.entries = []
        self.load_from_json()

    def add_entry(self):
        date = self.date_entry.get()
        try:
            datetime.strptime(date, '%Y-%m-%d')  # Проверка формата даты
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат даты. Используйте YYYY-MM-DD.")
            return

        try:
            temperature = float(self.temp_entry.get())  # Проверка температуры
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом.")
            return

        description = self.desc_entry.get()
        if not description:
            messagebox.showerror("Ошибка", "Описание не должно быть пустым.")
            return

        precipitation = self.precip_entry.get().lower() in ['да', 'true', '1']

        entry = {
            "date": date,
            "temperature": temperature,
            "description": description,
            "precipitation": precipitation
        }

        self.entries.append(entry)
        messagebox.showinfo("Успех", "Запись добавлена!")
        self.save_to_json()

        # Очистка полей ввода
        self.date_entry.delete(0, tk.END)
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precip_entry.delete(0, tk.END)

    def save_to_json(self):
        with open('weather_diary.json', 'w') as f:
            json.dump(self.entries, f, ensure_ascii=False, indent=4)

    def load_from_json(self):
        try:
            with open('weather_diary.json', 'r') as f:
                self.entries = json.load(f)
        except FileNotFoundError:
            self.entries = []

    def filter_by_date(self, date):
        return [entry for entry in self.entries if entry['date'] == date]

    def filter_by_temperature(self, min_temp):
        return [entry for entry in self.entries if entry['temperature'] > min_temp]

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()
