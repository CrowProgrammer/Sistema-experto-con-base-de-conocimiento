from tkinter import *
from PIL import ImageTk, Image
import copy

# Clase para representar un automóvil
class Car:
    def __init__(self, name="", description="", image="sources/default_car.jpg", characteristics=None):
        self.name = name
        self.description = description
        self.image = image
        self.characteristics = characteristics if characteristics else {}

# Clase para visualizar un automóvil
class CarVisualizer(Frame):
    def __init__(self, root, car, explanation=""):
        super().__init__(root)
        self.car = car
        self.explanation = explanation
        self.pack(fill="both", expand=True)

        # Título
        title_label = Label(self, text=self.car.name, font=("Arial", 25))
        title_label.pack()

        # Descripción
        desc_label = Label(self, text=self.car.description, font=("Arial", 14), wraplength=800)
        desc_label.pack()

        # Explicación
        explanation_label = Label(self, text=self.explanation, font=("Arial", 14), wraplength=800)
        explanation_label.pack()

        # Imagen
        img = Image.open(self.car.image)
        img = img.resize((400, 300), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(img)
        image_label = Label(self, image=self.photo)
        image_label.pack()

# Clase para clasificar automóviles
class CarClassifier:
    def __init__(self, root, main_menu):
        self.root = root
        self.main_menu = main_menu
        self.frame = Frame(self.root)
        self.cars = []
        self.default_car = Car("Desconocido", "Características no identificadas", "sources/default_car.jpg")
        self.load_cars()
        self.rules = {}
        self.possible_cars = []
        self.reset_button = Button(self.root, text="Reiniciar", command=self.main_menu.show)

    # Cargar automóviles en la base de datos
    def load_cars(self):
        car1 = Car("Toyota Corolla",
                   "Un sedán confiable y eficiente en combustible.",
                   "sources/Toyota_Corolla.jpg",
                   {"tipo": "sedán", "color": "blanco"})
        car2 = Car("Ford Mustang",
                   "Un clásico coche deportivo.",
                   "sources/ford_mustang.jpg",
                   {"tipo": "deportivo", "color": "rojo"})
        
        car3 = Car("Honda Civic",
           "Un sedán compacto y económico.",
           "sources/honda_civic.jpg",
           {"tipo": "sedán", "color": "azul"})
           
        car4 = Car("BMW M5",
                "Un sedán de lujo con un rendimiento excepcional.",
                "sources/bmw_m5.jpg",
                {"tipo": "sedán", "color": "negro"})

        # Agregando todos los autos a la lista
        self.cars.extend([car1, car2, car3, car4])

    def clear_frame(self):
        # Eliminar todos los widgets del frame
        for widget in self.frame.winfo_children():
            widget.pack_forget()

    # Mostrar menú de selección de características
    def ask_question(self, question, options):
        question_label = Label(self.frame, text=question, font=("Arial", 14))
        question_label.pack()
        selected_option = StringVar()
        selected_option.set("Otro")
        option_menu = OptionMenu(self.frame, selected_option, *options)
        option_menu.pack()
        next_button = Button(self.frame, text="Siguiente", command=lambda: selected_option.set("ready"))
        next_button.pack()
        next_button.wait_variable(selected_option)
        question_label.pack_forget()
        option_menu.pack_forget()
        next_button.pack_forget()
        return selected_option.get()

    # Clasificar automóvil
    def classify(self):
        self.clear_frame()
        self.frame.pack(fill="both", expand=True)
        self.possible_cars = copy.deepcopy(self.cars)
        self.rules.clear()
        characteristic = ""
        answer = ""
        try:
            while len(self.possible_cars) > 1:
                possible_rules = {}
                for car in self.possible_cars:
                    for key, value in car.characteristics.items():
                        if key not in self.rules:
                            if key not in possible_rules:
                                possible_rules[key] = {}
                            possible_rules[key][value] = possible_rules[key].get(value, 0) + 1

                if not possible_rules:
                    break

                characteristic = next(iter(possible_rules))
                options = list(possible_rules[characteristic].keys()) + ["Otro"]
                answer = self.ask_question(f"Selecciona el {characteristic}:", options)
                self.rules[characteristic] = answer

                self.possible_cars = [car for car in self.possible_cars if car.characteristics.get(characteristic, "Otro") == answer]

            final_car = self.possible_cars[0] if self.possible_cars else self.default_car
        except IndexError:
            final_car = self.default_car

        explanation = "\n".join([f"{key}: {value}" for key, value in self.rules.items()])
        self.frame.pack_forget()
        CarVisualizer(self.root, final_car, explanation).pack()
        self.reset_button.pack()

    def show(self):
        self.clear_frame()
        self.frame.pack(fill="both", expand=True)
        Button(self.frame, text="Clasificar Automóvil", command=self.classify).pack()

# Clase para el menú principal
class MainMenu:
    def __init__(self, root):
        self.root = root
        self.frame = Frame(self.root)
        self.car_classifier = CarClassifier(root, self)

    def show(self):
        # Reiniciar la ventana antes de mostrar el menú principal
        for widget in self.root.winfo_children():
            widget.pack_forget()

        self.frame.pack(fill="both", expand=True)
        Button(self.frame, text="Iniciar Clasificador", command=self.show_classifier).pack()

    def hide(self):
        self.frame.pack_forget()

    def show_classifier(self):
        self.hide()
        self.car_classifier.show()

# Función principal para ejecutar el programa
if __name__ == "__main__":
    root = Tk()
    root.title("Clasificador de Automóviles")
    root.geometry("1000x600")
    main_menu = MainMenu(root)
    main_menu.show()
    root.mainloop()
