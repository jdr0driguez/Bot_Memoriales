# test_consumo.py
import json
from core.API_parser import parse_api_response
from core.processing_serviceOri import process_elemento

def test_local():
    # 1) Carga el JSON de prueba
    with open("test_input.json", encoding="utf-8") as f:
        data = json.load(f)

    # 2) Deserializa a ApiResponse
    api_resp = parse_api_response(data)

    # 3) Normaliza a lista de Elemento
    elementos = api_resp.Element
    lista = elementos if isinstance(elementos, list) else [elementos]

    # 4) Procesa cada elemento y muestra resultado
    for e in lista:
        resultado = process_elemento(e)
        print(f"{resultado.expediente}: {'OK' if resultado.exito else 'ERROR'} – {resultado.mensaje}")

if __name__ == "__main__":
    test_local()
