const ws = new WebSocket('ws://127.0.0.1:8000/ws');
const feed = document.getElementById('live-feed');
const statusContainer = document.getElementById('agent-status');

// Add connection status
const connStatus = document.createElement('div');
connStatus.id = 'connection-status';
connStatus.style.gridColumn = 'span 2';
connStatus.style.padding = '5px';
connStatus.style.textAlign = 'center';
connStatus.style.borderRadius = '5px';
connStatus.style.marginBottom = '10px';
connStatus.innerText = 'Connecting to backend...';
connStatus.style.background = '#f39c12';
statusContainer.prepend(connStatus);

ws.onopen = () => {
    connStatus.innerText = 'Connected to Backend';
    connStatus.style.background = '#27ae60';
    connStatus.style.color = 'white';
};

ws.onerror = () => {
    connStatus.innerText = 'Connection Error';
    connStatus.style.background = '#e74c3c';
    connStatus.style.color = 'white';
};

const agents = ['Project Manager', 'UI/UX Designer', 'Frontend Developer', 'Backend Developer', 'QA Engineer', 'DevOps Engineer'];
const agentMap = {
    'Project Manager': 'pm',
    'UI/UX Designer': 'ui',
    'Frontend Developer': 'frontend',
    'Backend Developer': 'backend',
    'QA Engineer': 'qa',
    'DevOps Engineer': 'devops'
};

// Colors for agents to match 3D scene
const agentColors = {
    'Project Manager': '#2D9F77',
    'UI/UX Designer': '#7F77DD',
    'Frontend Developer': '#378ADD',
    'Backend Developer': '#D85A30',
    'QA Engineer': '#BA7517',
    'DevOps Engineer': '#639922'
};

agents.forEach(name => {
    const card = document.createElement('div');
    card.className = 'status-card';
    card.id = `status-${agentMap[name]}`;
    card.style.borderLeft = `4px solid ${agentColors[name]}`;
    card.innerHTML = `<strong>${name}</strong><br><span class="status-text">Idle</span>`;
    statusContainer.appendChild(card);
});

function sendTask() {
    const description = document.getElementById('taskInput').value;
    if (!description) return;
    
    feed.innerHTML = ''; // Clear feed for new task
    fetch('http://127.0.0.1:8000/task', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({description})
    });
}

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    // Add to feed
    const msg = document.createElement('div');
    msg.className = 'msg';
    msg.style.borderLeft = `3px solid ${agentColors[data.from] || '#ccc'}`;
    msg.innerHTML = `<strong>${data.from}:</strong> ${data.message}`;
    feed.prepend(msg);
    
    // Update status
    const internalFrom = agentMap[data.from];
    if (internalFrom) {
        const card = document.getElementById(`status-${internalFrom}`);
        if (card) {
            const statusText = card.querySelector('.status-text');
            statusText.innerText = data.message.includes('Thinking...') ? 'Thinking...' : 'Active';
            statusText.style.color = data.message.includes('Thinking...') ? '#f39c12' : '#27ae60';
        }

        // Show 3D bubble and particle
        if (typeof showSpeechBubble === 'function') {
            showSpeechBubble(internalFrom, data.message);
        }
        if (typeof spawnParticle === 'function') {
            spawnParticle(internalFrom, data.to || 'All');
        }
    }
    
    // Check if task is complete
    if (data.message.includes('✅ All tasks completed')) {
        agents.forEach(name => {
            const card = document.getElementById(`status-${agentMap[name]}`);
            if (card) card.querySelector('.status-text').innerText = 'Idle';
        });
    }
};

// Refresh workspace files every 5 seconds
function refreshWorkspace() {
    fetch('http://127.0.0.1:8000/workspace')
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById('file-list');
            list.innerHTML = '';
            data.files.forEach(file => {
                const item = document.createElement('div');
                item.style.padding = '2px 0';
                item.style.cursor = 'pointer';
                item.style.borderBottom = '1px solid #34495e';
                item.innerText = '📄 ' + file;
                item.onclick = () => {
                    fetch(`http://127.0.0.1:8000/workspace/${file}`)
                        .then(res => res.json())
                        .then(fileData => {
                            alert(`Content of ${file}:\n\n${fileData.content}`);
                        });
                };
                list.appendChild(item);
            });
        });
}

setInterval(refreshWorkspace, 5000);
refreshWorkspace();
