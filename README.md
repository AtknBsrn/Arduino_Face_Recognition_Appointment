Arduino Face Recognition Appointment System

This project is a **face recognition-based appointment reminder system** using **Arduino** and **Python**.  
It detects a person using a **Logitech Brio 100 camera**, tracks their face using **servo motors**, and checks if they have an appointment stored in the database.  

If an appointment is detected, the system provides a **voice reminder**.

Features
✔ **Face recognition** using OpenCV & face_recognition  
✔ **Real-time face tracking** with Arduino & SG90 servo motors  
✔ **SQLite3 database** for storing users and their appointments  
✔ **Voice reminders** using gTTS (Google Text-to-Speech)  
✔ **Auto scanning mode** when no face is detected  

Installation & Setup

Install Required Python Packages**
Make sure you have all dependencies installed before running the project.  
Run the following command to install them:  

pip install -r requirements.txt

Before starting the system, you need to register a face in the database.
Run the following command and follow the instructions:

python add_face_to_db.py

Once the face is registered, add an appointment time:

python add_appointment.py

Now you can start the system with:

python main.py

The system will scan for faces.
If a recognized face is detected, it will check the database for an appointment.
If the current time matches the appointment, the system will play a voice reminder.

Hardware Requirements
Component	Description
🖥 Raspberry Pi / PC	Runs the face recognition and processing.
🎥 Logitech Brio 100	Captures live video for face detection.
🎤 Brio 100 Microphone	Used for voice commands & reminders.
🎛 Arduino Uno R4 WiFi	Controls the servo motors.
⚙ SG90 Servo Motors (x2)	One for horizontal movement, one for vertical.
🔊 Speaker (2W 8Ω)	Outputs voice reminders.
🔌 Wires & Breadboard	For circuit connections.

System Workflow
1️ Face detection & tracking:

The camera continuously scans for faces.
If a face is detected, the servos move to center it in the frame.
2️ Appointment check:

If the detected face is stored in the database, it checks for a scheduled appointment.
3️ Voice reminder:

If an appointment is found and it is within 10 or 5 minutes, the system will play a voice reminder using gTTS.
4️ Auto scanning mode:

If no face is detected, the camera moves automatically to search for a person.

Important Notes
⚠ Make sure the correct Arduino port is set before running the script.
⚠ Use add_face_to_db.py first, then add_appointment.py, before running main.py.

