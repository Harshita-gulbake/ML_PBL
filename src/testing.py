import customtkinter
import pymysql
from PIL import Image
from tkinter import filedialog
from ultralytics import YOLO
import os
import time
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import textwrap
import matplotlib.pyplot as plt
from openai import OpenAI
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from connection import get_connection

# Load YOLO model once
model = YOLO('models/modelV3.pt')


class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, folder_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x230+600+200")
        self.title("IAgroscan | Batch Detection")
        self.wm_iconbitmap("data/imgs/Scanner.ico")

        self.label_detection = customtkinter.CTkLabel(
            self, text="Batch Detection Successful!",
            font=customtkinter.CTkFont(family="Google Sans Medium", size=17)
        )
        self.label_detection.pack(padx=20, pady=20)

        self.label_detection2 = customtkinter.CTkLabel(
            self, text="Detections Saved In:",
            font=customtkinter.CTkFont(family="Google Sans Medium", size=15)
        )
        self.label_detection2.pack(padx=20, pady=20)

        self.label_path = customtkinter.CTkLabel(
            self, text=folder_path,
            font=customtkinter.CTkFont(family="JetBrains Mono", size=12)
        )
        self.label_path.pack(padx=20, pady=20)

        self.attributes('-topmost', True)
        self.lift()


class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("800x700+550+175")
        customtkinter.set_appearance_mode("light")
        self.title("IAgroscan | Main Menu")
        self.wm_iconbitmap("data/imgs/Scanner.ico")

        customtkinter.set_default_color_theme("blue")

        self.grid_columnconfigure((1), weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure((0, 1), weight=1)

        # Sidebar
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, fg_color="sea green", corner_radius=25)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, padx=10, pady=10, sticky="nswe")
        self.sidebar_frame.grid_rowconfigure(10, weight=1)

        # Center frame
        self.center_frame = customtkinter.CTkFrame(self, width=350, corner_radius=25)
        self.center_frame.grid(row=0, column=1, padx=(0, 10), pady=10, rowspan=4, sticky="nswe")
        self.center_frame.grid_rowconfigure(2, weight=1)
        self.center_frame.grid_columnconfigure(2, weight=1)

        # Logo
        logo = customtkinter.CTkImage(
            light_image=Image.open("data/imgs/Scanner2.png"),
            dark_image=Image.open("data/imgs/Scanner2.png"),
            size=(200, 200),
        )

        self.labelImg = customtkinter.CTkLabel(self.sidebar_frame, image=logo, text="")
        self.labelImg.grid(row=1, column=0, padx=20, pady=(20, 10))

        # Sidebar icons
        img_scan_white = Image.open("data/icons/scannerw.png")
        img_scan_green = Image.open("data/icons/scannerg.png")

        img_records_white = Image.open("data/icons/cellsw.png")
        img_records_green = Image.open("data/icons/cellsg.png")

        img_chart_white = Image.open("data/icons/bar_chartw.png")
        img_chart_green = Image.open("data/icons/bar_chartg.png")

        # ---- Simple Detection ----
        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame, command=self.select_image,
            text="Single Detection", fg_color="transparent",
            height=60, text_color="white", corner_radius=15,
            anchor="w", font=("Google Sans Medium", 18),
            image=customtkinter.CTkImage(dark_image=img_scan_white, light_image=img_scan_white)
        )

        def on_hover_1(event):
            self.sidebar_button_1.configure(
                text_color="sea green", fg_color="white",
                image=customtkinter.CTkImage(dark_image=img_scan_green, light_image=img_scan_green)
            )

        def off_hover_1(event):
            self.sidebar_button_1.configure(
                text_color="white", fg_color="transparent",
                image=customtkinter.CTkImage(dark_image=img_scan_white, light_image=img_scan_white)
            )

        self.sidebar_button_1.bind("<Enter>", on_hover_1)
        self.sidebar_button_1.bind("<Leave>", off_hover_1)
        self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        # ---- Batch Detection ----
        self.sidebar_button_2 = customtkinter.CTkButton(
            self.sidebar_frame, command=self.select_batch,
            text="Batch Detection", fg_color="transparent",
            height=60, text_color="white", corner_radius=15,
            anchor="w", font=("Google Sans Medium", 18),
            image=customtkinter.CTkImage(dark_image=img_scan_white, light_image=img_scan_white)
        )

        def on_hover_2(event):
            self.sidebar_button_2.configure(
                text_color="sea green", fg_color="white",
                image=customtkinter.CTkImage(dark_image=img_scan_green, light_image=img_scan_green)
            )

        def off_hover_2(event):
            self.sidebar_button_2.configure(
                text_color="white", fg_color="transparent",
                image=customtkinter.CTkImage(dark_image=img_scan_white, light_image=img_scan_white)
            )

        self.sidebar_button_2.bind("<Enter>", on_hover_2)
        self.sidebar_button_2.bind("<Leave>", off_hover_2)
        self.sidebar_button_2.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        # ---- Records ----
        self.sidebar_button_3 = customtkinter.CTkButton(
            self.sidebar_frame, command=self.load_detections,
            text="Records", fg_color="transparent",
            height=60, text_color="white", corner_radius=15,
            anchor="w", font=("Google Sans Medium", 18),
            image=customtkinter.CTkImage(dark_image=img_records_white, light_image=img_records_white)
        )

        def on_hover_3(event):
            self.sidebar_button_3.configure(
                text_color="sea green", fg_color="white",
                image=customtkinter.CTkImage(dark_image=img_records_green, light_image=img_records_green)
            )

        def off_hover_3(event):
            self.sidebar_button_3.configure(
                text_color="white", fg_color="transparent",
                image=customtkinter.CTkImage(dark_image=img_records_white, light_image=img_records_white)
            )

        self.sidebar_button_3.bind("<Enter>", on_hover_3)
        self.sidebar_button_3.bind("<Leave>", off_hover_3)
        self.sidebar_button_3.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        # ---- Charts ----
        self.sidebar_button_4 = customtkinter.CTkButton(
            self.sidebar_frame, command=self.load_charts,
            text="Charts", fg_color="transparent",
            height=60, text_color="white", corner_radius=15,
            anchor="w", font=("Google Sans Medium", 18),
            image=customtkinter.CTkImage(dark_image=img_chart_white, light_image=img_chart_white)
        )

        def on_hover_4(event):
            self.sidebar_button_4.configure(
                text_color="sea green", fg_color="white",
                image=customtkinter.CTkImage(dark_image=img_chart_green, light_image=img_chart_green)
            )

        def off_hover_4(event):
            self.sidebar_button_4.configure(
                text_color="white", fg_color="transparent",
                image=customtkinter.CTkImage(dark_image=img_chart_white, light_image=img_chart_white)
            )

        self.sidebar_button_4.bind("<Enter>", on_hover_4)
        self.sidebar_button_4.bind("<Leave>", off_hover_4)
        self.sidebar_button_4.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        self.toplevel_window = None

    # ---- Top-level message ----
    def open_toplevel(self, folder_path):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self, folder_path)
        else:
            self.toplevel_window.focus()

    # ---- Single Image Detection ----
    def select_image(self):
        file_path = filedialog.askopenfilename()
        results = model(file_path)

        for result in results:
            result.show()
            result.save(filename='result.jpg')

    # ---- Batch Detection ----
    def select_batch(self):
        folder_path = filedialog.askdirectory()
        results = model(folder_path)
        num_images_detected = len(results)
        print(f"Number of images detected: {num_images_detected}")

        detections_count = {i: 0 for i in range(11)}
        class_names = {
            0: 'sugarcane_yellow', 1: 'sugarcane_redspot', 2: 'sugarcane_healthy',
            3: 'maize_grayleaf', 4: 'maize_rust', 5: 'maize_healthy', 6: 'maize_blight',
            7: 'banana_cordana', 8: 'banana_pestalotiopsis', 9: 'banana_healthy', 10: 'banana_sigatoka'
        }

        for i, result in enumerate(results):
            timestamp = int(time.time() * 1000)
            result_filename = os.path.join(folder_path, f'result_{timestamp}_{i}.jpg')
            result.save(filename=result_filename)

            for detection in result.boxes:
                class_id = int(detection.cls)
                if class_id in detections_count:
                    detections_count[class_id] += 1
                else:
                    print(f"Unknown class detected: {class_id}")

        detected_classes = {class_names[class_id]: count for class_id, count in detections_count.items() if count > 0}
        total_unique_classes = len(detected_classes)
        total_classes_not_detected = 11 - total_unique_classes
        detection_effectiveness = (num_images_detected / (num_images_detected + total_classes_not_detected)) * 100

        print(f"Total unique classes detected: {total_unique_classes}")
        print("Detection count per class:")
        for name, count in detected_classes.items():
            print(f"{name}: {count}")

        # ---- Database ----
        connection = get_connection()
        if connection is None:
            print("Error: Could not connect to the database.")
            return

        try:
            with connection.cursor() as cursor:
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                sql_detections = "INSERT INTO detections (timestamp, num_images, num_diseases) VALUES (%s, %s, %s)"
                cursor.execute(sql_detections, (timestamp, num_images_detected, total_unique_classes))
                detection_id = cursor.lastrowid

                for class_name, count in detected_classes.items():
                    sql_details = "INSERT INTO detection_details (detection_id, class_name, count) VALUES (%s, %s, %s)"
                    cursor.execute(sql_details, (detection_id, class_name, count))

            connection.commit()
            print("Data successfully inserted into database.")
        except pymysql.Error as e:
            print(f"Database insertion error: {e}")
        finally:
            connection.close()

        # ---- Report Generation ----
        report_filename = os.path.join(folder_path, 'detection_report.pdf')
        c = canvas.Canvas(report_filename, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 16)
        c.drawString(200, height - 60, "Detection Report")

        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, height - 140, f"Total Detections -------------------------------------------- {num_images_detected}")
        c.drawString(50, height - 160, f"Total Unique Classes --------------------------------------- {total_unique_classes}")
        c.drawString(50, height - 180, f"Classes Not Detected --------------------------------------- {total_classes_not_detected}")
        c.drawString(50, height - 200, f"Detection Effectiveness ------------------------------------ {detection_effectiveness:.2f}%")

        # AI Recommendations
        api_key = ""  # <-- put your OpenAI API key
        client = OpenAI(api_key=api_key)

        diseases_detected = ", ".join(detected_classes.keys())
        prompt = f"""
My AI pathology detection model has detected these diseases ({diseases_detected}).
Sugarcane yellow corresponds to the fungus Mycovellosiella koepkei,
sugarcane redspot corresponds to red rot, grayleaf is gray leaf spot,
rust is rust, blight is leaf blight, cordana, pestalotiopsis, and sigatoka
are banana fungi. Recommend treatments, procedures to follow, severity,
and prevention methods. Write it technically, wrapping every 60 characters.
Do not conclude; format it as a technical report.
"""

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-3.5-turbo",
        )
        recommendations = chat_completion.choices[0].message.content

        c.drawString(50, height - 240, "Recommendations")
        c.setFont("Helvetica", 11)

        wrapped_text = textwrap.wrap(recommendations, width=95)
        y_pos = height - 260

        for line in wrapped_text:
            c.drawString(50, y_pos, line)
            y_pos -= 15

        # ---- Charts ----
        labels = list(detected_classes.keys())
        sizes = list(detected_classes.values())

        # Pie Chart
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title('Detection Distribution by Class')
        plt.axis('equal')
        pie_chart_path = os.path.join(folder_path, 'pie_chart.png')
        plt.savefig(pie_chart_path)
        plt.close()

        # Bar Chart
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(labels, sizes, color='skyblue')
        plt.title('Detection Count by Class')
        plt.xlabel('Classes')
        plt.ylabel('Number of Detections')
        plt.xticks(rotation=90)
        plt.tight_layout()
        bar_chart_path = os.path.join(folder_path, 'bar_chart.png')
        plt.savefig(bar_chart_path)
        plt.close()

        chart_width = 500
        c.drawImage(pie_chart_path, 50, 400, width=chart_width, preserveAspectRatio=True, mask='auto')
        c.drawImage(bar_chart_path, 50, -40, width=chart_width, preserveAspectRatio=True, mask='auto')
        c.save()

        self.open_toplevel(folder_path)

    # ---- Load Detection Records ----
    def load_detections(self):
        for widget in self.center_frame.winfo_children():
            widget.destroy()

        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM detections"
        cursor.execute(query)
        detections = cursor.fetchall()
        conn.close()

        headers = ["ID", "Detection Date", "Number of Detections", "Number of Diseases"]
        table_frame = customtkinter.CTkFrame(self.center_frame, width=410, fg_color="sea green", corner_radius=10)
        table_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        for i, header in enumerate(headers):
            label = customtkinter.CTkLabel(table_frame, text=header, font=("Arial", 14, "bold"), text_color="white")
            label.grid(row=0, column=i, padx=5, pady=5)

        for i, detection in enumerate(detections):
            for j, value in enumerate(detection):
                label = customtkinter.CTkLabel(table_frame, text=value, font=("Arial", 12), text_color="white")
                label.grid(row=i + 1, column=j, padx=5, pady=5)

    # ---- Load Charts ----
    def load_charts(self):
        for widget in self.center_frame.winfo_children():
            widget.destroy()

        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT class_name, SUM(count) FROM detection_details GROUP BY class_name"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()

        class_names = [row[0] for row in data]
        counts = [row[1] for row in data]

        # Pie Chart
        fig1, ax1 = plt.subplots(figsize=(3, 3))
        ax1.pie(counts, labels=class_names, autopct='%1.1f%%', startangle=45, labeldistance=1, textprops={'fontsize': 8})
        ax1.axis('equal')
        ax1.set_title("Overall Disease Distribution")

        pie_chart = FigureCanvasTkAgg(fig1, master=self.center_frame)
        pie_chart.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Histogram
        fig2, ax2 = plt.subplots(figsize=(5, 3.4))
        ax2.hist(class_names, weights=counts, bins=len(class_names), color='skyblue', edgecolor='black')
        ax2.set_title('Disease Distribution')
        ax2.set_xlabel('Diseases')
        ax2.set_ylabel('Count')
        plt.xticks(rotation=45, ha='right', fontsize=8)

        hist_chart = FigureCanvasTkAgg(fig2, master=self.center_frame)
        hist_chart.get
