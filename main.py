from app import create_app

app = create_app()

# Registro de la API
if __name__ == '__main__':
    app.run()