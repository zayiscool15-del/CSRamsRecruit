import base64
import io
import random
import smtplib

from email.mime.text import MIMEText
from flask import Flask, render_template, render_template_string, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import qrcode
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

app = Flask(__name__)
app.secret_key = "csrams_secret_key"


@app.route("/url")
def function_name():
    return render_template_string(""" HTML HERE """)


# ======================
# DATABASE
# ======================
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ======================
# EMAIL FUNCTION (REAL EMAIL READY)
# ======================

def send_email(to_email, subject, html_message):
    sender_email = "your_email@gmail.com"
    app_password = "your_app_password"

    msg = MIMEText(html_message, "html")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print("Email failed:", e)


# ======================
# MODELS
# ======================
class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    password = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    location = db.Column(db.String(120))
    program = db.Column(db.String(200))
    semester = db.Column(db.String(50))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    parent_email = db.Column(db.String(120))
    interest = db.Column(db.String(100))
    location = db.Column(db.String(100))
    password = db.Column(db.String(200))


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))


# ======================
# CREATE DATABASE + DEFAULT TEACHER
# ======================
with app.app_context():
    db.create_all()

    if not Teacher.query.filter_by(username="admin").first():
        teacher = Teacher(
            username="admin",
            password=generate_password_hash("admin123")
        )
        db.session.add(teacher)
        db.session.commit()

# ======================
# RED STYLE TEMPLATE FOR OTHER PAGES
# ======================

def red_style(content):
    return f"""
    <html>
    <head>
    <style>

        body {{
    margin: 0;
    font-family: Arial, sans-serif;
    background:
        linear-gradient(rgba(92, 0, 0, 0.75), rgba(92, 0, 0, 0.75)),
        url('/static/ra3.jpg');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: white;
    text-align: center;
}}

        .page-banner {{
            width: 100%;
            max-height: 220px;
            object-fit: contain;
            background: white;
            padding: 20px 0 10px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        }}

        .page-content {{
            padding: 30px 20px;
        }}

        h1 {{
            font-size: 3em;
            color: #ffffff;
            margin-bottom: 10px;
        }}

        h2 {{
            color: #ffd6d6;
            margin-bottom: 15px;
        }}

        p {{
            font-size: 1.08em;
            line-height: 1.7;
        }}

        .btn {{
            display: inline-block;
            padding: 12px 25px;
            margin: 10px;
            background: white;
            color: #8B0000;
            text-decoration: none;
            border-radius: 25px;
            font-weight: bold;
            transition: 0.3s ease;
        }}

        .btn:hover {{
            background: #ffe6e6;
            transform: translateY(-2px);
        }}

        .card {{
            background: rgba(255,255,255,0.14);
            padding: 20px;
            border-radius: 16px;
            margin: 10px;
            display: inline-block;
            width: 260px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.25);
        }}

        .section {{
            margin-top: 50px;
            background: white;
            padding: 35px 30px;
            border-radius: 20px;
            box-shadow: 0 12px 30px rgba(0,0,0,0.18);
            color: #222;
        }}

        .section h2 {{
            color: #8B0000;
            margin-bottom: 10px;
        }}

        .section p {{
            color: #444;
        }}

        .program-list {{
            max-width: 1000px;
            margin: 30px auto;
        }}

        .program-card {{
            display: block;
            background: #ffffff;
            padding: 22px;
            margin-bottom: 18px;
            border-radius: 16px;
            text-decoration: none;
            color: #222;
            transition: all 0.3s ease;
            border-left: 6px solid #8B0000;
            box-shadow: 0 6px 18px rgba(0,0,0,0.12);
        }}

        .program-card h3 {{
            margin: 0 0 10px 0;
            color: #8B0000;
        }}

        .program-card p {{
            margin: 0 0 12px 0;
            color: #555;
        }}

        .program-card .view-link {{
            font-weight: bold;
            color: #000;
        }}

        .program-card:hover {{
            transform: translateY(-5px);
            background: #f9f9f9;
            box-shadow: 0 12px 28px rgba(0,0,0,0.2);
        }}

        /* CONTACT CARD UPGRADE */
        .contact-card {{
            max-width: 520px;
            margin: 20px auto 40px auto;
            padding: 25px;
            background: white;
            border-radius: 18px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.18);
            color: #222;
        }}

        .contact-card h3 {{
            color: #8B0000;
        }}

        .contact-card a {{
            color: #8B0000;
        }}

        /* BUTTONS CLEAN */
        .btn {{
            display: inline-block;
            padding: 12px 25px;
            margin: 10px;
            background: #8B0000;
            color: white;
            text-decoration: none;
            border-radius: 25px;
            font-weight: bold;
            transition: 0.3s ease;
        }}

        .btn:hover {{
            background: white;
        }}

        .gallery-card {{
            display: block;
            background: rgba(255,255,255,0.12);
            border-radius: 22px;
            overflow: hidden;
            box-shadow: 0 12px 30px rgba(0,0,0,0.35);
            border: 1px solid rgba(255,255,255,0.12);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            text-decoration: none;
        }}

        .gallery-card:hover {{
            transform: translateY(-6px) scale(1.02);
            box-shadow: 0 18px 40px rgba(0,0,0,0.42);
        }}

        .gallery-card img {{
            width: 100%;
            height: 320px;
            object-fit: cover;
            display: block;
            cursor: pointer;
        }}

        .gallery-card p {{
            margin: 0;
            padding: 16px 18px;
            color: #fff7f7;
            background: rgba(0,0,0,0.16);
        }}

        .video-card {{
            max-width: 850px;
            margin: 30px auto;
            background: rgba(255,255,255,0.12);
            padding: 25px;
            border-radius: 22px;
            box-shadow: 0 12px 30px rgba(0,0,0,0.35);
            border: 1px solid rgba(255,255,255,0.10);
        }}

        .video-card h3 {{
            color: #ffcccc;
            margin-bottom: 15px;
        }}

        .video-card p {{
            color: #f7eaea;
            line-height: 1.6;
        }}

        input, select, textarea {{
            padding: 10px;
            margin: 8px;
            border: 1px solid #8B0000;
            border-radius: 5px;
        }}

        button {{
            background: #8B0000;
            color: white;
            padding: 10px 20px;
            border-radius: 20px;
            border: none;
            cursor: pointer;
        }}

        button:hover {{
            background: #a30000;
        }}

        table {{
            margin: auto;
            border-collapse: collapse;
            background: white;
            color: #8B0000;
        }}

        th, td {{
            border: 1px solid #8B0000;
            padding: 10px;
        }}

        a {{
            color: #8B0000;
            text-decoration: none;
            font-weight: bold;
        }}

        a:hover {{
            text-decoration: underline;
        }}
    </style>
    </head>
    <body>

        <div class="page-content">
            {content}
        </div>
    </body>
    </html>
   """
url = "https://csramsrecruit.onrender.com/"

# Generate QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

# Create an image
img = qr.make_image(fill_color="black", back_color="white")

# Save the image
img.save("rams_recruit_qr.png")

print("QR code saved as rams_recruit_qr.png")


@app.route("/")
def home():
    url = "https://csramsrecruit.onrender.com/"
    qr = qrcode.QRCode(box_size=6, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    qr_b64 = base64.b64encode(buf.getvalue()).decode("ascii")

    return f"""
    <html>
    <head>
        <title>WSSU CS Open House</title>
        <style>
            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background:
                    linear-gradient(rgba(92, 0, 0, 0.58), rgba(92, 0, 0, 0.58)),
                    url('/static/campus.jpg');
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
                color: white;
                text-align: center;
            }}

            .container {{
                max-width: 900px;
                margin: auto;
                padding: 90px 20px;
            }}

            .hero-logo {{
                max-width: 240px;
                width: 100%;
                margin-bottom: 20px;
                border-radius: 18px;
                background: rgba(255,255,255,0.92);
                padding: 10px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.25);
            }}

            h1 {{
                font-size: 3em;
                margin-bottom: 10px;
            }}

            p {{
                font-size: 1.1em;
                line-height: 1.6;
            }}

            .qr-box {{
                margin: 30px 0;
            }}

            .qr-box img {{
                background: white;
                padding: 12px;
                border-radius: 16px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.25);
            }}

            .btn {{
                display: inline-block;
                padding: 12px 25px;
                margin: 10px;
                background: white;
                color: #8B0000;
                text-decoration: none;
                border-radius: 25px;
                font-weight: bold;
                transition: 0.3s ease;
            }}

            .btn:hover {{
                background: #ffe6e6;
                transform: translateY(-2px);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <img src="/static/ra3.jpg" alt="WSSU Logo" class="hero-logo">

            <h1>Welcome to WSSU CS Open House</h1>
            <p>Connect with Computer Science and Information Technology at Winston-Salem State University.</p>

            <div class="qr-box">
                <img src="data:image/png;base64,{qr_b64}" alt="QR Code">
            </div>

            <a href="/Programs" class="btn">Explore Programs</a>
            <a href="/student_login" class="btn">Student Login</a>
            <a href="/login" class="btn">Teacher Login</a>
        </div>
    </body>
    </html>
    """

@app.route("/Programs")
def Program():
    return """
    <html>
    <head>
        <title>Explore Computer Science & IT</title>
        <style>
            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background:
                    linear-gradient(rgba(92, 0, 0, 0.68), rgba(92, 0, 0, 0.68)),
                    url('/static/campus.jpg');
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
                color: white;
                text-align: center;
            }

            .container {
                padding: 60px 20px;
                max-width: 1200px;
                margin: auto;
            }

            h1 {
                font-size: 3em;
                margin-bottom: 10px;
                color: white;
            }

            h2 {
                color: #8B0000;
                margin-bottom: 15px;
            }

            p {
                line-height: 1.7;
            }

            .top-logo {
                max-width: 320px;
                width: 100%;
                margin-bottom: 20px;
                border-radius: 18px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.25);
                background: white;
                padding: 10px;
            }

            .contact-card {
                max-width: 560px;
                margin: 20px auto 35px auto;
                padding: 24px;
                background: white;
                color: #222;
                border-radius: 18px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.18);
            }

            .contact-card h3 {
                margin-top: 0;
                color: #8B0000;
            }

            .contact-card a {
                color: #8B0000;
                text-decoration: none;
                font-weight: bold;
            }

            .contact-card a:hover {
                text-decoration: underline;
            }

            .section {
                margin-top: 50px;
                background: white;
                padding: 35px 30px;
                border-radius: 20px;
                box-shadow: 0 12px 30px rgba(0,0,0,0.18);
                color: #222;
            }

            .section p {
                color: #444;
            }

            .btn {
    display: inline-block;
    padding: 12px 25px;
    margin: 10px;
    background: #8B0000;
    color: white !important;   /* 🔥 THIS FIXES IT */
    text-decoration: none;
    border-radius: 25px;
    font-weight: bold;
    transition: 0.3s ease;
}

.btn:hover {
    background: black;
    color: white !important;   /* 🔥 keeps text white on hover */
}

            .program-list {
                max-width: 1000px;
                margin: 30px auto 0 auto;
            }

            .program-card {
                display: block;
                background: #ffffff;
                padding: 22px;
                margin-bottom: 18px;
                border-radius: 16px;
                text-decoration: none;
                color: #222;
                transition: all 0.3s ease;
                border-left: 6px solid #8B0000;
                box-shadow: 0 6px 18px rgba(0,0,0,0.12);
                text-align: left;
            }

            .program-card h3 {
                margin: 0 0 10px 0;
                color: #8B0000;
            }

            .program-card p {
                margin: 0 0 12px 0;
                color: #555;
            }

            .program-card .view-link {
                font-weight: bold;
                color: black;
            }

            .program-card:hover {
                transform: translateY(-5px);
                background: #f9f9f9;
                box-shadow: 0 12px 28px rgba(0,0,0,0.2);
            }

            .gallery-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
                gap: 28px;
                margin-top: 25px;
            }

            .gallery-card {
                display: block;
                background: white;
                border-radius: 18px;
                overflow: hidden;
                box-shadow: 0 10px 25px rgba(0,0,0,0.18);
                transition: 0.3s ease;
                text-decoration: none;
                color: black;
            }

            .gallery-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 16px 34px rgba(0,0,0,0.24);
            }

            .gallery-card img {
                width: 100%;
                height: 300px;
                object-fit: cover;
                display: block;
            }

            .gallery-card p {
                padding: 14px;
                margin: 0;
                color: #333;
                background: white;
            }

            .video-card {
                max-width: 900px;
                margin: 20px auto 0 auto;
                background: white;
                padding: 24px;
                border-radius: 18px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.18);
                color: #222;
            }

            .video-card h3 {
                color: #8B0000;
                margin-top: 0;
            }

            .video-card p {
                color: #444;
            }
        </style>
    </head>
    <body>
        <div class="container">

            <img src="/static/ra3.jpg" alt="WSSU Banner" class="top-logo">

            <h1>Explore Computer Science & IT</h1>
            <p><b>Winston-Salem State University</b></p>

            <div class="contact-card">
                <h3>Computer Science Department</h3>
                <p>
                    <b>Department:</b> Computer Science<br>
                    📞 <a href="tel:13367502480">336-750-2480</a><br>
                    ✉️ <a href="mailto:jonese@wssu.edu">jonese@wssu.edu</a>
                </p>

                <a href="/register" class="btn">Student Registration</a>
                <a href="/student_login" class="btn">Student Login</a>
                <a href="/login" class="btn">Teacher Login</a>
            </div>

            <div class="section">
                <h2>Programs of Study</h2>
                <p>
                    Click a program below to learn more about course options, student experience,
                    and opportunities at Winston-Salem State University.
                </p>

                <div class="program-list">
                    <a href="/program/cs" class="program-card">
                        <h3>Bachelor of Science in Computer Science</h3>
                        <p>Advanced programming, cybersecurity, AI, and high-performance computing.</p>
                        <span class="view-link">View Program -&gt;</span>
                    </a>

                    <a href="/program/it" class="program-card">
                        <h3>Bachelor of Science in Information Technology</h3>
                        <p>Hands-on IT training with networking, systems, and internships.</p>
                        <span class="view-link">View Program -&gt;</span>
                    </a>

                    <a href="/program/ms" class="program-card">
                        <h3>MS in Computer Science & Information Technology</h3>
                        <p>Graduate-level specialization in cybersecurity, AI, and data science.</p>
                        <span class="view-link">View Program -&gt;</span>
                    </a>

                    <a href="/program/minorcs" class="program-card">
                        <h3>Computer Science Minor</h3>
                        <p>Enhance your major with strong programming and database skills.</p>
                        <span class="view-link">View Program -&gt;</span>
                    </a>

                    <a href="/program/datascience" class="program-card">
                        <h3>Data Science Minor</h3>
                        <p>Data analytics, AI foundations, and interdisciplinary applications.</p>
                        <span class="view-link">View Program -&gt;</span>
                    </a>

                    <a href="/program/programmingcert" class="program-card">
                        <h3>Certificate in Computer Programming</h3>
                        <p>Perfect for career changers seeking technical programming skills.</p>
                        <span class="view-link">View Program -&gt;</span>
                    </a>

                    <a href="/program/datacert" class="program-card">
                        <h3>Certificate in Data Analytics</h3>
                        <p>Professional online certificate in data mining and visualization.</p>
                        <span class="view-link">View Program -&gt;</span>
                    </a>
                </div>
            </div>

            <div class="section">
                <h2>Life in Computer Science & IT at WSSU</h2>

                <div class="gallery-grid">
                    <a class="gallery-card" href="/static/ra1.jpg" target="_blank">
                        <img src="/static/ra1.jpg" alt="WSSU student life 1">
                        <p>Student collaboration and engagement.</p>
                    </a>

                    <a class="gallery-card" href="/static/ra2.webp" target="_blank">
                        <img src="/static/ra2.webp" alt="WSSU student life 2">
                        <p>Hands-on learning and technology opportunities.</p>
                    </a>

                    <a class="gallery-card" href="/static/ra4.jpg" target="_blank">
                        <img src="/static/ra4.jpg" alt="WSSU lab experience">
                        <p>Modern spaces for growth, creativity, and innovation.</p>
                    </a>

                    <a class="gallery-card" href="/static/ra5.jpg" target="_blank">
                        <img src="/static/ra5.jpg" alt="WSSU student success">
                        <p>Student success, mentorship, and campus pride.</p>
                    </a>
                </div>
            </div>

            <div class="section">
                <h2>Student Voices</h2>

                <div class="video-card">
                    <h3>Student Experience at WSSU</h3>

                    <video controls preload="metadata" playsinline poster="/static/ra3.jpg" style="width:100%; max-width:900px; border-radius:18px; box-shadow:0 12px 30px rgba(0,0,0,0.35);">
                        <source src="/static/video/ram.mp4" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>

                    <p style="margin-top:15px;">
                        "WSSU gave me hands-on learning and confidence in tech."
                    </p>
                </div>
            </div>

            <br>
            <a href="/register" class="btn">Apply Now</a>
            <a href="/" class="btn">Back Home</a>

        </div>
    </body>
    </html>
    """
# ======================
# STUDENT REGISTER
# ======================
@app.route("/register", methods=["GET", "POST"])
def register_program():
    if request.method == "POST":
        first_name = request.form.get("name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        location = request.form.get("location")
        program = request.form.get("program")
        semester = request.form.get("semester")
        password = request.form.get("password")

        name = first_name + " " + last_name
        hashed_password = generate_password_hash(password)
        student_id = "WSSU" + str(random.randint(10000, 99999))

        new_reg = Registration(
            student_id=student_id,
            name=name,
            email=email,
            phone=phone,
            location=location,
            program=program,
            semester=semester,
            password=hashed_password
        )

        db.session.add(new_reg)
        db.session.commit()

        return redirect(f"/confirmation/{student_id}")

    return red_style("""
    <h2>WSSU Program Registration</h2>

    <form method="POST" style="max-width:450px;margin:auto;background:white;padding:25px;border-radius:15px;box-shadow:0 4px 12px rgba(0,0,0,0.2);">

        <input name="name" placeholder="First Name" required style="width:90%;"><br>
        <input name="last_name" placeholder="Last Name" required style="width:90%;"><br>
        <input type="email" name="email" placeholder="Email" required style="width:90%;"><br>
        <input name="phone" placeholder="Phone Number" style="width:90%;"><br>
        <input name="location" placeholder="City / State" style="width:90%;"><br>
        <input type="password" name="password" placeholder="Create Password" required style="width:90%;"><br>

        <select name="program" required style="width:95%;">
            <option value="">Select Program of Interest</option>
            <option value="Computer Science">Computer Science</option>
            <option value="Information Technology">Information Technology</option>
            <option value="Cybersecurity">Cybersecurity</option>
            <option value="Data Science">Data Science</option>
            <option value="Software Engineering">Software Engineering</option>
            <option value="Artificial Intelligence">Artificial Intelligence</option>
            <option value="Networking">Networking</option>
        </select><br><br>

        <select name="semester" required style="width:95%;">
            <option value="">Select Entry Semester</option>
            <option value="Fall 2026">Fall 2026</option>
            <option value="Spring 2027">Spring 2027</option>
            <option value="Summer 2026">Summer 2026</option>
        </select><br><br>

        <button style="width:60%;">Register</button>
    </form>
    """)


@app.route("/confirmation/<student_id>")
def confirmation(student_id):
    reg = Registration.query.filter_by(student_id=student_id).first_or_404()

    return red_style(f"""
    <div style="max-width:600px;margin:40px auto;background:white;padding:30px;border-radius:15px;box-shadow:0 4px 12px rgba(0,0,0,0.2);">
        <h2 style="color:green;">Registration Successful</h2>

        <p><b>Student ID:</b> {reg.student_id}</p>
        <p><b>Name:</b> {reg.name}</p>
        <p><b>Email:</b> {reg.email}</p>
        <p><b>Phone:</b> {reg.phone}</p>
        <p><b>Location:</b> {reg.location}</p>
        <p><b>Program:</b> {reg.program}</p>
        <p><b>Semester:</b> {reg.semester}</p>

        <br>
        <a href="/Programs">Back to Programs</a>
    </div>
    """)


@app.route("/admin")
def admin():
    if "user" not in session:
        return redirect("/login")

    registrations = Registration.query.all()

    return render_template_string("""
    <html>
    <head>
        <style>
            body { font-family: Arial; background:#111; color:white; }
            table { width:100%; border-collapse: collapse; }
            th, td { padding:10px; border:1px solid white; }
            th { background:#ff4d4d; }
        </style>
    </head>
    <body>
        <h1>Admin Registration Dashboard</h1>
        <table>
            <tr>
                <th>Student ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Program</th>
                <th>Semester</th>
            </tr>
            {% for r in registrations %}
            <tr>
                <td>{{ r.student_id }}</td>
                <td>{{ r.name }}</td>
                <td>{{ r.email }}</td>
                <td>{{ r.program }}</td>
                <td>{{ r.semester }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """, registrations=registrations)


# ======================
# STUDENT LOGIN
# ======================
@app.route("/student_login", methods=["GET", "POST"])
def student_login():
    message = ""

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        student = Registration.query.filter_by(email=email).first()

        if student and check_password_hash(student.password, password):
            session["student"] = student.student_id
            return redirect("/student_dashboard")
        else:
            message = "Invalid email or password."

    return red_style(f"""
    <div class="container">
                     <img src="/static/ra3.jpg" 
     style="display:block;margin:20px auto;max-width:200px;width:100%;
     border-radius:16px;box-shadow:0 8px 20px rgba(0,0,0,0.2);
     background:white;padding:10px;">
        <h1>Student Login</h1>
        <p>Access your WSSU Computer Science & IT student dashboard.</p>

        <div style="max-width:420px;margin:auto;background:white;padding:30px;border-radius:18px;box-shadow:0 8px 22px rgba(0,0,0,0.2);">
            <form method="POST">
                <input type="email" name="email" placeholder="Email" required style="width:90%;"><br>
                <input type="password" name="password" placeholder="Password" required style="width:90%;"><br>
                <button style="width:70%;">Login</button>
            </form>

            <p style="color:red;margin-top:15px;">{message}</p>

            <p style="margin-top:15px;">
                Don't have an account? <a href="/register">Register here</a>
            </p>
        </div>
    </div>
    """)

# ======================
# STUDENT DASHBOARD
# ======================
@app.route("/student_dashboard")
def student_dashboard():
    if "student" not in session:
        return redirect("/student_login")

    student = Registration.query.filter_by(student_id=session["student"]).first()

    if not student:
        return redirect("/student_login")

    course_map = {
        "Computer Science": ["Algorithms", "Operating Systems", "Artificial Intelligence"],
        "Information Technology": ["Networking", "Cloud Computing", "System Administration"],
        "Data Science": ["Machine Learning", "Data Mining", "Data Visualization"],
        "Cybersecurity": ["Ethical Hacking", "Network Security", "Digital Forensics"],
        "Software Engineering": ["Software Design", "Web Development", "Testing and QA"],
        "Artificial Intelligence": ["Machine Learning", "Neural Networks", "AI Ethics"],
        "Networking": ["Network Security", "Routing and Switching", "Cloud Infrastructure"]
    }

    recommended = course_map.get(student.program, [])
    course_html = "".join([f"<li>{c}</li>" for c in recommended])

    return red_style(f"""
    <div class="container">
                     <img src="/static/ra3.jpg" 
     style="max-width:220px;width:100%;margin-bottom:20px;border-radius:16px;
     box-shadow:0 8px 20px rgba(0,0,0,0.2);background:white;padding:10px;">
        <h1>Student Dashboard</h1>

        <div style="max-width:900px;margin:auto;display:grid;grid-template-columns:1fr 1fr;gap:25px;">
            <div style="background:white;color:#8B0000;padding:25px;border-radius:18px;box-shadow:0 8px 22px rgba(0,0,0,0.2);">
                <h2 style="color:#8B0000;">Student Information</h2>
                <p><b>Student ID:</b> {student.student_id}</p>
                <p><b>Name:</b> {student.name}</p>
                <p><b>Email:</b> {student.email}</p>
                <p><b>Program:</b> {student.program}</p>
                <p><b>Semester:</b> {student.semester}</p>
                <p><b>Location:</b> {student.location}</p>
            </div>

            <div style="background:white;color:#8B0000;padding:25px;border-radius:18px;box-shadow:0 8px 22px rgba(0,0,0,0.2);">
                <h2 style="color:#8B0000;">Recommended Courses</h2>
                <ul style="text-align:left;display:block;">
                    {course_html}
                </ul>
            </div>
        </div>

        <br>
        <a href="/Programs" class="btn">Explore Programs</a>
        <a href="/logout_student" class="btn">Logout</a>
    </div>
    """)

@app.route("/logout_student")
def logout_student():
    session.pop("student", None)
    return redirect("/")


# ======================
# TEACHER LOGIN
# ======================
@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = Teacher.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user"] = user.username
            return redirect("/teacher")
        else:
            message = "Invalid username or password."

    return red_style(f"""
    <div class="container">
                     <img src="/static/ra3.jpg" 
     style="display:block;margin:20px auto;max-width:200px;width:100%;
     border-radius:16px;box-shadow:0 8px 20px rgba(0,0,0,0.2);
     background:white;padding:10px;">
        <h1>Teacher Login</h1>
        <p>Sign in to manage student registrations and view the dashboard.</p>

        <div style="max-width:420px;margin:auto;background:white;padding:30px;border-radius:18px;box-shadow:0 8px 22px rgba(0,0,0,0.2);">
            <form method="POST">
                <input name="username" placeholder="Username" required style="width:90%;"><br>
                <input type="password" name="password" placeholder="Password" required style="width:90%;"><br>
                <button style="width:70%;">Login</button>
            </form>

            <p style="color:red;margin-top:15px;">{message}</p>
        </div>
    </div>
    """)


# ======================
# TEACHER DASHBOARD (UPGRADED)
# ======================
@app.route("/teacher", methods=["GET"])
def teacher():
    if "user" not in session:
        return redirect("/login")

    search_id = request.args.get("student_id", "").strip()

    if search_id:
        registrations = Registration.query.filter(
            Registration.student_id.ilike(f"%{search_id}%")
        ).all()
    else:
        registrations = Registration.query.all()

    rows = ""
    for r in registrations:
        rows += f"""
        <tr>
            <td>{r.student_id}</td>
            <td>{r.name}</td>
            <td>{r.email}</td>
            <td>{r.phone}</td>
            <td>{r.location}</td>
            <td>{r.program}</td>
            <td>{r.semester}</td>
            <td>
                <a href="/contact_registration/{r.id}" class="btn" style="padding:8px 14px;font-size:0.9em;">Contact</a>
            </td>
            <td>
                <a href="/delete_registration/{r.id}"
                   onclick="return confirm('Are you sure you want to remove this student?')"
                   class="btn"
                   style="padding:8px 14px;font-size:0.9em;background:black;">
                   Remove
                </a>
            </td>
        </tr>
        """

    return red_style(f"""
    <div class="container">
        <img src="/static/ra3.jpg"
             style="display:block;margin:20px auto;max-width:200px;width:100%;
             border-radius:16px;box-shadow:0 8px 20px rgba(0,0,0,0.2);
             background:white;padding:10px;">

        <h1>Teacher Dashboard</h1>
        <p>Manage student registrations, search by Student ID, and contact students directly.</p>

        <div style="max-width:700px;margin:20px auto;background:white;padding:20px;border-radius:18px;box-shadow:0 8px 22px rgba(0,0,0,0.2);">
            <form method="GET" action="/teacher">
                <input name="student_id" placeholder="Search by Student ID"
                       value="{search_id}" style="width:60%;">
                <button type="submit">Search</button>
                <a href="/teacher" class="btn">Clear</a>
            </form>
        </div>

        <div style="overflow-x:auto;background:white;padding:20px;border-radius:18px;box-shadow:0 8px 22px rgba(0,0,0,0.2);">
            <table style="width:100%;">
                <tr>
                    <th>Student ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Location</th>
                    <th>Program</th>
                    <th>Semester</th>
                    <th>Contact</th>
                    <th>Remove</th>
                </tr>
                {rows if rows else '<tr><td colspan="9">No students found.</td></tr>'}
            </table>
        </div>

        <br>
        <a href="/Programs" class="btn">Explore Programs</a>
        <a href="/logout" class="btn">Logout</a>
    </div>
    """)
@app.route("/contact_registration/<int:id>", methods=["GET", "POST"])
def contact_registration(id):
    if "user" not in session:
        return redirect("/login")

    student = Registration.query.get_or_404(id)
    email = student.email

    if request.method == "POST":
        subject = request.form.get("subject", "Message from WSSU CS Program")
        message = request.form.get("message", "")

        send_email(email, subject, f"""
        <h3>Message from Winston-Salem State University</h3>
        <p>{message}</p>
        <br>
        <p><b>Student:</b> {student.name}</p>
        <p><b>Student ID:</b> {student.student_id}</p>
        """)

        return red_style(f"""
        <div class="container">
            <h2>Email Sent Successfully</h2>
            <p>Your message was sent to <b>{student.name}</b>.</p>
            <a href="/teacher" class="btn">Back to Dashboard</a>
        </div>
        """)

    return red_style(f"""
    <div class="container">
        <img src="/static/ra3.jpg"
             style="display:block;margin:20px auto;max-width:200px;width:100%;
             border-radius:16px;box-shadow:0 8px 20px rgba(0,0,0,0.2);
             background:white;padding:10px;">

        <h1>Contact Student</h1>

        <div style="max-width:700px;margin:auto;background:white;color:#8B0000;padding:25px;border-radius:18px;box-shadow:0 8px 22px rgba(0,0,0,0.2);">
            <p><b>Name:</b> {student.name}</p>
            <p><b>Student ID:</b> {student.student_id}</p>
            <p><b>Email:</b> {student.email}</p>

            <form method="POST">
                <input name="subject" placeholder="Subject" value="Message from WSSU CS Program" style="width:90%;"><br>
                <textarea name="message" placeholder="Type your message here..." style="width:90%;height:180px;"></textarea><br><br>
                <button>Send Email</button>
            </form>

            <br>
            <a href="/teacher" class="btn">Back to Dashboard</a>
        </div>
    </div>
    """)
@app.route("/delete_registration/<int:id>")
def delete_registration(id):
    if "user" not in session:
        return redirect("/login")

    student = Registration.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()

    return redirect("/teacher")

# ======================
# DELETE STUDENT / CONTACT
# ======================
@app.route("/contact/<int:id>/<type>", methods=["GET", "POST"])
def contact(id, type):
    if "user" not in session:
        return redirect("/login")

    student = Student.query.get_or_404(id)
    email = student.email if type == "student" else student.parent_email

    if request.method == "POST":
        message = request.form["message"]
        send_email(email, "Message from WSSU CS Program", f"<p>{message}</p>")

        return red_style("""
        <h3>Email Sent Successfully</h3>
        <a href='/teacher'>Back to Dashboard</a>
        """)

    return red_style(f"""
    <h2>Send Email to {type.title()}</h2>
    <p><b>To:</b> {email}</p>

    <form method="POST">
        <textarea name="message" style="width:300px;height:150px;"></textarea><br><br>
        <button>Send Email</button>
    </form>
    """)


# ======================
# LOGOUT
# ======================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

def program_page(title, contact_html, body_html):
    return render_template_string(f"""
    <html>
    <head>
        <title>{title}</title>
        <style>
            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f7f7f7;
                color: #222;
            }}

            .page-wrap {{
                max-width: 1000px;
                margin: 0 auto;
                padding: 40px 20px 60px 20px;
            }}

            .hero {{
                background: linear-gradient(rgba(139,0,0,0.92), rgba(139,0,0,0.92));
                color: white;
                border-radius: 22px;
                padding: 35px 30px;
                box-shadow: 0 12px 28px rgba(0,0,0,0.18);
                text-align: center;
                margin-bottom: 30px;
            }}

            .hero img {{
                max-width: 220px;
                width: 100%;
                background: white;
                border-radius: 18px;
                padding: 10px;
                margin-bottom: 20px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            }}

            .hero h1 {{
                margin: 0 0 10px 0;
                font-size: 2.4em;
            }}

            .contact-card {{
                background: white;
                border-left: 6px solid #8B0000;
                border-radius: 18px;
                padding: 22px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.10);
                margin-bottom: 25px;
            }}

            .contact-card strong {{
                color: #8B0000;
            }}

            .section {{
                background: white;
                border-radius: 18px;
                padding: 24px;
                margin-bottom: 22px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.10);
            }}

            .section h2 {{
                color: #8B0000;
                margin-top: 0;
                margin-bottom: 12px;
                border-bottom: 2px solid #f0d6d6;
                padding-bottom: 8px;
            }}

            .section p {{
                line-height: 1.7;
                color: #333;
            }}

            .section ul {{
                margin: 0;
                padding-left: 22px;
                color: #333;
                line-height: 1.8;
            }}

            .btn-row {{
                text-align: center;
                margin-top: 30px;
            }}

            .btn {{
                display: inline-block;
                padding: 12px 24px;
                margin: 8px;
                background: #8B0000;
                color: white;
                text-decoration: none;
                border-radius: 25px;
                font-weight: bold;
                transition: 0.3s ease;
            }}

            .btn:hover {{
                background: black;
            }}
        </style>
    </head>
    <body>
        <div class="page-wrap">
            <div class="hero">
                <img src="/static/ra3.jpg" alt="WSSU Banner">
                <h1>{title}</h1>
                <p>Winston-Salem State University</p>
            </div>

            <div class="contact-card">
                {contact_html}
            </div>

            {body_html}

            <div class="btn-row">
                <a href="/Programs" class="btn">Back to Programs</a>
                <a href="/register" class="btn">Apply Now</a>
            </div>
        </div>
    </body>
    </html>
    """)
# ======================
# PROGRAM DETAIL PAGES
# ======================
@app.route("/program/cs")
def cs():
    return program_page(
        "Bachelor of Science in Computer Science",
        """
        <strong>Department:</strong> Computer Science <br>
        <strong>Phone:</strong> 336-750-2480 <br>
        <strong>Email:</strong> jonese@wssu.edu
        """,
        """
        <div class="section">
            <h2>Program Overview</h2>
            <p>
            Computer science touches every part of modern society. Since 1981,
            WSSU has delivered a cutting-edge curriculum that adapts to the ever-changing tech industry.
            Almost all alumni are employed within six months of graduation.
            </p>
        </div>

        <div class="section">
            <h2>5-Year BS → MS Option</h2>
            <p>
            Add one year to your bachelor's degree and earn your Master’s degree early
            through our 5-Year (4+1) BS–MS track.
            </p>
        </div>

        <div class="section">
            <h2>Concentration Options</h2>
            <ul>
                <li>Computer Graphics</li>
                <li>Database Administration</li>
                <li>Internet Systems</li>
                <li>Information Security</li>
                <li>Networking</li>
                <li>High Performance Computing</li>
                <li>Space Science</li>
                <li>Computational Science</li>
                <li>Accounting</li>
                <li>Management</li>
                <li>Marketing</li>
                <li>Mathematics</li>
            </ul>
        </div>
        """
    )

@app.route("/program/it")
def it():
    return program_page(
        "Bachelor of Science in Information Technology",
        """
        <strong>Department:</strong> Information Technology <br>
        <strong>Phone:</strong> 336-750-2480 <br>
        <strong>Email:</strong> jonese@wssu.edu
        """,
        """
        <div class="section">
            <h2>Program Overview</h2>
            <p>
            Since 2007, WSSU’s IT program has prepared graduates to enter the workforce
            immediately after graduation. Students gain hands-on experience in system
            development, networking, and emerging technologies.
            </p>
        </div>

        <div class="section">
            <h2>5-Year BS → MS Track</h2>
            <p>
            Complete your Bachelor’s and Master’s degrees in only five years.
            </p>
        </div>

        <div class="section">
            <h2>Why Choose WSSU IT?</h2>
            <ul>
                <li>Hands-on internships & job shadowing</li>
                <li>Study abroad opportunities</li>
                <li>20:1 student-to-faculty ratio</li>
                <li>Access to The Ideas Lab @ The College</li>
            </ul>
        </div>
        """
    )


@app.route("/program/ms")
def ms():
    return program_page(
        "Master of Science in Computer Science & Information Technology",
        """
        <strong>Phone:</strong> 336-750-2485 <br>
        <strong>Email:</strong> jonese@wssu.edu
        """,
        """
        <div class="section">
            <h2>Program Overview</h2>
            <p>
            Advance your career in gaming, cybersecurity, virtual reality,
            health research, and more. 98% of graduates secure employment
            or enter doctoral programs within six months.
            </p>
        </div>

        <div class="section">
            <h2>Program Options</h2>
            <ul>
                <li>5-Year BS–MS Track</li>
                <li>Certificate in Data Analytics</li>
            </ul>
        </div>

        <div class="section">
            <h2>Student Experience</h2>
            <ul>
                <li>Industry internships</li>
                <li>ACM student organization</li>
                <li>Faculty mentorship</li>
            </ul>
        </div>
        """
    )


@app.route("/program/minorcs")
def program_minor_cs():
    return program_page(
        "Computer Science Minor",
        """
        <strong>Department:</strong> Computer Science <br>
        <strong>Phone:</strong> 336-750-2480 <br>
        <strong>Email:</strong> jonese@wssu.edu
        """,
        """
        <div class="section">
            <h2>Program Overview</h2>
            <p>
            This minor provides students from other majors with programming
            and computational thinking skills.
            </p>
        </div>

        <div class="section">
            <h2>Core Courses</h2>
            <ul>
                <li>Intro to Programming</li>
                <li>Data Structures</li>
                <li>Algorithms</li>
            </ul>
        </div>
        """
    )


@app.route("/program/datascience")
def program_ds_minor():
    return red_style("""
    <h2>Data Science Minor</h2>
    <div class="program-container">
        <h1>Data Science Minor</h1>

        <section>
            <h2>Program Overview</h2>
            <p>
            18 credit hours combining Data Science, Statistics,
            and interdisciplinary applications.
            </p>
        </section>

        <section>
            <h2>Foundation Courses</h2>
            <ul>
                <li>CSC 1315 – Intro to Data Science</li>
                <li>CSC 2315 – Applied Data Science</li>
                <li>One Approved Statistics Course</li>
            </ul>
        </section>

        <section>
            <h2>Advanced Course Options</h2>
            <p>Includes AI, Big Data, Database Systems, GIS, Bioinformatics, and more.</p>
        </section>
    </div>
    """)


@app.route("/program/programmingcert")
def program_programming_cert():
    return program_page(
        "Certificate in Computer Programming",
        """
        <strong>Department:</strong> Computer Science <br>
        <strong>Phone:</strong> 336-750-2480 <br>
        <strong>Email:</strong> jonese@wssu.edu
        """,
        """
        <div class="section">
            <h2>Program Overview</h2>
            <p>
            Designed for career changers with a BS or BA degree.
            Flexible scheduling and web-assisted instruction available.
            </p>
        </div>

        <div class="section">
            <h2>Required Courses</h2>
            <ul>
                <li>CST 5310 – Fundamentals of Programming</li>
                <li>CST 5311 – Intermediate Programming</li>
                <li>CST 5312 – Internet Systems</li>
                <li>CST 5313 – Applied Data Structures</li>
                <li>CST 5314 – Web Programming</li>
                <li>CST 5315 – Database Management</li>
            </ul>
        </div>
        """
    )
@app.route("/program/datacert")
def program_data_cert():
    return program_page(
        "Certificate in Data Analytics",
        """
        <strong>Department:</strong> Computer Science <br>
        <strong>Phone:</strong> 336-750-2480 <br>
        <strong>Email:</strong> jonese@wssu.edu
        """,
        """
        <div class="section">
            <h2>Program Overview</h2>
            <p>
            12-credit online program designed for professionals
            in health care, business, education, and technology.
            </p>
        </div>

        <div class="section">
            <h2>Required Courses</h2>
            <ul>
                <li>CST 5316 – Foundations of Data Analytics</li>
                <li>CST 6307 – Data Mining</li>
                <li>CST 6314 – Big Data Analytics</li>
                <li>CST 6320 – Data Visualization</li>
            </ul>
        </div>
        """
    )
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
