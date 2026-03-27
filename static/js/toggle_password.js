document.addEventListener("DOMContentLoaded", function () {
    const botoes = document.querySelectorAll("[data-toggle-password]");

    botoes.forEach(function (botao) {
        if (botao.dataset.togglePasswordBound === "true") return;
        botao.dataset.togglePasswordBound = "true";

        botao.addEventListener("click", function () {
            const targetId = botao.getAttribute("data-target-id");
            const input = document.getElementById(targetId);
            const icon = botao.querySelector("i");

            if (!input || !icon) return;

            if (input.type === "password") {
                input.type = "text";
                icon.className = "bi bi-eye-slash";
                botao.setAttribute("aria-label", "Ocultar senha");
                botao.setAttribute("title", "Ocultar senha");
            } else {
                input.type = "password";
                icon.className = "bi bi-eye";
                botao.setAttribute("aria-label", "Mostrar senha");
                botao.setAttribute("title", "Mostrar senha");
            }
        });
    });
});