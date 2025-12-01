import { getBaseUrl } from './config.js';
import { sendFilterUpdate } from './websocket.js';

let currentImageFileName = null;

export function setupGlobalSearch() {
    const searchInput = document.getElementById("globalSearchInput");
    const searchIcon = document.getElementById("globalSearchIcon");

    if (!searchInput) return;

    const performSearch = () => {
        const query = searchInput.value.trim();
        if (query.length > 0) {
            window.location.href = `database.html?search_query=${encodeURIComponent(query)}`;
        }
    };

    searchInput.addEventListener('keyup', (e) => { if (e.key === 'Enter') performSearch(); });
    if (searchIcon) searchIcon.addEventListener('click', performSearch);

    // Lógica específica dentro da página database
    if (document.getElementById("databasePage")) {
        let timeout;
        searchInput.addEventListener('keyup', () => {
            clearTimeout(timeout);
            timeout = setTimeout(() => loadDatabaseImages(searchInput.value), 300);
        });
    }
}

export async function loadDatabaseImages(searchQuery = '') {
    const grid = document.getElementById("databaseGrid");
    if (!grid) return;

    grid.innerHTML = '<div style="grid-column: 1/-1; text-align:center;">Carregando...</div>';

    try {
        const queryParam = searchQuery ? `search_query=${encodeURIComponent(searchQuery)}` : '';
        const response = await fetch(`${getBaseUrl()}/database/images?${queryParam}`);
        if (!response.ok) throw new Error('Erro na API');
        const images = await response.json();

        if (!images || images.length === 0) {
            grid.innerHTML = '<div style="grid-column: 1/-1; text-align:center; padding: 50px;">Nenhuma imagem encontrada.</div>';
            sendFilterUpdate('7 days');
            return;
        }

        grid.innerHTML = '';
        images.forEach(image => {
            let statusColor = '#3B82F6';
            const f = String(image.fase_principal).toLowerCase();
            if(f === 'adulto') statusColor = '#EF4444';
            else if(f === 'ovo') statusColor = '#F59E0B';
            else if(f === 'pupa') statusColor = '#6366F1';
            else if(f.includes('não') || f === 'n/a') statusColor = '#9CA3AF';

            const rawFileName = image.file_name.split('/').pop();
            const fileNameToLoad = rawFileName.startsWith('P') ? rawFileName : `I${rawFileName.replace(/^[IP]/, '')}`;
            const imageUrl = `${getBaseUrl()}/images/${fileNameToLoad}`;

            grid.insertAdjacentHTML('beforeend', `
                <a href="database-detalhes.html?id=${image.id}" class="image-card">
                    <img src="${imageUrl}" class="image-card-img" onerror="this.src='https://placehold.co/400x300?text=Indisponível'">
                    <div class="image-card-info">
                        <span class="image-card-title">${rawFileName}</span>
                        <div class="image-card-status" style="border-left-color: ${statusColor};"></div>
                    </div>
                </a>
            `);
        });

    } catch (error) {
        console.error(error);
        grid.innerHTML = '<div style="grid-column: 1/-1; text-align:center; color:red;">Erro de conexão.</div>';
    }
}

export async function loadImageDetails(imageId) {
    const mainTitle = document.getElementById("fileTitle");
    const previewImage = document.getElementById("previewImage");
    const imageToggle = document.getElementById("imageToggle");

    if(mainTitle) mainTitle.textContent = "Carregando...";
    
    try {
        const response = await fetch(`${getBaseUrl()}/database/image/${imageId}`);
        if (!response.ok) throw new Error('Imagem não encontrada');
        const details = await response.json();

        if (mainTitle) mainTitle.textContent = details.file_name;
        currentImageFileName = details.file_name.replace(/^[IP]/, '');

        if (imageToggle) {
            imageToggle.checked = false;
            imageToggle.onchange = toggleImageVersion;
        }
        toggleImageVersion();

        const setTxt = (id, val) => { 
            const el = document.getElementById(id); 
            if(el) el.textContent = val ?? 'N/A'; 
        };
        
        setTxt('det-id', details.id);
        setTxt('det-data', details.data);
        setTxt('det-hora', details.hora);
        setTxt('det-gaiola', details.gaiola);
        setTxt('det-fase', details.fase);
        setTxt('det-qtd', details.quantidade.toLocaleString());
        setTxt('det-tamanho', details.tamanho_arquivo);
        setTxt('det-dispositivo', details.dispositivo);
        setTxt('det-precisao', details.precisao);
        setTxt('det-velocidade-cpu', details.velocidade_cpu);
        setTxt('det-versao-modelo', details.versao_modelo);
        setTxt('det-sexo', details.sexo_detectado === 'M' ? 'Macho' : details.sexo_detectado === 'F' ? 'Fêmea' : 'ND');

    } catch (error) {
        console.error(error);
        if (mainTitle) mainTitle.textContent = "Erro ao carregar";
    }
}

function toggleImageVersion() {
    const previewImage = document.getElementById("previewImage");
    const imageToggle = document.getElementById("imageToggle");
    const labelInput = document.getElementById("label-input");
    const labelProcessed = document.getElementById("label-processed");

    if (!previewImage || !currentImageFileName) return;

    const isProcessed = imageToggle && imageToggle.checked;
    const prefix = isProcessed ? 'P' : 'I';
    const newFileName = prefix + currentImageFileName;

    previewImage.src = `${getBaseUrl()}/images/${newFileName}`;
    
    if (labelInput) labelInput.style.fontWeight = !isProcessed ? '700' : '400';
    if (labelProcessed) labelProcessed.style.fontWeight = isProcessed ? '700' : '400';
}