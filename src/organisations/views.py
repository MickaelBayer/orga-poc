from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from src import db
from src.accounts.forms import SetAdminForm
from src.accounts.models import User
from src.organisations.forms import CreateForm
from src.organisations.models import Organisation

organisations_bp = Blueprint(
    "organisations", __name__, url_prefix="/organisations")


def is_user_in_orga_or_in_an_ancestor(user, id):
    """
    True if the user is one of the organisations above the one of the given id
    """
    if user.organisation == id:
        return True
    orga = Organisation.query.get(id)
    while orga is not None and orga.parent_orga_id != orga.id:
        if user.organisation == orga.parent_orga_id:
            return True
        orga = Organisation.query.get(orga.parent_orga_id)
    return False


def all_ancestors(user, id):
    """
    All ancestors of organisation id to user's organisation
    """
    user_orga = Organisation.query.get(user.organisation)
    if user.organisation == id:
        return [user_orga]
    ancestors = []
    orga = Organisation.query.get(id)
    while orga is not None and orga.parent_orga_id != orga.id:
        ancestors.append(orga)
        if user.organisation == orga.parent_orga_id:
            ancestors.append(user_orga)
            ancestors.reverse()
            return ancestors
        orga = Organisation.query.get(orga.parent_orga_id)
    ancestors.append(user_orga)
    ancestors.reverse()
    return ancestors


@organisations_bp.route("/<id>", methods=["GET", "POST"])
@login_required
def home(id):
    if request.method == "GET":
        if is_user_in_orga_or_in_an_ancestor(current_user, int(id)):
            ancestors = all_ancestors(current_user, int(id))
            orga = Organisation.query.get(int(id))
            orga_members = User.query.filter_by(
                organisation=int(id)).order_by(User.email)
            orgas = db.session.query(Organisation).filter(
                Organisation.parent_orga_id == orga.id, Organisation.id != 1)
            forms = None
            if current_user.is_admin and (current_user.organisation == int(id) or current_user.organisation == orga.parent_orga_id):
                forms = []
                for member in orga_members:
                    form = SetAdminForm(request.form)
                    form.is_admin.data = member.is_admin
                    form.user_id.data = member.id
                    forms.append(form)
                return render_template("organisations/index.html", organisation=orga, orga_members=orga_members, children=orgas, ancestors=ancestors, forms=forms)
            else:
                return render_template("organisations/index.html", organisation=orga, orga_members=orga_members, children=orgas, ancestors=ancestors, forms=forms)
        else:
            flash("You can not access this.", "danger")
            return redirect(url_for("core.home"))
    elif request.method == "POST":
        if current_user.is_admin:
            if len(request.form) > 0:
                form = SetAdminForm(request.form)
                if form.validate():
                    user = User.query.get(form.user_id.data)
                    user.is_admin = form.is_admin.data
                    db.session.add(user)
                    db.session.commit()
                else:
                    flash("Something went wrong.", "danger")
            return redirect(url_for("organisations.home", id=id))
        else:
            flash("You can not access this.", "danger")
            return redirect(url_for("core.home"))
    else:
        flash("You can not access this.", "danger")
        return redirect(url_for("organisations.home", id=id))


@organisations_bp.route("/<id>/create", methods=["GET", "POST"])
@login_required
def create(id):
    if current_user.is_admin and int(id) == current_user.organisation:
        if request.method == "GET":
            orga = Organisation.query.get(int(id))
            form = CreateForm(request.form)
            return render_template("organisations/create.html", organisation=orga, form=form)
        elif request.method == "POST":
            if len(request.form) > 0:
                form = CreateForm(request.form)
                if form.validate():
                    new_orga = Organisation(
                        name=form.name.data, description=form.description.data, parent_orga_id=int(id))
                    db.session.add(new_orga)
                    db.session.commit()
                    flash("You have created a new sub-organisation.", "success")
                else:
                    flash("Something went wrong.", "danger")
                return redirect(url_for("organisations.home", id=id))
        else:
            flash("You can not access this.", "danger")
            return redirect(url_for("organisations.home", id=id))
    else:
        flash("You can not access this.", "danger")
        return redirect(url_for("organisations.home", id=id))
