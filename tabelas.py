import json
from pathlib import Path

import pandas as pd

from classificacao import classificar
from kabum import buscar_kabum

BUSCA = "iphone"
ARQUIVO = Path("tabelas") / "kabum.csv"
HOJE = pd.Timestamp.today().strftime("%Y-%m-%d")

# resultado da busca de hoje
df = pd.DataFrame(buscar_kabum(BUSCA))
df.insert(0, "busca", BUSCA)
df["data_hora"] = HOJE

# junta com o historico, SUBSTITUINDO o snapshot de hoje pra essa busca.
# (o Kabum embaralha os resultados a cada request, entao rodar 2x no mesmo
#  dia traria URLs diferentes e infariam o historico -> cada dia = 1 coleta)
ARQUIVO.parent.mkdir(exist_ok=True)
if ARQUIVO.exists():
    historico = pd.read_csv(ARQUIVO)
    ja_coletado_hoje = (historico["busca"] == BUSCA) & (historico["data_hora"] == HOJE)
    historico = historico[~ja_coletado_hoje]
    df = pd.concat([historico, df], ignore_index=True)

# classifica todas as linhas (regras centralizadas em classificacao.py);
# recalcula sempre, entao linhas antigas tambem ficam preenchidas
classificado = df["nome"].fillna("").map(classificar).apply(pd.Series)
df["categoria"] = classificado["categoria"]
df["condicao"] = classificado["condicao"]
df["tags"] = classificado["tags"].map(lambda t: json.dumps(t, ensure_ascii=False))

df.to_csv(ARQUIVO, index=False, encoding="utf-8-sig")
print(f"{len(df)} linhas salvas em {ARQUIVO}")
print(df[["nome", "categoria", "condicao", "tags"]].head(10).to_string())
df