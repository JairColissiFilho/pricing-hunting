const form = document.getElementById("form-busca");
const campo = document.getElementById("campo-produto");
const botao = document.getElementById("botao-buscar");
const status = document.getElementById("status");
const resultados = document.getElementById("resultados");
const filtros = document.getElementById("filtros");
const filtroCategoria = document.getElementById("filtro-categoria");
const filtroOrdenar = document.getElementById("filtro-ordenar");

let ultimaBusca = [];

function formatarPreco(valor) {
  if (valor === null || valor === undefined) return null;
  return valor.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

function nomeCategoria(categoria) {
  return categoria.replace(/_/g, " ");
}

function precoEfetivo(item) {
  return item.preco_com_desconto ?? item.preco;
}

function criarCard(item) {
  const a = document.createElement("a");
  a.className = "card";
  a.href = item.url;
  a.target = "_blank";
  a.rel = "noopener noreferrer";

  const img = document.createElement("img");
  img.src = item.imagem || "";
  img.alt = item.nome || "";
  img.loading = "lazy";
  a.appendChild(img);

  const body = document.createElement("div");
  body.className = "card-body";

  const nome = document.createElement("div");
  nome.className = "card-nome";
  nome.textContent = item.nome || "(sem nome)";
  body.appendChild(nome);

  const precos = document.createElement("div");
  precos.className = "precos";

  const precoOriginal = formatarPreco(item.preco);
  const precoComDesconto = formatarPreco(item.preco_com_desconto);

  if (precoComDesconto && item.preco_com_desconto !== item.preco) {
    const antigo = document.createElement("div");
    antigo.className = "preco-antigo";
    antigo.textContent = precoOriginal || "";
    precos.appendChild(antigo);
  }

  const atual = document.createElement("div");
  atual.className = "preco-atual";
  atual.textContent = precoComDesconto || precoOriginal || "Preço indisponível";
  precos.appendChild(atual);

  if (item.disponivel === false) {
    const indisponivel = document.createElement("div");
    indisponivel.className = "indisponivel";
    indisponivel.textContent = "Indisponível";
    precos.appendChild(indisponivel);
  }

  body.appendChild(precos);
  a.appendChild(body);
  return a;
}

function popularFiltroCategoria(dados) {
  const categorias = [...new Set(dados.map((item) => item.categoria))].sort();

  filtroCategoria.innerHTML = '<option value="">Todas</option>';
  categorias.forEach((categoria) => {
    const option = document.createElement("option");
    option.value = categoria;
    option.textContent = nomeCategoria(categoria);
    filtroCategoria.appendChild(option);
  });
}

function aplicarFiltroEOrdenacao() {
  let lista = ultimaBusca;

  if (filtroCategoria.value) {
    lista = lista.filter((item) => item.categoria === filtroCategoria.value);
  }

  lista = [...lista];
  if (filtroOrdenar.value === "menor-preco") {
    lista.sort((a, b) => precoEfetivo(a) - precoEfetivo(b));
  } else if (filtroOrdenar.value === "maior-preco") {
    lista.sort((a, b) => precoEfetivo(b) - precoEfetivo(a));
  }

  resultados.innerHTML = "";
  lista.forEach((item) => resultados.appendChild(criarCard(item)));
  status.textContent = `${lista.length} resultado(s)`;
}

async function buscar(produto) {
  status.textContent = `Buscando "${produto}"...`;
  resultados.innerHTML = "";
  filtros.hidden = true;
  botao.disabled = true;

  try {
    const resp = await fetch(`/api/buscar?q=${encodeURIComponent(produto)}`);
    const dados = await resp.json();

    if (!resp.ok) {
      status.textContent = `Erro: ${dados.erro || resp.statusText}`;
      return;
    }

    if (dados.length === 0) {
      status.textContent = "Nenhum produto encontrado.";
      return;
    }

    ultimaBusca = dados;
    popularFiltroCategoria(dados);
    filtros.hidden = false;
    aplicarFiltroEOrdenacao();
  } catch (err) {
    status.textContent = "Erro ao buscar. Verifique se o servidor está rodando.";
  } finally {
    botao.disabled = false;
  }
}

form.addEventListener("submit", (ev) => {
  ev.preventDefault();
  const produto = campo.value.trim();
  if (produto) buscar(produto);
});

filtroCategoria.addEventListener("change", aplicarFiltroEOrdenacao);
filtroOrdenar.addEventListener("change", aplicarFiltroEOrdenacao);
