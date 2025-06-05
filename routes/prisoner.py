from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required, current_user
from models import Prisoner, db
from utils import generate_prisoner_id
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

prisoner_bp = Blueprint('prisoner', __name__)

@prisoner_bp.route('/')
@login_required
def index():
    return redirect(url_for('prisoner.inmates'))

@prisoner_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        crime = request.form.get('crime')
        block = request.form.get('block')
        pid = generate_prisoner_id()
        prisoner = Prisoner(prisoner_id=pid, name=name, crime=crime, block=block)
        db.session.add(prisoner)
        db.session.commit()
        flash(f'Prisoner {name} registered with ID {pid}')
        return redirect(url_for('prisoner.inmates', highlight=pid))
    return render_template('register.html')

@prisoner_bp.route('/inmates')
@login_required
def inmates():
    highlight = request.args.get('highlight')
    inmates_list = Prisoner.query.filter_by(status='在押').all()
    return render_template('inmates.html', inmates=inmates_list, highlight=highlight)

@prisoner_bp.route('/release/<int:prisoner_db_id>', methods=['GET', 'POST'])
@login_required
def release(prisoner_db_id):
    prisoner = Prisoner.query.get_or_404(prisoner_db_id)
    if request.method == 'POST':
        rtype = request.form.get('type')
        prisoner.status = '已释放'
        prisoner.release_type = rtype
        prisoner.date_out = datetime.utcnow()
        db.session.commit()
        # Generate certificate
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.drawString(100, 750, 'Release Certificate')
        p.drawString(100, 720, f'Prisoner ID: {prisoner.prisoner_id}')
        p.drawString(100, 700, f'Name: {prisoner.name}')
        p.drawString(100, 680, f'Release Type: {prisoner.release_type}')
        p.drawString(100, 660, f'Date of Release: {prisoner.date_out.strftime("%Y-%m-%d")}')
        p.showPage()
        p.save()
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=f'{prisoner.prisoner_id}_certificate.pdf', mimetype='application/pdf')
    return render_template('release.html', prisoner=prisoner)