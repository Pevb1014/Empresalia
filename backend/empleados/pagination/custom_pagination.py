from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    Clase de paginación personalizada para Django Rest Framework.

    Esta clase extiende PageNumberPagination para definir un esquema de paginación
    estándar para los conjuntos de resultados de la API. Permite controlar el tamaño
    de la página por defecto, así como permitir que el cliente especifique un tamaño
    de página y establecer un límite máximo para evitar peticiones excesivas.

    Atributos:
        page_size (int): El número de elementos a devolver en una sola página por defecto.
                         Si el cliente no especifica 'page_size', se usarán 10 elementos.
        page_size_query_param (str): El nombre del parámetro de consulta que el cliente
                                     puede usar para solicitar un tamaño de página diferente
                                     (ej. ?page_size=20).
        max_page_size (int): El número máximo de elementos que un cliente puede solicitar
                             en una sola página. Actúa como una medida de seguridad para
                             prevenir la sobrecarga del servidor.
    """
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100