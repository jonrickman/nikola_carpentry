from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user
from nikola_carpentry import app, ProjectForm, db
from nikola_carpentry.models import Project, ProjectFile

@app.route("/projects", methods=["GET", "POST"])
def projects():

    ready_projects = Project.query.filter().all()
    project_files = ProjectFile.query.filter().all()
    form = ProjectForm()
    
    if form.validate_on_submit():

        project = Project(title= form.title.data,
                        content=form.content.data)
        
        with app.app_context():
            project.insert()
            db.session.refresh(project)

        basename = form.save_files()

        with app.app_context():
            project_file = ProjectFile(project.id, str(basename))
            project_file.insert()

        flash("Project created successfully")
        next_page = request.args.get("next")
        return redirect(next_page) if next_page else redirect(url_for("projects"))
    
    return render_template("projects.html", 
                           user=current_user, 
                           ready_projects = ready_projects,
                           project_files = project_files,
                           form=form)


@app.route("/projects/<int:project_id>/")
def get_project(project_id: int):
    project = Project.query.filter_by(id=project_id).first()
    form = ProjectForm()
    
    return render_template("project.html", 
                           user=current_user, 
                           form = form,
                           project=project)


@app.route("/projects/approve/<int:project_id>/")
def approve_project(project_id: int):
    Project.query.filter_by(id=project_id).update({"approved": True})

    if current_user.is_authenticated:
        db.session.commit()
        return redirect(url_for("projects"))
    
    return "Nope"

@app.route("/projects/delete/<int:project_id>/")
def delete_project(project_id: int):
    Project.query.filter_by(id=project_id).delete()

    if current_user.is_authenticated:
        db.session.commit()
        return redirect(url_for("projects"))
    
    return "Nope"
    
