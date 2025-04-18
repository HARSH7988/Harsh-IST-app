from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for,flash
from .models import *
from flask import current_app as app
import matplotlib.pyplot as plt


# Auth Routes
@app.route("/")
def home():
    return render_template("wholeapp.html")


@app.route("/login", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        uname = request.form.get("user_name")
        pwd = request.form.get("password")  
        usr = User_Info.query.filter_by(email=uname, password=pwd).first()
        if usr:
            session["user_id"] = usr.id
            session["full_name"] = usr.full_name
            if usr and usr.role == 0:
                return redirect(url_for("admin_dashboard"))
            elif usr and usr.role == 1:
                return redirect(url_for("user_dashboard"))
        else:
            return render_template("login.html", msg="❌🔑 Invalid User Credential! Please try again. 🚫")
                          
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        uname = request.form.get("user_name")
        pwd = request.form.get("password")  
        full_name = request.form.get("full_name")
        dob_str = request.form.get("dob")  
        qualification = request.form.get("qualification")

        dob_obj = None  
        if dob_str:
            try:
                dob_obj = datetime.strptime(dob_str, "%Y-%m-%d").date()
            except ValueError:
                return "Invalid date format. Use YYYY-MM-DD." 
  
        existing_user = User_Info.query.filter_by(email=uname).first()
        if existing_user:
            return render_template("signup.html", msg="Email already registered⚠️📧")    
        
        new_usr = User_Info(email=uname, password=pwd, full_name=full_name, dob=dob_obj, qualification=qualification)
        db.session.add(new_usr)
        db.session.commit()
        return render_template("signup.html", msg="Registration successfully!, Login Now 🎊✨")

    return render_template("signup.html", msg="")

#subject routes
@app.route("/admin")
def admin_dashboard():
    subjects = Subject.query.all()
    return render_template("admin_dashboard.html", subjects=subjects)


@app.route("/user")
def user_dashboard():
    # Fetch all subjects along with their chapters and quizzes
    subjects = Subject.query.all()
    current_date = datetime.now().date()  # Get today's date for filtering quizzes
    return render_template("user_dashboard.html", subjects=subjects, current_date=current_date)



@app.route("/subject", methods=["GET", "POST"])
def add_subject():
    if request.method == "POST":
        sname = request.form.get("name")
        description = request.form.get("description")
        
        new_subject = Subject(name=sname, description=description)
        db.session.add(new_subject)
        db.session.commit()
        
        return redirect(url_for("admin_dashboard"))
    
    return render_template("add_subject.html")

@app.route("/edit_subject/<id>", methods=["GET", "POST"])
def edit_subject(id):
    subject = Subject.query.filter_by(id=id).first()
    if request.method == "POST":
        subject.name = request.form.get("name")
        subject.description = request.form.get("description")
        db.session.commit()
        return redirect(url_for("admin_dashboard"))
    return render_template("edit_subject.html", subject=subject)

@app.route("/delete_subject/<id>")
def delete_subject(id):
    subject = Subject.query.filter_by(id=id).first()
    db.session.delete(subject)
    db.session.commit()
    return redirect(url_for("admin_dashboard"))

# Add Chapter Route
@app.route("/chapters/<int:subject_id>", methods=["GET"])
def chapter_dashboard(subject_id):
    # Fetch all chapters for the given subject
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    # Fetch subject details for context
    subject = Subject.query.filter_by(id=subject_id).first()

    return render_template("chapter_dashboard.html", chapters=chapters, subject=subject)

@app.route("/chapteers/<int:subject_id>", methods=["GET"])
def chapter_dashboard1(subject_id):
    # Fetch all chapters for the given subject
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    # Fetch subject details for context
    subject = Subject.query.filter_by(id=subject_id).first()

    return render_template("chapter_dashboard1.html", chapters=chapters, subject=subject)


@app.route("/chapter/<int:subject_id>", methods=["GET", "POST"])
def add_chapter(subject_id):
    if request.method == "POST":
        cname = request.form.get("name")
        description = request.form.get("description")
        
        new_chapter = Chapter(name=cname, description=description, subject_id=subject_id)
        db.session.add(new_chapter)
        db.session.commit()
        
        return redirect(url_for("chapter_dashboard", subject_id=subject_id))
    
    # Fetch subject details to show in the form
    subject = Subject.query.filter_by(id=subject_id).first()
    return render_template("add_chapter.html", subject=subject)


@app.route("/edit_chapter/<id>", methods=["GET", "POST"])
def edit_chapter(id):
    chapter = Chapter.query.filter_by(id=id).first()
    if request.method == "POST":
        chapter.name = request.form.get("name")
        chapter.description = request.form.get("description")
        db.session.commit()
        return redirect(url_for("chapter_dashboard", subject_id=chapter.subject_id))
    return render_template("edit_chapter.html", chapter=chapter)

@app.route("/delete_chapter/<id>")
def delete_chapter(id):
    chapter = Chapter.query.filter_by(id=id).first()
    db.session.delete(chapter)
    db.session.commit()
    return redirect(url_for("chapter_dashboard", subject_id=chapter.subject_id))


# Add Quiz Route
@app.route("/quizzes/<int:chapter_id>", methods=["GET"])
def quiz_dashboard(chapter_id):
    # Fetch all quizzes for the given chapter
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    # Fetch chapter details for context
    chapter = Chapter.query.filter_by(id=chapter_id).first()

    return render_template("quiz_dashboard.html", quizzes=quizzes, chapter=chapter)

@app.route("/quizzees/<int:chapter_id>", methods=["GET"])
def quiz_dashboard1(chapter_id):
    # Fetch all quizzes for the given chapter
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    # Fetch chapter details for context
    chapter = Chapter.query.filter_by(id=chapter_id).first()

    return render_template("quiz_dashboard1.html", quizzes=quizzes, chapter=chapter)

@app.route("/quiz/<int:chapter_id>", methods=["GET", "POST"])
def add_quiz(chapter_id):
    if request.method == "POST":
        name = request.form.get("name")
        date_of_quiz = datetime.strptime(request.form.get("date_of_quiz"), "%Y-%m-%d")
        time_duration = int(request.form.get("time_duration"))
        
        new_quiz = Quiz(name=name,date_of_quiz=date_of_quiz, time_duration=time_duration, chapter_id=chapter_id)
        db.session.add(new_quiz)
        db.session.commit()
        
        return redirect(url_for("quiz_dashboard",chapter_id=chapter_id))
    
    chapter = Chapter.query.filter_by(id=chapter_id).first()
    return render_template("add_quiz.html", chapter=chapter)

@app.route("/edit_quiz/<id>", methods=["GET", "POST"])
def edit_quiz(id):
    quiz = Quiz.query.filter_by(id=id).first()
    if request.method == "POST":
        quiz.name = request.form.get("name")
        quiz.date_of_quiz = datetime.strptime(request.form.get("date_of_quiz"), "%Y-%m-%d")
        quiz.time_duration = int(request.form.get("time_duration"))
        db.session.commit()
        return redirect(url_for("quiz_dashboard", chapter_id=quiz.chapter_id))
    return render_template("edit_quiz.html", quiz=quiz)


@app.route("/delete_quiz/<id>")
def delete_quiz(id):
    quiz = Quiz.query.filter_by(id=id).first()
    db.session.delete(quiz)
    db.session.commit()
    return redirect(url_for("quiz_dashboard", chapter_id=quiz.chapter_id))


# Add Question Route
@app.route("/questions/<int:quiz_id>", methods=["GET"])
def question_dashboard(quiz_id):
    # Fetch all questions for the given quiz
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    # Fetch quiz details for context
    quiz = Quiz.query.filter_by(id=quiz_id).first()

    return render_template("question_dashboard.html", questions=questions, quiz=quiz)



@app.route("/question/<quiz_id>", methods=["GET", "POST"])
def add_question(quiz_id):
    if request.method == "POST":
        q_statement = request.form.get("question_statement")
        option1 = request.form.get("option1")
        option2 = request.form.get("option2")
        option3 = request.form.get("option3")
        option4 = request.form.get("option4")
        correct_option = request.form.get("correct_option")

        new_question = Question(
            question_statement=q_statement,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_option=correct_option,
            quiz_id=quiz_id
        )
        
        db.session.add(new_question)
        db.session.commit()
        
        return redirect(url_for("question_dashboard",quiz_id=quiz_id))
    
    quiz = Quiz.query.filter_by(id=quiz_id).first()
    return render_template("add_question.html", quiz=quiz)

@app.route("/edit_question/<id>", methods=["GET", "POST"])
def edit_question(id):
    # Step 1: Fetch the question and its associated quiz
    question = Question.query.get_or_404(id)  # Auto-404 if question not found
    quiz = Quiz.query.get_or_404(question.quiz_id)  # Fetch quiz using question's quiz_id

    if request.method == "POST":
        # Step 2: Update question data from form
        question.question_statement = request.form.get("question_statement")
        question.option1 = request.form.get("option1")
        question.option2 = request.form.get("option2")
        question.option3 = request.form.get("option3")
        question.option4 = request.form.get("option4")
        question.correct_option = request.form.get("correct_option")

        # Step 3: Commit to database
        db.session.commit()
        flash("Question updated successfully!")
        
        # Step 4: Redirect to question dashboard
        return redirect(url_for("question_dashboard", quiz_id=quiz.id))

    # Step 5: Pass BOTH question and quiz to the template
    return render_template("edit_question.html", question=question, quiz=quiz)


@app.route("/delete_question/<id>")
def delete_question(id):
    question = Question.query.filter_by(id=id).first()
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for("question_dashboard", quiz_id=question.quiz_id))


@app.route("/manage_users", methods=["GET", "POST"])
def manage_users():
    if request.method == "POST":
        # Fetch user ID from the form
        user_id = request.form.get("user_id")
        user = User_Info.query.filter_by(id=user_id).first()

        # Delete the user if found
        if user:
            db.session.delete(user)
            db.session.commit()
        
        # Redirect back to the same page after deletion
        return redirect(url_for("manage_users"))
    
    # Fetch all users with role=1 for GET request
    users = User_Info.query.filter_by(role=1).all()
    return render_template("manage_users.html", users=users)

@app.route("/admin_profile", methods=["GET"])
def admin_profile():
    # Fetch all admins (users with role=0)
    admins = User_Info.query.filter_by(role=0).all()
    return render_template("admin_profile.html", admins=admins)

@app.route("/user_profile", methods=["GET"])
def user_profile():
    # Fetch all admins (users with role=0)
    admins = User_Info.query.filter_by(role=1).all()
    return render_template("user_profile.html", admins=admins)

@app.route("/admin_summary")
def admin_summary():
 
    return render_template("admin_summary.html")

@app.route("/questionss/<int:quiz_id>", methods=["GET"])
def question_dashboard1(quiz_id):
    # Fetch all questions for the given quiz
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    # Fetch quiz details for context
    quiz = Quiz.query.filter_by(id=quiz_id).first()

    return render_template("question_dashboard1.html", questions=questions, quiz=quiz)

@app.route("/usser", methods=["GET", "POST"])
def usser():
 
    return render_template("user_dashboard1.html")

@app.route("/summary")
def summary():
    if "user_id" not in session:
        return redirect(url_for("signin"))
    user_id = session["user_id"]
    scores = Score.query.filter_by(user_id=user_id).all()
    return render_template("summary.html", scores=scores)

@app.route("/edit_admin/<int:id>", methods=["GET", "POST"])
def edit_admin(id):
    # Fetch the admin by ID
    admin = User_Info.query.get(id)
    if request.method == "POST":
        # Get form data
        email = request.form.get("email")
        password = request.form.get("password")
        full_name = request.form.get("name")
        dob_str = request.form.get("dob")
        qualification = request.form.get("qualification")

        # Date parsing logic
        dob_obj = None
        if dob_str:
            try:
                dob_obj = datetime.strptime(dob_str, "%Y-%m-%d").date()
            except ValueError:
                return "Invalid date format. Use YYYY-MM-DD."


        # Update admin details
        admin.email = email
        admin.password = password  # Should hash password in production
        admin.full_name = full_name
        admin.dob = dob_obj
        admin.qualification = qualification

        db.session.commit()
        return redirect(url_for("admin_profile"))
    
    return render_template("edit_admin.html", admin=admin)


@app.route('/search')
def search():
    query = request.args.get('query', '').strip().lower()

    if not query:
        return render_template("search_results.html", subjects=[], chapters=[], quizzes=[], query=query)

    subjects = Subject.query.filter(Subject.name.ilike(f"%{query}%")).all()
    chapters = Chapter.query.filter(Chapter.name.ilike(f"%{query}%")).all()
    quizzes = Quiz.query.filter(Quiz.name.ilike(f"%{query}%")).all()

    return render_template("search_results.html", subjects=subjects, chapters=chapters, quizzes=quizzes, query=query)

@app.route('/admsearch')
def admsearch():
    query = request.args.get('query', '').strip().lower()

    if not query:
        return render_template("admsearch_results.html", subjects=[], chapters=[], quizzes=[], query=query)

    subjects = Subject.query.filter(Subject.name.ilike(f"%{query}%")).all()
    chapters = Chapter.query.filter(Chapter.name.ilike(f"%{query}%")).all()
    quizzes = Quiz.query.filter(Quiz.name.ilike(f"%{query}%")).all()

    return render_template("admsearch_results.html", subjects=subjects, chapters=chapters, quizzes=quizzes, query=query)


@app.route("/user/subjects", methods=["GET"])
def user_view_subjects():
    # Fetch all subjects for the user
    subjects = Subject.query.all()
    return render_template("user_subjects.html", subjects=subjects)

@app.route("/user/chapters/<int:subject_id>", methods=["GET"])
def user_view_chapters(subject_id):
    # Fetch all chapters for the given subject
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    subject = Subject.query.get_or_404(subject_id)
    return render_template("user_chapters.html", chapters=chapters, subject=subject)

@app.route("/user/quizzes/<int:chapter_id>", methods=["GET"])
def user_view_quizzes(chapter_id):
    # Fetch all quizzes for the given chapter
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).filter(Quiz.date_of_quiz <= date.today()).all()
    chapter = Chapter.query.get_or_404(chapter_id)
    return render_template("user_quizzes.html", quizzes=quizzes, chapter=chapter)
 
@app.route("/submit_quiz/<int:quiz_id>", methods=["POST"])
def submit_quiz(quiz_id):
    if "user_id" not in session:
        return redirect(url_for("signin"))

    user_id = session["user_id"]
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = quiz.questions

    score = 0
    total = len(questions)

    for question in questions:
        selected = request.form.get(f"q{question.id}")
        if selected and selected == question.correct_option:
            score += 1

    # Save Score
    new_score = Score(
        total_scored=score,
        quiz_id=quiz_id,
        user_id=user_id,
    )
    db.session.add(new_score)
    db.session.commit()

    return render_template("result.html", score=score, total=total)

@app.route("/admin_summmary")
def admin_summmary():
    plot=()
    plot.savefig("./static/images/subject_summary.jpeg")
    plot.clf()
    return render_template("admin_summary.html")

@app.route("/user_summmary")
def user_summmary():
    plot=()
    plot.savefig("./static/images/subject_summary.jpeg")
    plot.clf()
    return render_template("quiz_summary.html")

