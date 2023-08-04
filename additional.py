# Name: Hu Bowen
# Date: 3 Aug 2023
#
# additional.py
# Implements additional requirements for PRG1 '23 Final Assignment
# Interactive map with real time data

import tkinter as tk
import tkintermapview as tk_map
from PIL import Image, ImageTk, ImageDraw, ImageFont

from utils.files import load_file
from utils.carpark import parse_carpark_information, get_carpark_information, associate_carpark_info, get_realtime_info

data_sources = [
    "carpark-availability-v1.csv",
    "carpark-availability-v2.csv",
    "Real Time from LTA"
]

chosen_data_source = data_sources[0]


def prompt_choice(frame: tk.Frame):
    """Prompts the user to choose between the 2 CSV files
    or real-time data from LTA, and displays the map accordingly"""

    # Clear the window to make way for new elements
    clear_frame(frame)

    # Initialise title
    title_label = tk.Label(frame, text="PRG1 Assignment", font=("Arial", 25))
    title_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    # Initialise user prompt
    user_prompt = tk.Label(
        frame, text="Where would you like to source your data from?")
    user_prompt.place(in_=title_label, relx=0.5, y=50, anchor=tk.CENTER)

    # Initialise dropdown
    default_option = tk.StringVar(frame)
    default_option.set(data_sources[0])

    dropdown = tk.OptionMenu(frame, default_option,
                             *data_sources, command=set_data_source)
    dropdown.place(in_=user_prompt, relx=0.5, y=40, anchor=tk.CENTER)

    # Initialise submit button
    map_btn = tk.Button(frame, text="Show Map",
                        command=lambda: show_map(frame))
    map_btn.place(in_=dropdown, relx=0.5, y=50, anchor=tk.CENTER)


def show_map(frame: tk.Frame):
    """Makes Tkinter show map with data based on the user selected source"""
    clear_frame(frame)

    # Load carpark data
    if chosen_data_source == data_sources[2]:
        cp_availability = get_realtime_info()
    else:
        cp_availability = load_file(chosen_data_source)[1:]  # Remove header
        cp_availability = parse_carpark_information(cp_availability)

    # Link carpark data
    cp_info = get_carpark_information()
    linked_info = associate_carpark_info(
        cp_availability, cp_info, get_location=True)

    # Initialise map
    map_widget = tk_map.TkinterMapView(frame, width=800, height=600)
    map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Center the map to Singapore
    map_widget.set_position(1.290270, 103.851959)
    map_widget.set_zoom(11)

    # Map carpark data to map
    for data in linked_info:
        # Account for location with none values
        if data["Location"] is None:
            continue

        # Get location coordinates and map to Tkinter map
        degrees, minutes = data["Location"].split(' ')
        degrees, minutes = float(degrees), float(minutes)

        # Get availability percentage and set marker color
        percentage = data["Percentage"]
        if percentage < 25:
            inner_color = "#00FF00"
            outer_color = "#006400"
        elif percentage < 50:
            inner_color = "#FFFF00"
            outer_color = "#FFA500"
        else:
            inner_color = "#FF0000"
            outer_color = "#8B0000"

        # Generate data to show on image
        display_text = ""
        display_text += data["Carpark Number"] + '\n'
        display_text += "Available Lots: " + data["Lots Available"] + '\n'
        display_text += "Total Lots: " + data["Total Lots"] + '\n'
        display_text += "Percentage: " + \
            str(round(data["Percentage"], 2)) + "%"

        # Display marker
        map_widget.set_marker(
            degrees, minutes,
            text=data["Carpark Number"],
            marker_color_circle=inner_color,
            marker_color_outside=outer_color,
            data=display_text,
            command=marker_click
        )


def main():
    # Create tkinter window
    root = tk.Tk()
    root.geometry("800x600")
    root.title("Hu Bowen - PRG1 Assignment")

    # Create frame
    frame = tk.Frame(root)
    frame.pack(side="top", expand=True, fill="both")

    # Mainloop
    prompt_choice(frame)
    tk.mainloop()


def set_data_source(selection: str):
    """Callback function for Tkinter OptionMenu,
    sets the chosen data source based on what the user chose"""
    global chosen_data_source
    chosen_data_source = selection


def clear_frame(frame: tk.Frame):
    """Clears the Tkinter window

    Args:
        window (tkinter.Tk): The window to clear
    """

    for widget in frame.winfo_children():
        widget.destroy()


def marker_click(marker):
    """Function to generate an image to display carpark data,
    and toggles visibility if the image has been generated"""

    if marker.image is None:
        # Retrieve text to display
        display_text = marker.data

        # Generate image
        # Credits: https://stackoverflow.com/questions/63280719/tkinter-how-to-change-text-into-an-image
        image = Image.new("RGB", (200, 75), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", size=12)
        draw.text((0, 0), font=font, text=display_text, fill="black")
        final_image = ImageTk.PhotoImage(image)

        # Set image
        marker.image = final_image

    # Toggle image visibility
    if marker.image_hidden:
        marker.hide_image(False)
    else:
        marker.hide_image(True)
