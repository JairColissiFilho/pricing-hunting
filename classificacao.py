
import re
import unicodedata


def normalizar(texto: str) -> str:
    """'Placa de Vídeo Asus' -> 'placa de video asus' (minusculo, sem acento)."""
    if not texto:
        return ""
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("ascii")
    texto = texto.lower()
    texto = re.sub(r"[^a-z0-9]+", " ", texto)  # pontuacao -> espaco
    return re.sub(r"\s+", " ", texto).strip()


# --- categoria -------------------------------------------------------------
# ordem importa: a primeira regra que casar vence.
# (um "PC Gamer com RTX 3060" tem que cair em pc_gamer, nao em placa_de_video)
REGRAS_CATEGORIA = [
    ("pc_gamer",        ["pc gamer", "computador gamer", "cpu gamer", "pc gaming"]),
    ("notebook",        ["notebook", "laptop"]),
    ("console",         ["playstation", "xbox", "nintendo", "ps5", "ps4"]),
    ("monitor",         ["monitor"]),
    ("placa_de_video",  ["placa de video", "geforce", "radeon", "rtx", "gtx", "rx 5", "rx 6", "rx 7"]),
    ("processador",     ["processador", "ryzen", "core i3", "core i5", "core i7", "core i9", "pentium"]),
    ("placa_mae",       ["placa mae", "motherboard"]),
    ("memoria_ram",     ["memoria ram", "memoria dimm", "ddr4", "ddr5"]),
    ("armazenamento",   ["ssd", "hd ", "nvme", "m 2"]),
    ("fonte",           ["fonte ", "psu"]),  # regras acima ja capturaram gpu/pc que citem "fonte"
]


def classificar_categoria(nome: str) -> str:
    n = normalizar(nome)
    for categoria, chaves in REGRAS_CATEGORIA:
        if any(chave in n for chave in chaves):
            return categoria
    return "outro"


# --- condicao -------------------------------------------------------------
REGRAS_CONDICAO = [
    ("recondicionado", ["recondicionado", "refurbished"]),
    ("usado",          ["usado", "seminovo", "semi novo", "open box", "openbox", "vitrine"]),
]


def classificar_condicao(nome: str) -> str:
    n = normalizar(nome)
    for condicao, chaves in REGRAS_CONDICAO:
        if any(chave in n for chave in chaves):
            return condicao
    return "novo"


# --- tags ---------------------------------------------------------------
STOPWORDS = {
    "de", "da", "do", "das", "dos", "com", "sem", "para", "por", "e", "ou",
    "a", "o", "os", "as", "em", "no", "na", "nos", "nas", "um", "uma",
    "bits", "bit", "ate",
}


def extrair_tags(nome: str) -> list[str]:
    """Tokens normalizados do nome, sem stopword nem duplicata, ordem preservada."""
    tags = []
    for token in normalizar(nome).split():
        if len(token) < 2 or token in STOPWORDS:
            continue
        if token not in tags:
            tags.append(token)
    return tags


def classificar(nome: str) -> dict:
    return {
        "categoria": classificar_categoria(nome),
        "condicao": classificar_condicao(nome),
        "tags": extrair_tags(nome),
    }


if __name__ == "__main__":
    exemplos = [
        "Placa de Vídeo Asus NVIDIA GeForce RTX 3060, 12GB GDDR6, LHR, 192 Bits - DUAL-RTX3060-O12G-V2",
        "PC Gamer Ryzen 5 5500, RTX 3060, 16GB DDR4, SSD 480GB",
        "Usado: Iphone 15 256 Gb Preto - Excelente",
    ]
    for e in exemplos:
        print(e)
        print("  ", classificar(e))
