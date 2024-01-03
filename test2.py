import tkinter as tk
from tkinter import messagebox
from test import calculate_chain_cuts
from itertools import combinations

class ChainCutsInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Chain Cuts Interface")
        self.root.configure(bg="#EFEFEF")  # Задаем цвет фона

        self.label_input = tk.Label(root, text="Введите количество звеньев цепочки:", bg="#EFEFEF")
        self.label_input.pack()

        self.entry = tk.Entry(root)
        self.entry.pack()

        self.button = tk.Button(root, text="Выполнить", command=self.calculate_cuts, bg="#4CAF50", fg="white")
        self.button.pack()

        self.result_label = tk.Label(root, text="Результаты:", bg="#EFEFEF")
        self.result_label.pack()

        self.result_text = tk.Text(root, height=25, width=200)
        self.result_text.pack()

        self.canvas = tk.Canvas(root,height=300, width=1800, bg="#FFA500")
        self.canvas.pack()

    def draw_not_lazy_student(self):
        # Очищаем холст
        self.canvas.delete("all")

        # Получаем размеры холста
        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()

        self.canvas.create_text(canvas_width // 2, canvas_height // 2, text="Хорошего отдыха",
                                font=("Arial", 50, "bold"), fill="black")

        # Добавляем черную границу вокруг всего холста
        border_width = 5
        self.canvas.create_rectangle(border_width, border_width, canvas_width - border_width,
                                     canvas_height - border_width, width=border_width, outline="black")

    def calculate_cuts(self):
        try:
            koll_zvenyev_input = int(self.entry.get())
            num_cuts, resulting_chain, cut_positions = calculate_chain_cuts(koll_zvenyev_input)

            result_str = f"Минимальное количество разрезов: {num_cuts}\n" \
                         f"Звенья, которые получатся: {resulting_chain}\n" \
                         f"Места разрезов: {cut_positions}\n"

            self.result_text.delete(1.0, tk.END)  # Очищаем предыдущий результат
            self.result_text.insert(tk.END, result_str)

            self.draw_not_lazy_student()

            koll_dney = koll_zvenyev_input
            metodi_oplati = resulting_chain
            den_oplati = 1

            previous_subset = None
            used_numbers = set()

            while den_oplati <= koll_dney:
                for subset_size in range(1, len(metodi_oplati) + 1):
                    for subset in combinations(metodi_oplati, subset_size):
                        if sum(subset) == den_oplati and den_oplati not in used_numbers:
                            used_numbers.add(den_oplati)

                            if previous_subset is not None:
                                diff_subsets = list(set(previous_subset) - set(subset))
                                if diff_subsets:
                                    self.result_text.insert(tk.END, f"Забираем : {', '.join(map(str, diff_subsets))}\n")

                            self.result_text.insert(tk.END, f"День {den_oplati} отдаем {subset}\n")
                            previous_subset = subset
                            break

                den_oplati += 1

        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректное число звеньев.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ChainCutsInterface(root)
    root.mainloop()
