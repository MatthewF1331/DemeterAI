import { connectWebSocket } from './websocket.js';
import { setupGlobalSearch, loadDatabaseImages, loadImageDetails } from './database.js';
import { setupDateFilters } from './dashboard.js';

document.addEventListener("DOMContentLoaded", async () => {

    await connectWebSocket();

    setupGlobalSearch();

    setupDateFilters();

    // ----- LOGICA PARA PAGINAS -----

    // Lógica para DATABASE.HTML
    if (document.getElementById("databasePage")) {
        const params = new URLSearchParams(window.location.search);
        const urlSearchQuery = params.get("search_query") || '';
        const searchInput = document.getElementById("globalSearchInput");

        if (urlSearchQuery) {
            if (searchInput) searchInput.value = urlSearchQuery;
            loadDatabaseImages(urlSearchQuery);
        } else {
            loadDatabaseImages();
        }
    }

    // Lógica para DATABASE-DETALHES.HTML
    if (document.getElementById("databaseDetailsPage")) {
        const params = new URLSearchParams(window.location.search);
        const id = params.get("id");

        if (id) {
            loadImageDetails(id);
        } else {
            const mainTitle = document.getElementById("fileTitle");
            if (mainTitle) mainTitle.textContent = "Erro: ID Ausente";
        }
    }
});