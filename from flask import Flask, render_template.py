import base64
import io
from flask import Flask, render_template, render_template_string, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from email.mime.text import MIMEText
import qrcode
import os 
import random
import smtplib
from email.mime.text import MIMEText
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
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
# ===import random===================
import random
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib.pagesizes import letter

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


# Create database + default teacher
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

        student_id = "WSSU" + str(random.randint(10000,99999))

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

# The URL you want to encode
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

    # Generate QR code
    url = "https://csramsrecruit.onrender.com/"  # or request.url if dynamic
    qr = qrcode.QRCode(box_size=6, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Convert QR code to base64 to embed in HTML
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    qr_b64 = base64.b64encode(buf.getvalue()).decode("ascii")

    return f"""
    <html>
    <body style="font-family:Arial;text-align:center;">
        <h1>CS Open House Platform is running!</h1>
        <p>Scan the QR code to register</p>
        <img src="data:image/png;base64,{qr_b64}">
        <br><br>
        <a href="/Programs">Enter Program Page</a>
    </body>
    </html>
    """
# ======================
# HOME PAGE (KEEP YOUR RED DESIGN)
# ======================

@app.route("/Programs")
def Program():
    return render_template_string("""
    <html>
    <head>
        <title>CS & IT Program</title>
        <style>
            body {
                margin: 0;
                font-family: Arial, sans-serif;
background: linear-gradient(
    rgba(139,0,0,0.85),
    rgba(139,0,0,0.85)
), url('/static/campus.jpg');

background-size: cover;
background-position: center;
background-attachment: fixed;                color: white;
                text-align: center;
            }
            .container {
                padding: 60px 20px;
                max-width: 1100px;
                margin: auto;
            }
            h1 { font-size: 3em; }
            p { font-size: 1.1em; line-height: 1.6; }

            .btn {
                display: inline-block;
                padding: 12px 25px;
                margin: 10px;
                background: white;
                color: #8B0000;
                text-decoration: none;
                border-radius: 25px;
                font-weight: bold;
            }

            .btn:hover { background: #ffe6e6; }

            .card {
                background: rgba(255,255,255,0.15);
                padding: 20px;
                border-radius: 15px;
                margin: 10px;
                display: inline-block;
                width: 260px;
            }

            .section {
                margin-top: 40px;
            }

            ul {
                text-align: left;
                display: inline-block;
            }
        </style>
    </head>

    <body>
        <div class="container">

            <h1>Master of Science in Computer Science & IT</h1> 
            <p><b>Winston-Salem State University</b></p>
            <p>📞 336-750-2485 | ✉️ jonese@wssu.edu</p>

            <p>🚀 98% Employment Rate | 💻 Hands-On Learning | 🔐 Cybersecurity</p>

            <a href="/register" class="btn">Apply</a>
            <a href="/student_login" class="btn">Student Login</a>
            <a href="/login" class="btn">Teacher Login</a>

            <div class="section">
                <div class="card">💡 Innovative Learning</div>
                <div class="card">🔐 Cybersecurity Focus</div>
                <div class="card">🌐 Career Ready</div>
            </div>

            <div class="section">
                <div class="section">
    <h2>Programs of Study</h2>
    <p>
        The Department of Computer Science offers graduate and undergraduate degree programs, 
        as well as certificate programs. Our programs integrate extensive laboratory study, 
        student organizations, seminars, and research experiences. Faculty collaborate with IT 
        professionals in business and government to keep programs current with industry trends.
    </p>

    <div class="program-list">

    <a href="/program/cs" class="program-card">
        <h3>Bachelor of Science in Computer Science</h3>
        <p>Advanced programming, cybersecurity, AI, and high-performance computing.</p>
        <span class="view-link">View Program →</span>
    </a>

    <a href="/program/it" class="program-card">
        <h3>Bachelor of Science in Information Technology</h3>
        <p>Hands-on IT training with networking, systems, and internships.</p>
        <span class="view-link">View Program →</span>
    </a>

    <a href="/program/ms" class="program-card">
        <h3>MS in Computer Science & Information Technology</h3>
        <p>Graduate-level specialization in cybersecurity, AI, and data science.</p>
        <span class="view-link">View Program →</span>
    </a>

    <a href="/program/minorcs" class="program-card">
        <h3>Computer Science Minor</h3>
        <p>Enhance your major with strong programming and database skills.</p>
        <span class="view-link">View Program →</span>
    </a>

    <a href="/program/datascience" class="program-card">
        <h3>Data Science Minor</h3>
        <p>Data analytics, AI foundations, and interdisciplinary applications.</p>
        <span class="view-link">View Program →</span>
    </a>

    <a href="/program/programmingcert" class="program-card">
        <h3>Certificate in Computer Programming</h3>
        <p>Perfect for career changers seeking technical programming skills.</p>
        <span class="view-link">View Program →</span>
    </a>

    <a href="/program/datacert" class="program-card">
        <h3>Certificate in Data Analytics</h3>
        <p>Professional online certificate in data mining and visualization.</p>
        <span class="view-link">View Program →</span>
    </a>

</div>

<!-- CSS -->
<style>
.program-list {
    max-width: 1000px;
    margin: 40px auto;
}

.program-card {
    display: block;
    background: rgba(255,255,255,0.08);
    padding: 25px;
    margin-bottom: 15px;
    border-radius: 15px;
    text-decoration: none;
    color: white;
    transition: all 0.3s ease;
    border: 1px solid rgba(255,255,255,0.1);
}

.program-card h3 {
    margin: 0 0 10px 0;
    color: #ff4d4d;
}

.program-card p {
    margin: 0 0 15px 0;
    color: #ccc;
}

.program-card .view-link {
    font-size: 0.9em;
    font-weight: bold;
    color: #ff4d4d;
}

.program-card:hover {
    background: rgba(255,255,255,0.15);
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.4);
}
</style>
<!-- JavaScript -->
<script>
const accordions = document.querySelectorAll('.accordion-btn');
accordions.forEach(btn => {
    btn.addEventListener('click', () => {
        const content = btn.nextElementSibling;
        content.style.display = content.style.display === 'block' ? 'none' : 'block';
    });
});
</script>

            <div class="section">
                <h2>Program Options</h2>
                <div class="card">
                    <h3>5-Year B.S. → M.S.</h3>
                    <p>Earn both degrees faster and save time and money.</p>
                </div>
                <div class="card">
                    <h3>Data Analytics Certificate</h3>
                    <p>Great for any major entering tech.</p>
                </div>
            </div>

            <div class="section">
                <h2>Why Choose WSSU?</h2>
                <div class="card">#1 HBCU in NC</div>
                <div class="card">#1 for Social Mobility</div>
                <div class="card">Hands-on Internships</div>
                <div class="card">Faculty Mentorship</div>
            </div>

            <div class="section">
                <h2>Career Opportunities</h2>
                <ul>
                    <li>Software Developer</li>
                    <li>Cybersecurity Manager</li>
                    <li>Data Scientist</li>
                    <li>Network Architect</li>
                    <li>Database Administrator</li>
                    <li>Game Designer</li>
                </ul>
            </div>

            <div class="section">
                <h2>Info Session</h2>
                <p><b>April 1 @ 6:30 PM</b></p>
                <a href="/register" class="btn">Register Now</a>
            </div>

        </div>
    </body>
    </html>
    """)

# ======================
# RED STYLE TEMPLATE FOR OTHER PAGES
# ======================

def red_style(content):
    return f"""
    <html>
    <head>
    <style>
        body {{
            font-family: Arial;
            background: #fff5f5;
            color: #8B0000;
            text-align: center;
        }}

        input, select {{
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
        }}

        table {{
            margin: auto;
            border-collapse: collapse;
        }}

        th, td {{
            border: 1px solid #8B0000;
            padding: 10px;
        }}
    </style>
    </head>
    <body>
    {content}
    </body>
    </html>
    """
# ======================
# STUDENT REGISTER
# ======================



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

        student_id = "WSSU" + str(random.randint(10000,99999))

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

    # ✅ THIS PART WAS MISSING
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
# ======================
# STUDENT LOGIN
# ======================

@app.route("/student_login", methods=["GET","POST"])
def student_login():

    if request.method == "POST":
        student = Student.query.filter_by(email=request.form["email"]).first()

        if student and check_password_hash(student.password, request.form["password"]):
            session["student"] = student.id
            return redirect("/student_dashboard")

    return red_style("""
    <h2>Student Login</h2>

    <form method="POST">
    <input name="email" placeholder="Email"><br>
    <input type="password" name="password" placeholder="Password"><br>
    <button>Login</button>
    </form>
    """)

# ======================
# STUDENT DASHBOARD
# ======================

@app.route("/student_dashboard")
def student_dashboard():

    if "student" not in session:
        return redirect("/student_login")

    student = Student.query.get(session["student"])

    course_map = {
        "Computer Science": ["Algorithms", "Operating Systems", "Artificial Intelligence"],
        "Information Technology": ["Networking", "Cloud Computing", "System Administration"],
        "Data Science": ["Machine Learning", "Data Mining", "Data Visualization"],
        "Cybersecurity": ["Ethical Hacking", "Network Security", "Digital Forensics"]
    }

    recommended = course_map.get(student.interest, [])

    course_html = "".join([f"<li>{c}</li>" for c in recommended])

    return red_style(f"""
    <h2>Welcome {student.first_name}</h2>

    <p><b>Email:</b> {student.email}</p>
    <p><b>Interest:</b> {student.interest}</p>
    <p><b>Location:</b> {student.location}</p>

    <h3>Recommended Courses For You</h3>
    <ul>
    {course_html}
    </ul>

    <a href="/logout_student">Logout</a>
    """)

@app.route("/logout_student")
def logout_student():
    session.pop("student", None)
    return redirect("/")

# ======================
# TEACHER LOGIN
# ======================

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":
        user = Teacher.query.filter_by(username=request.form["username"]).first()

        if user and check_password_hash(user.password, request.form["password"]):
            session["user"] = user.username
            return redirect("/teacher")

    return red_style("""
    <h2>Teacher Login</h2>

    <form method="POST">
    <input name="username" placeholder="Username"><br>
    <input type="password" name="password" placeholder="Password"><br>
    <button>Login</button>
    </form>
    """)

# ======================
# TEACHER DASHBOARD (UPGRADED)
# ======================

@app.route("/teacher")
def teacher():

    if "user" not in session:
        return redirect("/login")

    students = Student.query.all()

    rows = ""
    for s in students:
        rows += f"""
        <tr>
            <td>{s.first_name} {s.last_name}</td>
            <td>{s.email}</td>
            <td>{s.parent_email}</td>
            <td>{s.interest}</td>
            <td>{s.location}</td>
            <td>
                <a href='/contact/{s.id}/student'>Email Student</a> |
                <a href='/contact/{s.id}/parent'>Email Parent</a> |
                <a href='/delete/{s.id}'>Delete</a>
            </td>
        </tr>
        """

    return red_style(f"""
    <h2>Teacher Dashboard</h2>

    <table>
    <tr>
        <th>Name</th>
        <th>Student Email</th>
        <th>Parent Email</th>
        <th>Interest</th>
        <th>Location</th>
        <th>Actions</th>
    </tr>
    {rows}
    </table>

    <br>
    <a href="/logout">Logout</a>
    """)
# ======================
# DELETE STUDENT
# ======================

@app.route("/contact/<int:id>/<type>", methods=["GET","POST"])
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
# ======================
# PROGRAM DETAIL PAGES
# ======================

@app.route("/program/cs")
def cs():
    return render_template_string("""
    <html>
    <head>
        <style>
            body { font-family: Arial; background:#111; color:white; }
            .program-container { max-width:900px; margin:auto; padding:40px; }
            h1 { color:#ff4d4d; }
            h2 { color:#ff4d4d; margin-top:30px; }
            .contact { background:rgba(255,255,255,0.1); padding:15px; border-radius:10px; }
            ul { padding-left:20px; }
        </style>
    </head>
    <body>
        <div class="program-container">
            <h1>Bachelor of Science in Computer Science</h1>

            <div class="program-container">

    <h1>Bachelor of Science in Computer Science</h1>
    <p class="contact">
        <strong>Department:</strong> Computer Science <br>
        <strong>Phone:</strong> 336-750-2480 <br>
        <strong>Email:</strong> jonese@wssu.edu
    </p>

    <section>
        <h2>Program Overview</h2>
        <p>
        Computer science touches every part of modern society. Since 1981, 
        WSSU has delivered a cutting-edge curriculum that adapts to the ever-changing tech industry. 
        Almost all alumni are employed within six months of graduation.
        </p>
    </section>

    <section>
        <h2>5-Year BS → MS Option</h2>
        <p>
        Add one year to your bachelor's degree and earn your Master’s degree early 
        through our 5-Year (4+1) BS–MS track.
        </p>
    </section>

    <section>
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
    </section>

</div>

            <h2>Program Overview</h2>
            <p>
            Since 1981, WSSU has delivered a cutting-edge computer science curriculum.
            Alumni are employed within six months of graduation.
            </p>

            <h2>5-Year BS → MS Option</h2>
            <p>
            Add one year and earn your Master's degree early with our 4+1 track.
            </p>

            <h2>Concentrations</h2>
            <ul>
                <li>Computer Graphics</li>
                <li>Database Administration</li>
                <li>Information Security</li>
                <li>Networking</li>
                <li>High Performance Computing</li>
                <li>Computational Science</li>
            </ul>
        </div>
    </body>
    </html>
    """)

@app.route("/program/it")
def it():
    return render_template_string("""
    <html>
    <head>
        <style>
            body { font-family: Arial; background:#111; color:white; }
            .program-container { max-width:900px; margin:auto; padding:40px; }
            h1 { color:#ff4d4d; }
            h2 { color:#ff4d4d; margin-top:30px; }
            .contact { background:rgba(255,255,255,0.1); padding:15px; border-radius:10px; }
        </style>
    </head>
    <body>
        <div class="program-container">
            <h1>Bachelor of Science in Information Technology</h1>

            <div class="contact">
                <strong>Phone:</strong> 336-750-2480 <br>
                <strong>Email:</strong> jonese@wssu.edu
           <div class="program-container">

    <h1>Bachelor of Science in Information Technology</h1>
    <p class="contact">
        <strong>Department:</strong> Information Technology <br>
        <strong>Phone:</strong> 336-750-2480 <br>
        <strong>Email:</strong> jonese@wssu.edu
    </p>

    <section>
        <h2>Program Overview</h2>
        <p>
        Since 2007, WSSU’s IT program has prepared graduates to enter the workforce 
        immediately after graduation. Students gain hands-on experience in system 
        development, networking, and emerging technologies.
        </p>
    </section>

    <section>
        <h2>5-Year BS → MS Track</h2>
        <p>
        Complete your Bachelor’s and Master’s degrees in only five years.
        </p>
    </section>

    <section>
        <h2>Why Choose WSSU IT?</h2>
        <ul>
            <li>Hands-on internships & job shadowing</li>
            <li>Study abroad opportunities</li>
            <li>20:1 student-to-faculty ratio</li>
            <li>Access to The Ideas Lab @ The College</li>
        </ul>
    </section>

</div>
    </body>
    </html>
    """)
@app.route("/program/ms")
def ms():
    return render_template_string("""
    <html>
    <head>
        <style>
            body { font-family: Arial; background:#111; color:white; }
            .program-container { max-width:900px; margin:auto; padding:40px; }
            h1 { color:#ff4d4d; }
            h2 { color:#ff4d4d; margin-top:30px; }
            .contact { background:rgba(255,255,255,0.1); padding:15px; border-radius:10px; }
        </style>
    </head>
    <body>
        <div class="program-container">
            <h1>Master of Science in Computer Science & IT</h1>

            <div class="contact">
                <strong>Phone:</strong> 336-750-2485 <br>
                <strong>Email:</strong> jonese@wssu.edu
            <div class="program-container">

    <h1>Master of Science in Computer Science & Information Technology</h1>
    <p class="contact">
        <strong>Phone:</strong> 336-750-2485 <br>
        <strong>Email:</strong> jonese@wssu.edu
    </p>

    <section>
        <h2>Program Overview</h2>
        <p>
        Advance your career in gaming, cybersecurity, virtual reality, 
        health research, and more. 98% of graduates secure employment 
        or enter doctoral programs within six months.
        </p>
    </section>

    <section>
        <h2>Program Options</h2>
        <ul>
            <li>5-Year BS–MS Track</li>
            <li>Certificate in Data Analytics</li>
        </ul>
    </section>

    <section>
        <h2>Student Experience</h2>
        <ul>
            <li>Industry internships</li>
            <li>ACM student organization</li>
            <li>Faculty mentorship</li>
        </ul>
    </section>

</div>
    </body>
    </html>
    """)



@app.route("/program/mscsit")
def program_ms():
    return red_style("""
    <h2>Master of Science in Computer Science & Information Technology</h2>

    <p>This graduate program provides advanced training in software systems,
    cybersecurity, and data analytics.</p>

    <h3>Focus Areas</h3>
    <ul>
        <li>Cybersecurity</li>
        <li>Artificial Intelligence</li>
        <li>Software Development</li>
        <li>Data Analytics</li>
    </ul>

    <a href="/Programs">Back to Programs</a>
    """)


@app.route("/program/minorcs")
def program_minor_cs():
    return red_style("""
    <h2>Computer Science Minor</h2>

    <p>This minor provides students from other majors with programming
    and computational thinking skills.</p>

    <ul>
        <li>Intro to Programming</li>
        <li>Data Structures</li>
        <li>Algorithms</li>
    </ul>

    <a href="/Programs">Back to Programs</a>
    """)


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
    return red_style("""
    <h2>Certificate in Computer Programming</h2>

    <div class="program-container">

    <h1>Certificate in Computer Programming</h1>

    <section>
        <h2>Program Overview</h2>
        <p>
        Designed for career changers with a BS or BA degree. 
        Flexible scheduling and web-assisted instruction available.
        </p>
    </section>

    <section>
        <h2>Required Courses</h2>
        <ul>
            <li>CST 5310 – Fundamentals of Programming</li>
            <li>CST 5311 – Intermediate Programming</li>
            <li>CST 5312 – Internet Systems</li>
            <li>CST 5313 – Applied Data Structures</li>
            <li>CST 5314 – Web Programming</li>
            <li>CST 5315 – Database Management</li>
        </ul>
    </section>

</div>
    """)


@app.route("/program/datacert")
def program_data_cert():
    return red_style("""
    <h2>Certificate in Data Analytics</h2>

    <div class="program-container">

    <h1>Certificate in Data Analytics</h1>

    <section>
        <h2>Program Overview</h2>
        <p>
        12-credit online program designed for professionals 
        in health care, business, education, and technology.
        </p>
    </section>

    <section>
        <h2>Required Courses</h2>
        <ul>
            <li>CST 5316 – Foundations of Data Analytics</li>
            <li>CST 6307 – Data Mining</li>
            <li>CST 6314 – Big Data Analytics</li>
            <li>CST 6320 – Data Visualization</li>
        </ul>
    </section>

</div>
    <a href="/Programs">Back to Programs</a>
    """)
# ======================
# RUN APP
# ======================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)