def validar_codigo(codigo):
    """
    Valida el formato del código de un producto.

    Parámetros:
        codigo (str): Código que se desea validar.

    Retorna:
        bool: True si el código es válido; False en caso contrario.
    """

    codigo = codigo.strip().upper()

    if len(codigo) == 6 and codigo.startswith("VG") and codigo[2:].isdigit():
        return True
    else:
        return False