import tkinter as as_tk
from dis import name
from tkinter import ttk, messagebox


class FridgeApp:
    pass


class FridgeApp:
    def init(self, root):
        self.root = root
        self.root.title("БД: Холодильники (Варіант 23)")
        self.root.geometry("900x600")

        # База даних (список словників)
        self.db = [
            {"manufacturer": "Samsung", "volume": 350, "energy": 280, "price": 25000},
            {"manufacturer": "LG", "volume": 320, "energy": 260, "price": 23000},
            {"manufacturer": "Bosch", "volume": 400, "energy": 300, "price": 35000},
            {"manufacturer": "Indesit", "volume": 280, "energy": 240, "price": 12000}
        ]

        # Змінні для полів вводу
        self.var_manufacturer = as_tk.StringVar()
        self.var_volume = as_tk.StringVar()
        self.var_energy = as_tk.StringVar()
        self.var_price = as_tk.StringVar()

        # Змінні для операцій (сортування/пошук)
        self.var_search_attr = as_tk.StringVar(value="manufacturer")
        self.var_search_value = as_tk.StringVar()

        self._setup_ui()
        self.update_table(self.db)

    def _setup_ui(self):
        # --- Фрейм додавання записів ---
        input_frame = ttk.LabelFrame(self.root, text="Додати новий холодильник")
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text="Виробник:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.var_manufacturer).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Об'єм (л):").grid(row=0, column=2, padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.var_volume).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="Енерго (кВт/рік):").grid(row=0, column=4, padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.var_energy).grid(row=0, column=5, padx=5, pady=5)

        ttk.Label(input_frame, text="Ціна (грн):").grid(row=0, column=6, padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.var_price).grid(row=0, column=7, padx=5, pady=5)

        ttk.Button(input_frame, text="Додати", command=self.add_record).grid(row=0, column=8, padx=10, pady=5)

        # --- Фрейм операцій (Сортування, Пошук, Видалення за атрибутом) ---
        ops_frame = ttk.LabelFrame(self.root, text="Операції з БД")
        ops_frame.pack(fill="x", padx=10, pady=5)

        # Вибір атрибута для операцій
        attributes = {"Виробник": "manufacturer", "Об'єм": "volume",
                      "Енерго": "energy", "Ціна": "price"}

        ttk.Label(ops_frame, text="Атрибут:").pack(side="left", padx=5)
        self.combo_attr = ttk.Combobox(ops_frame, values=list(attributes.keys()), state="readonly")
        self.combo_attr.current(0)
        self.combo_attr.pack(side="left", padx=5)

        ttk.Label(ops_frame, text="Значення:").pack(side="left", padx=5)
        ttk.Entry(ops_frame, textvariable=self.var_search_value).pack(side="left", padx=5)

        # Кнопки операцій
        ttk.Button(ops_frame, text="Сортувати (c)", command=lambda: self.sort_db(attributes)).pack(side="left", padx=5)
        ttk.Button(ops_frame, text="Пошук (f)", command=lambda: self.search_db(attributes)).pack(side="left", padx=5)
        ttk.Button(ops_frame, text="Видалити за атрибутом (d)", command=lambda: self.delete_by_attr(attributes)).pack(
            side="left", padx=5)
        ttk.Button(ops_frame, text="Скинути фільтр (a)", command=lambda: self.update_table(self.db)).pack(side="left",
                                                                                                          padx=20)

        # --- Таблиця (Treeview) ---
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("manufacturer", "volume", "energy", "price")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        # Заголовки стовпців
        self.tree.heading("manufacturer", text="Виробник")
        self.tree.heading("volume", text="Об'єм (л)")
        self.tree.heading("energy", text="Енергоспоживання (кВт·год/рік)")
        self.tree.heading("price", text="Ціна (грн)")

        # Налаштування ширини стовпців
        for col in columns:
            self.tree.column(col, anchor="center")

        # Скролбар
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- Кнопка видалення виділеного ---
        btn_del_idx = ttk.Button(self.root, text="Видалити виділений елемент (e)", command=self.delete_selected)
        btn_del_idx.pack(pady=10)

        # --- Логіка ---

    def add_record(self):
        """(b) Додавання елементів до БД"""
        m = self.var_manufacturer.get()
        v = self.var_volume.get()
        e = self.var_energy.get()
        p = self.var_price.get()

        if not (m and v and e and p):
            messagebox.showwarning("Помилка", "Всі поля мають бути заповнені!")
            return

        try:
            record = {
                "manufacturer": m,
                "volume": float(v),
                "energy": float(e),
                "price": float(p)
            }
            self.db.append(record)
            self.update_table(self.db)

            # Очищення полів
            self.var_manufacturer.set("")
            self.var_volume.set("")
            self.var_energy.set("")
            self.var_price.set("")
        except ValueError:
            messagebox.showerror("Помилка", "Об'єм, Енерго та Ціна повинні бути числами!")

    def update_table(self, data):
        """(a) Вивести БД (або відфільтровані дані)"""
        # Очищення таблиці
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заповнення даними
        for row in data:
            self.tree.insert("", "end", values=(row["manufacturer"], row["volume"], row["energy"], row["price"]))

    def delete_selected(self):
        """(e) Видаляти елемент з БД за заданим індексом (виділенням)"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Увага", "Виберіть рядок для видалення!")
            return

        # Отримуємо значення з виділеного рядка, щоб знайти його в базі
        # Примітка: у реальних БД використовують ID, тут видаляємо за збігом значень
        item_values = self.tree.item(selected_item)["values"]

        # Знаходимо індекс в оригінальному списку
        for i, row in enumerate(self.db):
            # Порівнюємо значення (враховуємо типи даних, treeview повертає все як строки іноді)
            if (str(row["manufacturer"]) == str(item_values[0]) and
                    str(row["volume"]) == str(item_values[1]) and
                    str(row["energy"]) == str(item_values[2]) and
                    str(row["price"]) == str(item_values[3])):
                del self.db[i]
                break

        self.update_table(self.db)

    def get_attr_key(self, attr_map):
        """Допоміжна функція для отримання ключа атрибуту"""
        selected_name = self.combo_attr.get()
        return attr_map[selected_name]

    def sort_db(self, attr_map):
        """(c) Відсортувати БД за заданим атрибутом"""
        key = self.get_attr_key(attr_map)
        # Сортуємо оригінальну базу
        self.db.sort(key=lambda x: x[key])
        self.update_table(self.db)

    def search_db(self, attr_map):
        """(f) Виводити всі елементи в БД за заданим атрибутом"""
        key = self.get_attr_key(attr_map)
        val = self.var_search_value.get()

        if not val:
            messagebox.showinfo("Інфо", "Введіть значення для пошуку")
            return
        filtered_data = []
        for row in self.db:
            # Конвертуємо все в стрінг для порівняння
            if str(row[key]).lower() == str(val).lower():
                filtered_data.append(row)

        if not filtered_data:
            messagebox.showinfo("Результат", "Нічого не знайдено")

        self.update_table(filtered_data)

    def delete_by_attr(self, attr_map):
        """(d) Видаляти елементи з БД за заданим атрибутом"""
        key = self.get_attr_key(attr_map)
        val = self.var_search_value.get()

        if not val:
            messagebox.showwarning("Увага", "Введіть значення для видалення")
            return

        confirm = messagebox.askyesno("Підтвердження", f"Видалити всі записи, де {key} = {val}?")
        if confirm:
            # Створюємо новий список тільки з тих елементів, що НЕ співпадають
            new_db = [row for row in self.db if str(row[key]).lower() != str(val).lower()]
            deleted_count = len(self.db) - len(new_db)
            self.db = new_db
            self.update_table(self.db)
            messagebox.showinfo("Успіх", f"Видалено записів: {deleted_count}")

    if name == "main":
        root = as_tk.Tk()
        app = FridgeApp(root)
        root.mainloop()