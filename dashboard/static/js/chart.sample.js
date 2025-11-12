document.addEventListener("DOMContentLoaded", function () {
    function getJSON(id) {
        const el = document.getElementById(id);
        return el ? JSON.parse(el.textContent) : [];
    }

    const categories = getJSON("data-categories");
    const movies = getJSON("data-movies");
    const months = getJSON("data-months");
    const revenue = getJSON("data-revenue");
    const topFilms = getJSON("data-top-films");
    const topRevenue = getJSON("data-top-revenue");
    const countries = getJSON("data-countries");
    const clients = getJSON("data-clients");

    // Gráfico 1
    if (categories.length && movies.length) {
        new Chart(document.getElementById("grafico-1"), {
            type: "bar",
            data: {
                labels: categories,
                datasets: [{ label: "Películas", data: movies, borderWidth: 1 }]
            },
            options: { responsive: true, plugins: { legend: { display: false } } }
        });
    }

    // Gráfico 2
    if (months.length && revenue.length) {
        new Chart(document.getElementById("grafico-2"), {
            type: "line",
            data: { labels: months, datasets: [{ label: "Ingresos por mes (€)", data: revenue, borderWidth: 2, fill: false, tension: 0.3 }] },
            options: { responsive: true, plugins: { legend: { display: true } }, scales: { y: { beginAtZero: true } } }
        });
    }

    // Gráfico 3
    if (topFilms.length && topRevenue.length) {
        new Chart(document.getElementById("grafico-3"), {
            type: "bar",
            data: { labels: topFilms, datasets: [{ label: "Total de alquileres (€)", data: topRevenue, borderWidth: 1 }] },
            options: { responsive: true, indexAxis: 'y', plugins: { legend: { display: false } } }
        });
    }

    // Gráfico 4
    if (categories.length && movies.length) {
        new Chart(document.getElementById("grafico-4"), {
            type: "bar",
            data: {
                labels: countries,
                datasets: [{ label: "Usuarios", data: movies, borderWidth: 1 }]
            },
            options: { responsive: true, plugins: { legend: { display: false } } }
        });
    }
});