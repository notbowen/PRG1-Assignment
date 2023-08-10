# Name: Hu Bowen
# Date: 3 Aug 2023
#
# additional.py
# Implements additional requirements for PRG1 '23 Final Assignment
# Interactive map with real time data

import sys

import tkinter as tk
import tkintermapview as tk_map
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
from typing import Dict, List

from utils.files import load_file
from utils.carpark import get_carpark_information, get_realtime_info
from utils.carpark import parse_carpark_information, associate_carpark_info
from utils.input import validate_num

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

    # Handle failed request
    if cp_availability is None:
        messagebox.showerror("ERROR!", "Failed to get realtime data!")
        sys.exit(1)

    # Link carpark data
    cp_info = get_carpark_information()
    linked_info = associate_carpark_info(
        cp_availability, cp_info, get_location=True)

    # Initialise filter by percentage
    cp_percentage_label = tk.Label(frame, text="Filter by percentage: ")
    cp_percentage_label.place(x=0, y=0)

    # Register input validation callback
    vcmd = frame.register(lambda s: s == "" or validate_num(s, range(0, 101)))
    cp_percentage = tk.Entry(frame, validate='key',
                             validatecommand=(vcmd, "%P"))
    cp_percentage.place(in_=cp_percentage_label, x=120)

    # Initialise filter by carpark
    cp_location_label = tk.Label(frame, text="Filter by location: ")
    cp_location_label.place(x=250, y=0)

    cp_location = tk.Entry(frame, width=40)
    cp_location.place(in_=cp_location_label, x=100)

    # Filter button
    filter_btn = tk.Button(frame, text="Filter")
    filter_btn.place(x=640, y=0, anchor="ne")

    # Export button
    export_btn = tk.Button(frame, text="Export")
    export_btn.place(x=690, y=0, anchor="ne")

    # Show most lots button
    most_lots_btn = tk.Button(frame, text="Most Lots")
    most_lots_btn.place(x=760, y=0, anchor="ne")

    # Initialise map
    map_widget = tk_map.TkinterMapView(frame, width=800, height=570)
    map_widget.place(y=30)

    # Center the map to Singapore
    map_widget.set_position(1.290270, 103.851959)
    map_widget.set_zoom(11)

    # Load data to map
    draw_markers(map_widget, linked_info)


def draw_markers(map_widget: tk_map.TkinterMapView, data: List[Dict[str, str]]):
    """Function to draw a marker on a Tkinter MapView, using the given carpark data
    formatted in a dict.

    Args:
        map_widget (tk_map.TkinterMapView): The map to draw the marker on
        data (ListDict[str, str]]): The list of carpark data
    """

    # Clear map markers
    map_widget.delete_all_marker()

    # Loop through list and draw
    for carpark in data:
        # Parse location data and skip if none
        location = carpark.get("Location")
        if location is None:
            continue

        # Format data into lat & long
        latitude, longitude = location.split(" ")
        latitude, longitude = float(latitude), float(longitude)

        # Get availability percentage and set marker color
        percentage = carpark["Percentage"]
        if percentage > 75:
            # Green
            inner_color = "#00FF00"
            outer_color = "#006400"
        elif percentage > 25:
            # Yellow
            inner_color = "#FFFF00"
            outer_color = "#FFA500"
        else:
            # Red
            inner_color = "#FF0000"
            outer_color = "#8B0000"

        # Generate data to show on image
        display_text = ""
        display_text += carpark["Carpark Number"] + '\n'
        display_text += "Available Lots: " + carpark["Lots Available"] + '\n'
        display_text += "Total Lots: " + carpark["Total Lots"] + '\n'
        display_text += "Percentage: " + \
            str(round(carpark["Percentage"], 2)) + "%\n"
        display_text += "Address: " + carpark["Address"]

        # Display marker
        map_widget.set_marker(
            latitude, longitude,
            text=carpark["Carpark Number"],
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
    root.resizable(False, False)

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


def on_filter(frame: tk.Frame, cp_percentage: tk.Entry, cp_location: tk.Entry):
    """Function that is called when filter button is clicked

    Args:
        frame (tk.Frame): The main tkinter frame
        cp_percentage (tk.Entry): The entry containing the percentage
        cp_location (tk.Entry): The entry containing the location
    """
    global percentage, location

    percentage = cp_percentage.get()
    if percentage == "":
        percentage = "0"

    location = cp_location.get()
    location = location.upper()

    show_map(frame)


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
        image = Image.new("RGB", (300, 75), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", size=12)
        draw.text((0, 0), font=font, text=display_text, fill="black")
        final_image = ImageTk.PhotoImage(image)

        # Set image
        marker.image = final_image
        marker.image_hidden = True

    # Toggle image visibility
    if marker.image_hidden:
        marker.hide_image(False)
    else:
        marker.hide_image(True)
