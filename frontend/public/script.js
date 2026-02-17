function switchTab(tabName) {
    // Hide all contents
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.add('hidden');
    });
    
    // Remove active class from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('tab-active');
    });
    
    // Show selected content
    document.getElementById(`content-${tabName}`).classList.remove('hidden');
    
    // Set active button
    document.getElementById(`tab-${tabName}`).classList.add('tab-active');
}

function rollDice(die, bonus, label) {
    const roll = Math.floor(Math.random() * die) + 1;
    const total = roll + bonus;
    
    const overlay = document.getElementById('dice-overlay');
    const resultText = document.getElementById('dice-result-text');
    
    resultText.innerHTML = `<span class="text-sm opacity-75">${label}:</span> ${total} <span class="text-sm opacity-75">(${roll} + ${bonus})</span>`;
    
    overlay.classList.remove('hidden');
    overlay.classList.remove('translate-y-20');
    
    // Hide after 4 seconds
    setTimeout(() => {
        overlay.classList.add('translate-y-20');
        setTimeout(() => overlay.classList.add('hidden'), 500);
    }, 4000);
}

// Initial setup
document.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const charId = urlParams.get('id');

    if (charId) {
        await loadCharacter(charId);
    }
});

async function loadCharacter(id) {
    try {
        const response = await fetch(`/api/characters/${id}`);
        if (!response.ok) throw new Error("Character not found");
        const char = await response.json();

        // Update Header
        document.getElementById('char-name').textContent = char.name;
        document.getElementById('curr-hp').textContent = char.current_hp;
        document.getElementById('max-hp').textContent = char.max_hp;
        
        // Update Stats (simplified mapping)
        updateStatBox('Strength', 'STR', char.strength);
        updateStatBox('Dexterity', 'DEX', char.dexterity);
        updateStatBox('Constitution', 'CON', char.constitution);
        updateStatBox('Intelligence', 'INT', char.intelligence);
        updateStatBox('Wisdom', 'WIS', char.wisdom);
        updateStatBox('Charisma', 'CHA', char.charisma);

        // Update AC and Init
        const dexMod = Math.floor((char.dexterity - 10) / 2);
        document.getElementById('ac').textContent = 10 + dexMod + 2; // Assuming shield for fighter
        document.getElementById('init').textContent = (dexMod >= 0 ? '+' : '') + dexMod;

    } catch (err) {
        console.error(err);
    }
}

function updateStatBox(label, short, score) {
    const boxes = document.querySelectorAll('.stat-box');
    const mod = Math.floor((score - 10) / 2);
    
    for (let box of boxes) {
        if (box.innerText.includes(short)) {
            box.querySelector('.text-2xl').textContent = score;
            box.querySelector('.text-sm').textContent = (mod >= 0 ? '+' : '') + mod;
            box.setAttribute('onclick', `rollDice(20, ${mod}, '${label}')`);
            break;
        }
    }
}
