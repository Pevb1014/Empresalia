from datetime import date, datetime

def normalizar_fecha_a_date(fecha):
    """
    Asegura que el valor sea un objeto de tipo date.
    Si recibe un datetime, extrae solo la fecha.
    Si no es un tipo compatible, devuelve el valor original para que
    los validadores de Django manejen el error.
    """
    if isinstance(fecha, datetime):
        return fecha.date()
    
    if isinstance(fecha, date):
        return fecha
        
    return fecha
