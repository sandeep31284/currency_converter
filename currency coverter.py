import customtkinter as ctk
import subprocess
import requests  # For getting exchange rates
from PIL import Image, ImageTk

# List of different types of currencies
currencies = ["USD", "EUR", "INR", "GBP", "AUD", "CAD", "JPY", "CNY"]  # Reduced for simplicity

# Dummy API key for demonstration, use a valid API key from a service like ExchangeRate-API or Fixer.io
API_KEY = 'dec218e00cf0ba0a1b5f8997'
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"


# Function to get conversion rate
def get_conversion_rate(from_currency, to_currency):
    url = f"{BASE_URL}{from_currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for bad status codes
        data = response.json()

        # Check if the response contains conversion rates
        if 'conversion_rates' in data:
            conversion_rate = data['conversion_rates'].get(to_currency, None)
            if conversion_rate:
                return conversion_rate
            else:
                return None
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def run():
    root.destroy()
    subprocess.run(['python', 'menu1.py'])


# Function to handle conversion
def convert_currency():
    from_currency = combobox1.get().split(" ")[0]
    to_currency = combobox2.get().split(" ")[0]
    try:
        amount = float(entry.get())
    except ValueError:
        result_entry.delete(0, ctk.END)
        result_entry.insert(0, "Invalid amount")
        return

    rate = get_conversion_rate(from_currency, to_currency)
    if rate:
        converted_amount = amount * rate
        result_entry.delete(0, ctk.END)
        result_entry.insert(0, str(round(converted_amount, 2)))
    else:
        result_entry.delete(0, ctk.END)
        result_entry.insert(0, "Error in conversion")


# Function to reset all fields
def reset_fields():
    combobox1.set("Select currency")
    combobox2.set("Select currency")
    entry.delete(0, ctk.END)
    result_entry.delete(0, ctk.END)


# Root function
ctk.set_appearance_mode("light")  # Modes: "light", "dark", "system" (for system default)
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "dark-blue", "green"

root = ctk.CTk()
root.title("Currency Converter")
root.geometry('1000x800')

# Resize the logo image using PIL and display it on the left
logo_image = Image.open("currencybg.png")  # Path to the logo image
logo_image = logo_image.resize((1000, 800), Image.Resampling.LANCZOS)  # Resize the image to 1000x600 pixels
logo_photo = ImageTk.PhotoImage(logo_image)
# Display the resized logo
logo_label = ctk.CTkLabel(root, image=logo_photo)
logo_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)


# Frame
frame = ctk.CTkFrame(root, fg_color="burlywood2", width=900, height=575)
frame.pack(padx=10, pady=150)

# Label
label = ctk.CTkLabel(frame, text="Currency Converter", font=ctk.CTkFont(size=30, weight="bold"), text_color="gray2",corner_radius=30)
label.grid(column=1, row=0, padx=0, pady=20)

# Combobox1
combobox1 = ctk.CTkComboBox(frame, values=currencies,corner_radius=5)
combobox1.set("Select currency")
combobox1.grid(column=0, row=1, padx=20, pady=20)

# Combobox2
combobox2 = ctk.CTkComboBox(frame, values=currencies,corner_radius=5)
combobox2.set("Select currency")
combobox2.grid(column=2, row=1, padx=20, pady=20)

# Entry for amount
entry = ctk.CTkEntry(frame, width=200, placeholder_text="Enter amount")
entry.grid(column=0, row=2, padx=20, pady=20)

# Convert button
convertbutton = ctk.CTkButton(frame, text="CONVERT", command=convert_currency, fg_color='#FF4040', text_color="gray2",
                              font=ctk.CTkFont(size=15, weight="bold"),width=20,height=100,hover_color='#98F5FF',corner_radius=500)
convertbutton.grid(column=1, row=1, padx=0, pady=0, rowspan=2)

# Entry to display result
result_entry = ctk.CTkEntry(frame, width=200, placeholder_text="Result")
result_entry.grid(column=2, row=2, padx=20, pady=20)

# Reset button
resetbutton = ctk.CTkButton(frame, text="Reset", command=reset_fields, fg_color='brown', text_color="gray2",
                            font=ctk.CTkFont(size=15, weight="bold"),corner_radius=30)
resetbutton.grid(column=0, row=3, padx=20, pady=20)

# Exit button
exitbutton = ctk.CTkButton(frame, text="Exit", command=run, fg_color='brown', text_color="gray2",
                           font=ctk.CTkFont(size=15, weight="bold"),corner_radius=30)
exitbutton.grid(column=2, row=3, padx=20, pady=20)

root.mainloop()