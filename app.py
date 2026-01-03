from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from models import db, Vulnerability, VulnerabilityType, ProductEnvironment
from cvss import CVSS3
import markdown
from datetime import date
import secrets
from sqlalchemy import func

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32) # for CSRF

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vulndb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
csrf = CSRFProtect(app)

# RUN ONCE TO CREATE DB
# with app.app_context():
#     db.create_all()

@app.route('/')
def index():
    vulns = db.session.execute(
        db.select(Vulnerability).order_by(Vulnerability.report_date.desc())
    ).scalars().all()

    total_count = len(vulns)
    
    critical_count = sum(1 for v in vulns if v.cvss_severity == 'Critical')
    
    avg_score = 0
    if total_count > 0:
        total_score = sum(v.cvss_score for v in vulns)
        avg_score = round(total_score / total_count, 1)

    unique_vendors = db.session.query(func.count(func.distinct(Vulnerability.product_vendor))).scalar()

    kpi_data = {
        "total_count": total_count,
        "critical_count": critical_count,
        "avg_score": avg_score,
        "vendor_count": unique_vendors
    }

    return render_template('index.html', vulnerabilities=vulns, kpi=kpi_data)

@app.route('/vulnerability/create', methods=['GET', 'POST'])
def create_vulnerability():
    if request.method == 'POST':
        new_vuln = Vulnerability(
            title=request.form['title'],
            cve_id=request.form['cve_id'],
            cvss_vector=request.form['cvss_vector'],
            cvss_score=float(request.form['cvss_score']),
            cvss_severity=request.form['cvss_severity'],
            vulnerability_name=request.form['vulnerability_name'],
            type=VulnerabilityType(request.form['type']),
            product_env=ProductEnvironment(request.form['product_env']),
            product_name=request.form['product_name'],
            product_vendor=request.form['product_vendor'],
            product_version=request.form['product_version'],
            product_link=request.form['product_link'],
            description=request.form['description'],
            reporter=request.form['reporter'],
            report_date=date.fromisoformat(request.form['report_date']),
            disclose_date=date.fromisoformat(request.form['disclose_date']) if request.form['disclose_date'] else None
        )
        
        db.session.add(new_vuln)
        db.session.commit()
        return redirect(url_for('index'))

    # enums -> dropdown generation
    return render_template(
        'create.html', 
        vuln_types=VulnerabilityType, 
        prod_envs=ProductEnvironment
    )

@app.route('/vulnerability/<int:id>')
def vulnerability_details(id):
    vuln = db.session.execute(db.select(Vulnerability).where(Vulnerability.id == id)).scalar_one_or_none()
    
    if not vuln:
        return "Vulnerability not found", 404
        
    return render_template('details.html', vuln=vuln)