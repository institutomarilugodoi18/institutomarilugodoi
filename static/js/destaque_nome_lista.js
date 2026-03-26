document.addEventListener("DOMContentLoaded", function () {
    const campoBusca = document.querySelector("[data-busca-nome]");
    const linhas = document.querySelectorAll("[data-linha-buscavel]");

    if (!campoBusca || !linhas.length) return;

    campoBusca.addEventListener("input", function () {
        const termo = campoBusca.value.trim().toLowerCase();

        linhas.forEach(function (linha) {
            const nome = (linha.dataset.nome || "").toLowerCase();

            if (termo.length && nome.includes(termo)) {
                linha.classList.add("table-warning");
            } else {
                linha.classList.remove("table-warning");
            }
        });
    });
});