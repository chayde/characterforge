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
document.addEventListener('DOMContentLoaded', () => {
    // We could fetch character data here eventually
});
