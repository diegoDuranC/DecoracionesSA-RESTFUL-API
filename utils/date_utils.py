from datetime import datetime

def format_date(date_str):
    """
    Formatea una fecha a 'YYYY-MM-DD'. Si la fecha no está en el formato correcto,
    devuelve la fecha actual en 'YYYY-MM-DD'.
    
    :param date_str: La fecha como cadena.
    :return: La fecha formateada como 'YYYY-MM-DD'.
    """
    if date_str:
        for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
            try: 
                # Intentar convertir la fecha a un objeto datetime
                date = datetime.strptime(date_str, fmt)
                # Formatear la fecha de nuevo al formato YYYY-MM-DD
                return date.strftime("%Y-%m-%d")
            
            except ValueError:
                continue
        # Si no se pudo convertir, asignar la fecha actual como vencimiento en caso de error
        return datetime.now().strftime("%Y-%m-%d")
    
    else:
        # Asignar una fecha predeterminada si no se proporciona una fecha de vencimiento
        return datetime.now().strftime("%Y-%m-%d")