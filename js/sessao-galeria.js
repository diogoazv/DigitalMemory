const cards = document.querySelectorAll(".card-fotos");

const BtnVerMais = document.querySelector(".btn-ver-mais");
const BtnVermenos = document.querySelector(".btn-ver-menos");

const galeriaAtual = document.querySelector("#galeria-atual");
const totalGalerias = document.querySelector("#total-galerias");

let cardsVisiveis = 4;


// Funcao responsavel por atualizar os cards
function atualizarCards() {

    cards.forEach((card, index) => {

        // esconde os cards que passam da quantidade visivel
        if (index >= cardsVisiveis) {
            card.style.display = "none";
        } else {
            card.style.display = "flex";
        }

    });

    // Atualiza o total de galerias
    totalGalerias.textContent = cards.length;

    // Atualiza o contador de cards 
    // O padStart coloca um zero antes de numeros menores que 10
    galeriaAtual.textContent =
        String(cardsVisiveis).padStart(2, "0");

    // Deixa btn-ver-menos sem cor quando estiver no inicio
    if (cardsVisiveis <= 4) {

        BtnVermenos.style.opacity = "0.3";
        BtnVermenos.disabled = true;

    } else {

        BtnVermenos.style.opacity = "1";
        BtnVermenos.disabled = false;

    }
    // Deixa o btn-ver-mais sem cor tambem quando chegar ao final
    if (cardsVisiveis >= cards.length) {

        BtnVerMais.style.opacity = "0.3";
        BtnVerMais.disabled = true;

    } else {

        BtnVerMais.style.opacity = "1";
        BtnVerMais.disabled = false;
    }
}


// Mostra os primeiros cards quando a pagina carrega
atualizarCards();


// Botao para mostrar mais cards
BtnVerMais.addEventListener("click", () => {
    // Guarda a quantidade de cards antes do clique
    const cardsAntes = cardsVisiveis;

    // Adiciona mais 4 cards
    cardsVisiveis += 4;

    // Impede que a quantidade passe do total de cards
    if (cardsVisiveis > cards.length) {
        cardsVisiveis = cards.length;
    }

    // Atualiza a quantidade de cards mostrados
    atualizarCards();

    // Pega somente os cards que acabaram de aparecer
    const novosCards = Array.from(cards).slice(
        cardsAntes,
        cardsVisiveis
    );

    // Define como os novos cards vao comecar
    gsap.set(novosCards, {
        opacity: 0,
        y: 30
    });

    // Faz os novos cards aparecerem
    gsap.to(novosCards, {

        opacity: 1,
        y: 0,

        duration: 0.6,

        stagger: 0.1

    });

});


// Botao para esconder cards
BtnVermenos.addEventListener("click", () => {

    // impede que sejam mostrados menos de 4 cards
    if (cardsVisiveis > 4) {

        // guarda a quantidade de cards antes de fechar
        const cardsAntes = cardsVisiveis;

        // Remove 4 cards
        cardsVisiveis -= 4;

        // pega somente os cards que vao sair
        const cardsSaindo = Array.from(cards).slice(
            cardsVisiveis,
            cardsAntes
        );

        // Faz os cards desaparecerem
        gsap.to(cardsSaindo, {

            opacity: 0,
            y: 30,

            duration: 0.4,

            stagger: 0.08,

            onComplete: () => {
                // Atualiza os cards depois da animacao
                atualizarCards();

                // Reseta os cards para poderem aparecer novamente
                gsap.set(cardsSaindo, {

                    opacity: 1,
                    y: 0

                });
            }
        });
    }
});
const menuBtn = document.querySelector(".menu-btn-mobile");
const menuLinks = document.querySelector(".nav-links-mobile");
const menuIcon = menuBtn.querySelector("i");

menuBtn.addEventListener("click", () => {

    menuLinks.classList.toggle("ativo");

    if (menuLinks.classList.contains("ativo")) {

        menuIcon.classList.remove("fa-bars");
        menuIcon.classList.add("fa-xmark");

    } else {

        menuIcon.classList.remove("fa-xmark");
        menuIcon.classList.add("fa-bars");

    }

});