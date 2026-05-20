from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hospital_lanfranco_secret_2024'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/hospital_lanfranco'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
try:
    with app.app_context():
        db.engine.connect()
        print("✅ Conectado a MySQL correctamente")
except Exception as e:
    print("❌ Error de conexión:")
    print(e)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor inicia sesion para acceder.'

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(8), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    telefono = db.Column(db.String(15))
    password = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), default='paciente')
    fecha_nac = db.Column(db.Date)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    citas = db.relationship('Cita', backref='paciente', lazy=True)

class Especialidad(db.Model):
    __tablename__ = 'especialidades'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    icono = db.Column(db.String(50))
    activa = db.Column(db.Boolean, default=True)
    medicos = db.relationship('Medico', backref='especialidad', lazy=True)

class Medico(db.Model):
    __tablename__ = 'medicos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    apellido = db.Column(db.String(150), nullable=False)
    cmp = db.Column(db.String(20), unique=True)
    especialidad_id = db.Column(db.Integer, db.ForeignKey('especialidades.id'))
    disponible = db.Column(db.Boolean, default=True)
    citas = db.relationship('Cita', backref='medico', lazy=True)

class Cita(db.Model):
    __tablename__ = 'citas'
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    especialidad_id = db.Column(db.Integer, db.ForeignKey('especialidades.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.String(10), nullable=False)
    motivo = db.Column(db.Text)
    estado = db.Column(db.String(20), default='pendiente')
    tipo = db.Column(db.String(20), default='manual')
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    especialidad = db.relationship('Especialidad', backref='citas')

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

def inicializar_db():
    db.create_all()
    if not Especialidad.query.first():
        esp_list = [
            ('Cardiologia','Diagnostico y tratamiento de enfermedades del corazon.','❤️'),
            ('Pediatria','Atencion medica integral para ninos y adolescentes.','👶'),
            ('Ginecologia','Salud reproductiva y atencion a la mujer.','🌸'),
            ('Traumatologia','Tratamiento de lesiones oseas y musculares.','🦴'),
            ('Medicina General','Atencion primaria y consulta general.','🩺'),
            ('Oftalmologia','Diagnostico y tratamiento de enfermedades oculares.','👁️'),
            ('Neurologia','Enfermedades del sistema nervioso.','🧠'),
            ('Dermatologia','Diagnostico y tratamiento de enfermedades de la piel.','🧬'),
        ]
        for n,d,i in esp_list:
            db.session.add(Especialidad(nombre=n,descripcion=d,icono=i))
        db.session.commit()
        medicos_data = [
            ('Carlos','Mendoza Ruiz','CM-12345',1),
            ('Ana','Garcia Lopez','CM-23456',2),
            ('Rosa','Torres Vega','CM-34567',3),
            ('Luis','Ramos Flores','CM-45678',4),
            ('Jorge','Castillo Pena','CM-56789',5),
        ]
        for n,a,c,e in medicos_data:
            db.session.add(Medico(nombre=n,apellido=a,cmp=c,especialidad_id=e))
        db.session.add(Usuario(nombre='Admin',apellido='Hospital',dni='00000000',
            email='admin@lanfranco.pe',password=generate_password_hash('admin123'),rol='admin'))
        db.session.commit()
        print("DB inicializada OK")

@app.route('/')
def index():
    return render_template('index.html', especialidades=Especialidad.query.filter_by(activa=True).all())

@app.route('/registro', methods=['GET','POST'])
def registro():
    if current_user.is_authenticated: return redirect(url_for('dashboard'))
    if request.method == 'POST':
        nombre=request.form.get('nombre','').strip()
        apellido=request.form.get('apellido','').strip()
        dni=request.form.get('dni','').strip()
        email=request.form.get('email','').strip()
        telefono=request.form.get('telefono','').strip()
        password=request.form.get('password','')
        confirm=request.form.get('confirm_password','')
        fecha_nac_str=request.form.get('fecha_nac','')
        if not all([nombre,apellido,dni,email,password]):
            flash('Todos los campos obligatorios deben completarse.','error'); return render_template('registro.html')
        if password!=confirm:
            flash('Las contrasenas no coinciden.','error'); return render_template('registro.html')
        if len(dni)!=8 or not dni.isdigit():
            flash('El DNI debe tener 8 digitos numericos.','error'); return render_template('registro.html')
        if Usuario.query.filter_by(email=email).first():
            flash('El correo electronico ya esta registrado.','error'); return render_template('registro.html')
        if Usuario.query.filter_by(dni=dni).first():
            flash('El DNI ya esta registrado.','error'); return render_template('registro.html')
        fecha_nac=None
        if fecha_nac_str:
            try: fecha_nac=datetime.strptime(fecha_nac_str,'%Y-%m-%d').date()
            except: pass
        db.session.add(Usuario(nombre=nombre,apellido=apellido,dni=dni,email=email,
            telefono=telefono,password=generate_password_hash(password),fecha_nac=fecha_nac))
        db.session.commit()
        flash('Registro exitoso! Ya puedes iniciar sesion.','success')
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated: return redirect(url_for('dashboard'))
    if request.method=='POST':
        email=request.form.get('email','').strip()
        password=request.form.get('password','')
        u=Usuario.query.filter_by(email=email).first()
        if u and check_password_hash(u.password,password):
            login_user(u)
            flash(f'Bienvenido, {u.nombre}!','success')
            return redirect(request.args.get('next') or url_for('dashboard'))
        flash('Correo o contrasena incorrectos.','error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user(); flash('Sesion cerrada correctamente.','info'); return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    citas=Cita.query.filter_by(paciente_id=current_user.id).order_by(Cita.fecha.desc()).all()
    return render_template('dashboard.html',citas=citas)

@app.route('/solicitar-cita', methods=['GET','POST'])
@login_required
def solicitar_cita():
    especialidades=Especialidad.query.filter_by(activa=True).all()
    today_str=date.today().isoformat()
    if request.method=='POST':
        esp_id=request.form.get('especialidad_id')
        med_id=request.form.get('medico_id')
        fecha_s=request.form.get('fecha')
        hora=request.form.get('hora')
        motivo=request.form.get('motivo','')
        tipo=request.form.get('tipo','manual')
        if not all([esp_id,med_id,fecha_s,hora]):
            flash('Completa todos los campos requeridos.','error')
            return render_template('solicitar_cita.html',especialidades=especialidades,today=today_str)
        try: fecha=datetime.strptime(fecha_s,'%Y-%m-%d').date()
        except:
            flash('Fecha invalida.','error')
            return render_template('solicitar_cita.html',especialidades=especialidades,today=today_str)
        if fecha<date.today():
            flash('La fecha no puede ser en el pasado.','error')
            return render_template('solicitar_cita.html',especialidades=especialidades,today=today_str)
        if Cita.query.filter_by(medico_id=med_id,fecha=fecha,hora=hora).first():
            flash('Ese horario ya esta ocupado.','error')
            return render_template('solicitar_cita.html',especialidades=especialidades,today=today_str)
        db.session.add(Cita(paciente_id=current_user.id,medico_id=int(med_id),
            especialidad_id=int(esp_id),fecha=fecha,hora=hora,motivo=motivo,tipo=tipo))
        db.session.commit()
        flash('Cita registrada exitosamente!','success')
        return redirect(url_for('dashboard'))
    return render_template('solicitar_cita.html',especialidades=especialidades,today=today_str)

@app.route('/cancelar-cita/<int:cita_id>', methods=['POST'])
@login_required
def cancelar_cita(cita_id):
    c=Cita.query.get_or_404(cita_id)
    if c.paciente_id!=current_user.id and current_user.rol!='admin':
        flash('No tienes permiso.','error'); return redirect(url_for('dashboard'))
    c.estado='cancelada'; db.session.commit()
    flash('Cita cancelada.','info'); return redirect(url_for('dashboard'))

@app.route('/api/medicos/<int:esp_id>')
def api_medicos(esp_id):
    m=Medico.query.filter_by(especialidad_id=esp_id,disponible=True).all()
    return jsonify([{'id':x.id,'nombre':f'Dr. {x.nombre} {x.apellido}'} for x in m])

@app.route('/api/horarios/<int:medico_id>/<fecha>')
def api_horarios(medico_id,fecha):
    todos=['08:00','08:30','09:00','09:30','10:00','10:30','11:00','11:30','14:00','14:30','15:00','15:30','16:00','16:30']
    try: fo=datetime.strptime(fecha,'%Y-%m-%d').date()
    except: return jsonify([])
    ocup=[c.hora for c in Cita.query.filter_by(medico_id=medico_id,fecha=fo).filter(Cita.estado!='cancelada').all()]
    return jsonify([h for h in todos if h not in ocup])

@app.route('/admin')
@login_required
def admin():
    if current_user.rol!='admin':
        flash('Acceso restringido.','error'); return redirect(url_for('dashboard'))
    return render_template('admin.html',
        total_usuarios=Usuario.query.count(),
        total_citas=Cita.query.count(),
        citas_hoy=Cita.query.filter_by(fecha=date.today()).count(),
        citas_pendientes=Cita.query.filter_by(estado='pendiente').count(),
        citas_recientes=Cita.query.order_by(Cita.creado_en.desc()).limit(15).all())

@app.route('/admin/confirmar/<int:cita_id>', methods=['POST'])
@login_required
def confirmar_cita(cita_id):
    if current_user.rol!='admin': return jsonify({'error':'No autorizado'}),403
    c=Cita.query.get_or_404(cita_id); c.estado='confirmada'; db.session.commit()
    return jsonify({'ok':True})

if __name__=='__main__':
    with app.app_context():
        inicializar_db()
    app.run(debug=True,port=5000)
