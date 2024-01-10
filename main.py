import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from tkinter import filedialog
from PIL import Image, ImageTk
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from bs4 import BeautifulSoup
import requests
import numpy as np


class ImageClassifierApp:
    def clean_html(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        cleaned_text = soup.get_text(separator='\n', strip=True)
        return cleaned_text

    def __init__(self, master):
        self.master = master
        self.master.title("Image Classifier")
        self.master.geometry("1280x800+0+0")
        self.master.config(bg='burlywood2')

        #tswira li fu9
        self.header_image = Image.open("nav.png")
        self.header_image = ImageTk.PhotoImage(self.header_image)
        self.header_label = tk.Label(self.master, image=self.header_image, bg='burlywood2')
        self.header_label.image = self.header_image
        self.header_label.grid(row=0, column=0, columnspan=4)

        # blasset ktaba
        self.text_entry = tk.Entry(self.master, width=200)
        self.text_entry.grid(row=1, column=0, padx=10, pady=10, columnspan=3)

        # botona d search
        search_text_button = tk.Button(self.master, text="Search", command=self.search_text, width=5)
        search_text_button.grid(row=1, column=3, padx=5)

        # botona d search b tswira
        classify_button = tk.Button(self.master, text="Search Image", command=self.classify_image, width=20)
        classify_button.grid(row=2, column=0, padx=5)

        # botona bach ktdkhel tswira
        browse_button = tk.Button(self.master, text="Browse Image", command=self.load_image, width=20)
        browse_button.grid(row=2, column=1, padx=5)

        # hada li kiyakhud tswira o ydir prediction
        self.model = MobileNetV2(weights='imagenet')

        # knbyno tswira
        self.image_label = tk.Label(self.master)
        self.image_label.grid(row=3, column=0, columnspan=4, pady=10)

        # knbyno recherche b wikipedia
        self.result_label = tk.Label(self.master, text="")
        self.result_label.grid(row=4, column=0, columnspan=4, pady=5)

        # scroled text fin kiban resultat
        self.result_text_widget = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, width=80, height=20)
        self.result_text_widget.grid(row=5, column=0, columnspan=4, padx=10)
        back_to_login_button = tk.Button(self.master, text="Log out", command=self.back_to_login,
                                         font=("times new roman", 14, "bold"), bd=0, cursor="hand2", bg="burlywood3",
                                         fg="black")
        back_to_login_button.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10, width=250, height=40)

        # knkhbiw scroled text f lwl
        self.result_text_widget.grid_remove()

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.display_image(file_path)

    def display_image(self, file_path):
        image_data = Image.open(file_path)
        image_data = image_data.resize((300, 300), Image.LANCZOS)
        image_data = ImageTk.PhotoImage(image_data)
        self.image_label.config(image=image_data)
        self.image_label.image = image_data

        self.image_path = file_path
        self.result_label.config(text="")
        # Make the ScrolledText visible when an image is loaded
        self.result_text_widget.grid()

    def search_google(self, query):
        search_url = f"https://en.wikipedia.org/wiki/{query}"
        response = requests.get(search_url)
        return response.text

    def back_to_login(self):
        from login_page import login_page
        self.master.destroy()
        root = tk.Tk()
        obj = login_page(root)
        root.mainloop()

    def classify_image(self):
        if hasattr(self, 'image_path'):
            img = image.load_img(self.image_path, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)

            predictions = self.model.predict(img_array)
            decoded_predictions = decode_predictions(predictions, top=1)[0]

            predicted_text = decoded_predictions[0][1]
            confidence = decoded_predictions[0][2]

            result_text = f"Prediction: {predicted_text} ({confidence:.2f})"
            self.result_label.config(text=result_text)


            search_results_html = self.search_google(predicted_text)

            # kn7wlo html l text
            search_results_text = self.clean_html(search_results_html)

            # knbyno resultat
            self.result_text_widget.delete(1.0, tk.END)
            self.result_text_widget.insert(tk.END, search_results_text)
            # knbyno scroled image mli knwrko 3la recherche
            self.result_text_widget.grid()
            self.header_label.grid_remove()
        else:
            self.result_label.config(text="Please load an image first.")

            self.result_text_widget.grid_remove()

    def search_text(self):

        text_query = self.text_entry.get().strip()

        if text_query:

            search_results_html = self.search_google(text_query)

            # Convert HTML to plain text
            search_results_text = self.clean_html(search_results_html)

            # Display the search results in the Tkinter interface
            self.result_text_widget.delete(1.0, tk.END)
            self.result_text_widget.insert(tk.END, search_results_text)
            # Make the ScrolledText visible when text is searched
            self.result_text_widget.grid()
            self.header_label.grid_remove()
        else:
            self.result_label.config(text="Please enter text for search.")
            self.result_text_widget.grid_remove()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Image Classifier")
    app = ImageClassifierApp(root)
    root.mainloop()
