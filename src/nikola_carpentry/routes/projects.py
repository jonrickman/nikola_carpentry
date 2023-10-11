from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user
from nikola_carpentry import app, ProjectForm, db
from nikola_carpentry.models import Project, ProjectFile
from werkzeug.utils import secure_filename


@app.route("/projects", methods=["GET", "POST"])
def projects():
    ready_projects = Project.query.filter().all()
    project_files = ProjectFile.query.filter().all()

    form = ProjectForm()

    if form.validate_on_submit():
        # create the project item
        title = form.title.data
        content = form.content.data
        project = Project(title, content)

        new_project_files = []
        # iterate the files from the form
        for f in form.files.data:
            # if no files in form data will still return []
            if not f:
                continue

            # get the basename and create the project file
            basename = secure_filename(f.filename)
            project_file = ProjectFile(basename)

            # get the fully qualified file path
            file_root = app.config["ROOT"]
            upload_folder = app.config["UPLOAD_FOLDER"]
            filepath = file_root / upload_folder / basename

            # save the file
            f.save(filepath)
            # append file to new project files
            new_project_files.append(project_file)

        # add project files
        # TODO: get selected images, currently only getting new images
        project.files = new_project_files

        # store the project and files
        db.session.add(project)
        [db.session.add(p) for p in new_project_files]

        # Commit the changes
        db.session.commit()

        flash("Project created successfully")
        next_page = request.args.get("next")
        return redirect(next_page) if next_page else redirect(url_for("projects"))

    return render_template(
        "projects.html",
        user=current_user,
        project_files=project_files,
        ready_projects=ready_projects,
        form=form,
    )


@app.route("/projects/<int:project_id>/")
def get_project(project_id: int):
    project = Project.query.filter_by(id=project_id).first()
    form = ProjectForm()

    return render_template(
        "project.html", user=current_user, form=form, project=project
    )


@app.route("/projects/approve/<int:project_id>/")
def approve_project(project_id: int):
    # Project.query.filter_by(id=project_id).update({"approved": True})

    # if current_user.is_authenticated:
    #     db.session.commit()
    #     return redirect(url_for("projects"))

    return "Nope"


@app.route("/projects/delete/<int:project_id>/")
def delete_project(project_id: int):
    # Project.query.filter_by(id=project_id).delete()

    # if current_user.is_authenticated:
    #     db.session.commit()
    #     return redirect(url_for("projects"))

    return "Nope"
