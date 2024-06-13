from app import create_app, create_tables

app = create_app()

# Registro de la API
if __name__ == '__main__':
    
    create_tables(app)
    app.run(host='25.5.250.33', port=5000, debug=True)
    app.run()