
# admin_routes.py
from middleware import admin_required

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    return 'Admin Dashboard'