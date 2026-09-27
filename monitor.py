import sqlite3
from datetime import date
from pathlib import Path

from kabum import buscar_kabum

BUSCA = "playstation 5"
PRODUTO_URL = "https://www.kabum.com.br/produto/934759/console-sony-playstation-5-com-leitor-de-discos-ssd-1tb-controle-sem-fio-dualsense-2-jogos"
BANCO = Path(__file__).parent / "precos.db"


def buscar_produto():
    for item in buscar_kabum(BUSCA):
        if item["url"] == PRODUTO_URL:
            return item
    raise ValueError("produto nao encontrado na busca")


def salvar(item):
    preco = item["preco_com_desconto"] or item["preco"]

    con = sqlite3.connect(BANCO)
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS precos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            produto TEXT NOT NULL,
            preco REAL NOT NULL,
            url TEXT NOT NULL
        )
        """
    )
    con.execute(
        "INSERT INTO precos (data, produto, preco, url) VALUES (?, ?, ?, ?)",
        (date.today().isoformat(), item["nome"], preco, item["url"]),
    )
    con.commit()
    con.close()
    return preco


def main():
    item = buscar_produto()
    preco = salvar(item)
    print(f"{date.today().isoformat()} - {item['nome']}: R$ {preco}")


if __name__ == "__main__":
    main()
