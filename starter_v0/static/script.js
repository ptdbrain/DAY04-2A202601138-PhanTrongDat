const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const typingIndicator = document.getElementById('typing-indicator');
const clearBtn = document.getElementById('clear-btn');
const toolTraceTemplate = document.getElementById('tool-trace-template');

let history = []; 

userInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});

userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

sendBtn.addEventListener('click', sendMessage);
clearBtn.addEventListener('click', () => {
    history = [];
    chatMessages.innerHTML = '';
    addMessage("Agent initialized. Connected to OpenRouter. Ready for instructions.", "system");
});

function addMessage(text, role) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message`;
    
    const avatar = document.createElement('div');
    // For mapping roles to the new UI classes:
    const uiRole = role === 'system' ? 'system' : (role === 'user' ? 'user' : 'assistant');
    avatar.className = `msg-avatar ${uiRole}`;
    
    if (uiRole === 'user') {
        avatar.textContent = 'U';
    } else if (uiRole === 'assistant') {
        avatar.innerHTML = '<i class="ri-pulse-line"></i>';
    } else {
        avatar.innerHTML = '<i class="ri-terminal-box-line"></i>';
    }
    
    const content = document.createElement('div');
    content.className = 'msg-content';
    
    // Parse markdown and highlight code blocks
    content.innerHTML = marked.parse(text);
    content.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightElement(block);
    });
    
    msgDiv.appendChild(avatar);
    msgDiv.appendChild(content);
    
    chatMessages.appendChild(msgDiv);
    scrollToBottom();
    
    return content;
}

function addToolTrace(container, eventData) {
    const clone = toolTraceTemplate.content.cloneNode(true);
    const traceDiv = clone.querySelector('.tool-call');
    
    const nameEl = clone.querySelector('.tool-name');
    nameEl.textContent = eventData.tool;
    
    const argsEl = clone.querySelector('.args-content');
    argsEl.textContent = JSON.stringify(eventData.args, null, 2);
    
    const resultEl = clone.querySelector('.result-content');
    resultEl.textContent = JSON.stringify(eventData.result, null, 2);
    
    const header = clone.querySelector('.tool-call-header');
    const body = clone.querySelector('.tool-call-body');
    
    header.addEventListener('click', () => {
        traceDiv.classList.toggle('collapsed');
        body.classList.toggle('collapsed');
    });
    
    container.appendChild(traceDiv);
    scrollToBottom();
}

function scrollToBottom() {
    chatMessages.scrollTo({
        top: chatMessages.scrollHeight,
        behavior: 'smooth'
    });
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;
    
    userInput.value = '';
    userInput.style.height = 'auto';
    addMessage(text, 'user');
    typingIndicator.classList.remove('hidden');
    scrollToBottom();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_text: text,
                history: history
            })
        });
        
        const data = await response.json();
        typingIndicator.classList.add('hidden');
        
        history.push({ role: 'user', content: text });
        history.push({ role: 'assistant', content: data.assistant_text || '' });
        
        const msgContainer = addMessage(data.assistant_text || "Task complete.", 'assistant');
        
        if (data.artifact_version) {
            document.getElementById('artifact-version-badge').textContent = data.artifact_version;
        }
        
        if (data.transcript_path) {
            const tInfo = document.getElementById('transcript-info');
            if (tInfo) {
                tInfo.innerHTML = `<em>Latest transcript saved to: ${data.transcript_path}</em>`;
            }
        }
        
        if (data.tool_events && data.tool_events.length > 0) {
            data.tool_events.forEach(event => {
                addToolTrace(msgContainer, event);
            });
        }
        
    } catch (error) {
        typingIndicator.classList.add('hidden');
        addMessage(`System error: ${error.message}`, 'system');
    }
}
