import json

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.kabum.com.br"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}


def _preco_float(valor):
    """'3.762,37' -> 3762.37 (aceita string ou numero)"""
    if valor in (None, "", 0):
        return None
    if isinstance(valor, (int, float)):
        return float(valor)
    return float(valor.replace(".", "").replace(",", "."))


def buscar_kabum(produto: str):
    url = f"{BASE_URL}/busca/{produto.replace(' ', '-')}"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # A busca da Kabum e renderizada via JavaScript: o HTML "cru" nao tem os
    # cards. Os produtos ficam no JSON do Next.js dentro de <script id="__NEXT_DATA__">.
    next_data = soup.find("script", id="__NEXT_DATA__")
    if not next_data:
        return []

    data = json.loads(next_data.string)
    itens = data["props"]["pageProps"]["data"]["catalogServer"]["data"]

    resultados = []
    for item in itens:
        preco = _preco_float(item.get("price"))
        preco_com_desconto = _preco_float(item.get("priceWithDiscount"))
        link = f"{BASE_URL}/produto/{item['code']}/{item['friendlyName']}"

        resultados.append({
            "nome": item.get("name"),
            "preco": preco,
            "preco_com_desconto": preco_com_desconto,
            "disponivel": item.get("available"),
            "imagem": item.get("thumbnail") or item.get("image"),
            "url": link,
        })

    return resultados


if __name__ == "__main__":
    r = buscar_kabum("GTX 3060")
    for item in r[:3]:  # so os 3 primeiros, pra nao poluir o print
        print(item)
