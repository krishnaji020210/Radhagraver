from Grabber import api
from fastapi.responses import HTMLResponse



@api.get("/eval", response_class=HTMLResponse)
async def code_playground():
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced Code Playground - Telegram WebApp</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Open+Sans:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/codemirror.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/theme/material-darker.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/codemirror.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/mode/javascript/javascript.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/mode/python/python.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/mode/clike/clike.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/mode/rust/rust.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/addon/edit/closebrackets.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/addon/edit/matchbrackets.min.js"></script>
    <style>
        :root {
            --bg-primary: #0a0f1c;
            --bg-secondary: #111827;
            --bg-tertiary: #1f2937;
            --accent-primary: #06b6d4;
            --accent-secondary: #fbbf24;
            --text-primary: #f9fafb;
            --text-secondary: #d1d5db;
            --text-muted: #9ca3af;
            --border: #374151;
            --success: #10b981;
            --warning: #f59e0b;
            --error: #ef4444;
            --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Open Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            overflow-x: hidden;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 1rem;
        }

        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1.5rem;
            padding: 1rem;
            background: var(--bg-secondary);
            border-radius: 12px;
            border: 1px solid var(--border);
        }

        .title {
            font-family: 'Montserrat', sans-serif;
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--accent-primary);
        }

        .telegram-status {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: var(--bg-tertiary);
            border-radius: 8px;
            border: 1px solid var(--border);
            font-size: 0.875rem;
        }

        .status-indicator {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--error);
        }

        .status-indicator.connected {
            background: var(--success);
        }

        .main-grid {
            display: grid;
            grid-template-columns: 1fr 400px;
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }

        @media (max-width: 1024px) {
            .main-grid {
                grid-template-columns: 1fr;
            }
        }

        .editor-panel {
            background: var(--bg-secondary);
            border-radius: 12px;
            border: 1px solid var(--border);
            overflow: hidden;
        }

        .panel-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1rem;
            background: var(--bg-tertiary);
            border-bottom: 1px solid var(--border);
        }

        .panel-title {
            font-family: 'Montserrat', sans-serif;
            font-weight: 600;
            color: var(--text-primary);
        }

        .language-selector {
            display: flex;
            gap: 0.5rem;
        }

        .lang-btn {
            padding: 0.375rem 0.75rem;
            background: transparent;
            border: 1px solid var(--border);
            border-radius: 6px;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.2s;
            font-size: 0.75rem;
            font-weight: 500;
        }

        .lang-btn:hover {
            background: var(--bg-primary);
            color: var(--text-primary);
        }

        .lang-btn.active {
            background: var(--accent-primary);
            color: var(--bg-primary);
            border-color: var(--accent-primary);
        }

        .toolbar {
            display: flex;
            gap: 0.75rem;
            padding: 1rem;
            background: var(--bg-tertiary);
            border-bottom: 1px solid var(--border);
        }

        .btn {
            padding: 0.5rem 1rem;
            background: var(--accent-primary);
            color: var(--bg-primary);
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.875rem;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .btn:hover {
            background: #0891b2;
            transform: translateY(-1px);
        }

        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .btn-secondary {
            background: var(--bg-primary);
            color: var(--text-primary);
            border: 1px solid var(--border);
        }

        .btn-secondary:hover {
            background: var(--bg-tertiary);
        }

        .editor-container {
            height: 400px;
        }

        .CodeMirror {
            height: 100% !important;
            font-family: 'JetBrains Mono', 'Fira Code', Consolas, monospace !important;
            font-size: 14px !important;
            line-height: 1.5 !important;
        }

        .output-panel {
            background: var(--bg-secondary);
            border-radius: 12px;
            border: 1px solid var(--border);
            overflow: hidden;
        }

        .console-output {
            height: 300px;
            overflow-y: auto;
            padding: 1rem;
            background: var(--bg-primary);
            font-family: 'JetBrains Mono', 'Fira Code', Consolas, monospace;
            font-size: 0.875rem;
            line-height: 1.5;
        }

        .log-entry {
            margin-bottom: 0.5rem;
            padding: 0.25rem 0;
            white-space: pre-wrap;
            word-break: break-word;
        }

        .log-info { color: var(--text-primary); }
        .log-success { color: var(--success); }
        .log-warning { color: var(--warning); }
        .log-error { color: var(--error); }

        .telegram-info {
            padding: 1rem;
            background: var(--bg-tertiary);
        }

        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 0.75rem;
        }

        .info-item {
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
            padding: 0.75rem;
            background: var(--bg-primary);
            border-radius: 8px;
            border: 1px solid var(--border);
        }

        .info-label {
            font-size: 0.75rem;
            color: var(--text-muted);
            font-weight: 500;
        }

        .info-value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.875rem;
            color: var(--accent-primary);
            word-break: break-all;
        }

        .examples-section {
            background: var(--bg-secondary);
            border-radius: 12px;
            border: 1px solid var(--border);
            overflow: hidden;
        }

        .examples-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            padding: 1rem;
        }

        .example-card {
            padding: 1rem;
            background: var(--bg-tertiary);
            border-radius: 8px;
            border: 1px solid var(--border);
            cursor: pointer;
            transition: all 0.2s;
        }

        .example-card:hover {
            background: var(--bg-primary);
            border-color: var(--accent-primary);
        }

        .example-title {
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
        }

        .example-desc {
            font-size: 0.875rem;
            color: var(--text-secondary);
        }

        .loading {
            display: inline-block;
            width: 16px;
            height: 16px;
            border: 2px solid var(--border);
            border-radius: 50%;
            border-top-color: var(--accent-primary);
            animation: spin 1s ease-in-out infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1 class="title">Advanced Code Playground</h1>
            <div class="telegram-status">
                <div class="status-indicator" id="statusIndicator"></div>
                <span id="statusText">Detecting Telegram WebApp...</span>
            </div>
        </header>

        <div class="main-grid">
            <div class="editor-panel">
                <div class="panel-header">
                    <h2 class="panel-title">Code Editor</h2>
                    <div class="language-selector">
                        <button class="lang-btn active" data-lang="javascript">JavaScript</button>
                        <button class="lang-btn" data-lang="python">Python</button>
                        <button class="lang-btn" data-lang="cpp">C++</button>
                        <button class="lang-btn" data-lang="rust">Rust</button>
                    </div>
                </div>
                <div class="toolbar">
                    <button class="btn" id="runBtn">
                        <span>▶</span> Run Code
                    </button>
                    <button class="btn btn-secondary" id="clearBtn">Clear Console</button>
                    <button class="btn btn-secondary" id="downloadBtn">Download</button>
                </div>
                <div class="editor-container">
                    <textarea id="codeEditor"></textarea>
                </div>
            </div>

            <div class="output-panel">
                <div class="panel-header">
                    <h2 class="panel-title">Console Output</h2>
                </div>
                <div class="console-output" id="consoleOutput"></div>
                <div class="telegram-info">
                    <div class="info-grid">
                        <div class="info-item">
                            <span class="info-label">User ID</span>
                            <span class="info-value" id="userId">—</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Platform</span>
                            <span class="info-value" id="platform">—</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Version</span>
                            <span class="info-value" id="version">—</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Theme</span>
                            <span class="info-value" id="theme">—</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="examples-section">
            <div class="panel-header">
                <h2 class="panel-title">Code Examples</h2>
            </div>
            <div class="examples-grid" id="examplesGrid">
                <!-- Examples will be populated by JavaScript -->
            </div>
        </div>
    </div>

    <script>
        // Global variables
        let editor;
        let currentLanguage = 'javascript';
        let tg = window.Telegram?.WebApp;

        // Code examples for different languages
        const codeExamples = {
            javascript: [
                {
                    title: "Hello Telegram WebApp",
                    code: `// Basic Telegram WebApp interaction
console.log("Hello from Telegram WebApp!");

// Check if running in Telegram
if (window.Telegram && window.Telegram.WebApp) {
    const tg = window.Telegram.WebApp;
    console.log("User:", tg.initDataUnsafe.user);
    console.log("Platform:", tg.platform);
    
    // Show main button
    tg.MainButton.text = "Click Me!";
    tg.MainButton.show();
    tg.MainButton.onClick(() => {
        console.log("Main button clicked!");
    });
} else {
    console.log("Not running in Telegram WebApp");
}`
                },
                {
                    title: "DOM Manipulation",
                    code: `// Create and style elements
const div = document.createElement('div');
div.textContent = 'Dynamic Content';
div.style.color = '#06b6d4';
div.style.padding = '10px';
div.style.border = '1px solid #374151';
div.style.borderRadius = '8px';
div.style.marginTop = '10px';

// Add to console output area
const output = document.getElementById('consoleOutput');
output.appendChild(div);

console.log("Element added to page!");`
                },
                {
                    title: "Async/Await Example",
                    code: `// Fetch data example
async function fetchData() {
    try {
        console.log("Fetching data...");
        const response = await fetch('https://jsonplaceholder.typicode.com/posts/1');
        const data = await response.json();
        console.log("Data received:", data);
        return data;
    } catch (error) {
        console.error("Error:", error);
    }
}

fetchData();`
                }
            ],
            python: [
                {
                    title: "Python Basics",
                    code: `# Python code examples (for reference)
print("Hello from Python!")

# List comprehension
numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers]
print(f"Squares: {squares}")

# Dictionary example
user_data = {
    "name": "Telegram User",
    "platform": "web",
    "active": True
}

for key, value in user_data.items():
    print(f"{key}: {value}")

# Function example
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(f"Fibonacci(10): {fibonacci(10)}")`
                },
                {
                    title: "Class Example",
                    code: `# Object-oriented Python
class TelegramBot:
    def __init__(self, name):
        self.name = name
        self.users = []
    
    def add_user(self, user_id, username):
        user = {"id": user_id, "username": username}
        self.users.append(user)
        print(f"Added user: {username}")
    
    def get_user_count(self):
        return len(self.users)
    
    def __str__(self):
        return f"Bot: {self.name} with {self.get_user_count()} users"

# Usage
bot = TelegramBot("MyBot")
bot.add_user(123456, "john_doe")
bot.add_user(789012, "jane_smith")
print(bot)`
                }
            ],
            cpp: [
                {
                    title: "C++ Basics",
                    code: `#include <iostream>
#include <vector>
#include <string>

int main() {
    std::cout << "Hello from C++!" << std::endl;
    
    // Vector example
    std::vector<int> numbers = {1, 2, 3, 4, 5};
    
    std::cout << "Numbers: ";
    for (const auto& num : numbers) {
        std::cout << num << " ";
    }
    std::cout << std::endl;
    
    // String manipulation
    std::string message = "Telegram WebApp";
    std::cout << "Message length: " << message.length() << std::endl;
    
    return 0;
}`
                },
                {
                    title: "Class Example",
                    code: `#include <iostream>
#include <string>
#include <vector>

class User {
private:
    int id;
    std::string username;
    bool is_active;

public:
    User(int user_id, const std::string& name) 
        : id(user_id), username(name), is_active(true) {}
    
    void display() const {
        std::cout << "User ID: " << id 
                  << ", Username: " << username 
                  << ", Active: " << (is_active ? "Yes" : "No") 
                  << std::endl;
    }
    
    void setActive(bool active) {
        is_active = active;
    }
};

int main() {
    std::vector<User> users;
    users.emplace_back(123456, "john_doe");
    users.emplace_back(789012, "jane_smith");
    
    for (const auto& user : users) {
        user.display();
    }
    
    return 0;
}`
                }
            ],
            rust: [
                {
                    title: "Rust Basics",
                    code: `fn main() {
    println!("Hello from Rust!");
    
    // Vector example
    let numbers: Vec<i32> = vec![1, 2, 3, 4, 5];
    println!("Numbers: {:?}", numbers);
    
    // String manipulation
    let message = String::from("Telegram WebApp");
    println!("Message length: {}", message.len());
    
    // Pattern matching
    let number = 42;
    match number {
        1..=10 => println!("Small number"),
        11..=50 => println!("Medium number"),
        _ => println!("Large number"),
    }
    
    // Function call
    let result = fibonacci(10);
    println!("Fibonacci(10): {}", result);
}

fn fibonacci(n: u32) -> u32 {
    match n {
        0 => 0,
        1 => 1,
        _ => fibonacci(n - 1) + fibonacci(n - 2),
    }
}`
                },
                {
                    title: "Struct Example",
                    code: `#[derive(Debug)]
struct User {
    id: u64,
    username: String,
    is_active: bool,
}

impl User {
    fn new(id: u64, username: String) -> Self {
        User {
            id,
            username,
            is_active: true,
        }
    }
    
    fn display(&self) {
        println!("User ID: {}, Username: {}, Active: {}", 
                 self.id, self.username, self.is_active);
    }
    
    fn set_active(&mut self, active: bool) {
        self.is_active = active;
    }
}

fn main() {
    let mut users = Vec::new();
    users.push(User::new(123456, "john_doe".to_string()));
    users.push(User::new(789012, "jane_smith".to_string()));
    
    for user in &users {
        user.display();
    }
    
    println!("Total users: {}", users.len());
}`
                }
            ]
        };

        // Initialize the application
        function initApp() {
            initTelegramWebApp();
            initCodeEditor();
            initEventListeners();
            populateExamples();
            loadDefaultCode();
        }

        // Initialize Telegram WebApp
        function initTelegramWebApp() {
            const statusIndicator = document.getElementById('statusIndicator');
            const statusText = document.getElementById('statusText');
            const userId = document.getElementById('userId');
            const platform = document.getElementById('platform');
            const version = document.getElementById('version');
            const theme = document.getElementById('theme');

            if (tg) {
                try {
                    tg.ready();
                    tg.expand();
                    
                    statusIndicator.classList.add('connected');
                    statusText.textContent = 'Telegram WebApp Connected';
                    
                    const user = tg.initDataUnsafe?.user;
                    userId.textContent = user?.id || '—';
                    platform.textContent = tg.platform || '—';
                    version.textContent = tg.version || '—';
                    theme.textContent = tg.colorScheme || '—';
                    
                    // Apply theme
                    if (tg.colorScheme === 'light') {
                        document.documentElement.style.setProperty('--bg-primary', '#ffffff');
                        document.documentElement.style.setProperty('--text-primary', '#000000');
                    }
                    
                    console.log('✅ Telegram WebApp initialized successfully');
                } catch (error) {
                    console.error('❌ Telegram WebApp initialization error:', error);
                }
            } else {
                statusText.textContent = 'Not in Telegram WebApp';
                platform.textContent = navigator.userAgent.split(' ')[0];
            }
        }

        // Initialize CodeMirror editor
        function initCodeEditor() {
            const textarea = document.getElementById('codeEditor');
            editor = CodeMirror.fromTextArea(textarea, {
                mode: 'javascript',
                theme: 'material-darker',
                lineNumbers: true,
                autoCloseBrackets: true,
                matchBrackets: true,
                indentUnit: 4,
                tabSize: 4,
                lineWrapping: true,
                value: ''
            });
        }

        // Initialize event listeners
        function initEventListeners() {
            // Language selector
            document.querySelectorAll('.lang-btn').forEach(btn => {
                btn.addEventListener('click', () => switchLanguage(btn.dataset.lang));
            });

            // Toolbar buttons
            document.getElementById('runBtn').addEventListener('click', runCode);
            document.getElementById('clearBtn').addEventListener('click', clearConsole);
            document.getElementById('downloadBtn').addEventListener('click', downloadCode);
        }

        // Switch programming language
        function switchLanguage(lang) {
            currentLanguage = lang;
            
            // Update active button
            document.querySelectorAll('.lang-btn').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.lang === lang);
            });

            // Update editor mode
            const modes = {
                javascript: 'javascript',
                python: 'python',
                cpp: 'text/x-c++src',
                rust: 'rust'
            };
            
            if (editor) {
                editor.setOption('mode', modes[lang]);
                if (editor.getValue().trim() === '') {
                    editor.setValue('');
                }
            }
            
            populateExamples();
            
            logToConsole(`Switched to ${lang.toUpperCase()} mode`, 'info');
        }

        // Populate code examples
        function populateExamples() {
            const examplesGrid = document.getElementById('examplesGrid');
            examplesGrid.innerHTML = '';
            
            const examples = codeExamples[currentLanguage];
            examples.forEach((example, index) => {
                const exampleCard = document.createElement('div');
                exampleCard.className = 'example-card';
                exampleCard.innerHTML = `
                    <h3 class="example-title">${example.title}</h3>
                    <p class="example-description">Click to load this example</p>
                `;
                exampleCard.addEventListener('click', () => loadExample(currentLanguage, index));
                examplesGrid.appendChild(exampleCard);
            });
        }

        // Load default code for current language
        function loadDefaultCode() {
            const examples = codeExamples[currentLanguage];
            if (examples.length > 0) {
                editor.setValue(examples[0].code);
            }
        }

        // Run code based on current language
        function runCode() {
            const code = editor.getValue();
            const runBtn = document.getElementById('runBtn');
            
            runBtn.disabled = true;
            runBtn.innerHTML = '<div class="loading"></div> Running...';
            
            clearConsole();
            logToConsole(`Running ${currentLanguage.toUpperCase()} code...`, 'info');
            
            setTimeout(() => {
                try {
                    if (currentLanguage === 'javascript') {
                        executeJavaScript(code);
                    } else {
                        simulateExecution(code);
                    }
                } catch (error) {
                    logToConsole(`Execution error: ${error.message}`, 'error');
                } finally {
                    runBtn.disabled = false;
                    runBtn.innerHTML = '<span>▶</span> Run Code';
                }
            }, 500);
        }

        // Execute JavaScript code
        function executeJavaScript(code) {
            try {
                const safeCode = `
                    (function() {
                        const tg = window.Telegram?.WebApp;
                        const console = {
                            log: (...args) => window.logToConsole('info', args.join(' ')),
                            warn: (...args) => window.logToConsole('warning', args.join(' ')),
                            error: (...args) => window.logToConsole('error', args.join(' '))
                        };
                        
                        ${code}
                    })();
                `;
                
                eval(safeCode);
                logToConsole('JavaScript execution completed', 'success');
            } catch (error) {
                logToConsole(`JavaScript error: ${error.message}`, 'error');
            }
        }

        // Simulate execution for other languages
        function simulateExecution(code) {
            const lines = code.split('\\n');
            let outputLines = [];
            
            lines.forEach(line => {
                line = line.trim();
                if (!line || line.startsWith('//') || line.startsWith('#')) return;
                
                if (line.includes('print') || line.includes('cout') || line.includes('println!')) {
                    const match = line.match(/["']([^"']*)["']/) || line.match(/<<\\s*["']([^"']*)["']/);
                    if (match) {
                        outputLines.push(match[1]);
                    }
                }
            });
            
            if (outputLines.length > 0) {
                outputLines.forEach(output => logToConsole(output, 'info'));
            } else {
                logToConsole(`${currentLanguage.toUpperCase()} code would execute here`, 'info');
                logToConsole('This is a simulation - actual execution requires a backend compiler/interpreter', 'info');
            }
            
            logToConsole(`${currentLanguage.toUpperCase()} simulation completed`, 'success');
        }

        // Log message to console
        function logToConsole(message, type) {
            const consoleOutput = document.getElementById('consoleOutput');
            const logEntry = document.createElement('div');
            logEntry.className = `log-entry log-${type}`;
            logEntry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
            consoleOutput.appendChild(logEntry);
            consoleOutput.scrollTop = consoleOutput.scrollHeight;
        }

        // Clear console
        function clearConsole() {
            const consoleOutput = document.getElementById('consoleOutput');
            consoleOutput.innerHTML = '';
            consoleOutput.scrollTop = 0;
            console.log("[v0] Console cleared");
        }

        // Download current code
        function downloadCode() {
            const code = editor.getValue();
            const extensions = {
                javascript: 'js',
                python: 'py',
                cpp: 'cpp',
                rust: 'rs'
            };
            
            const blob = new Blob([code], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `code.${extensions[currentLanguage]}`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            logToConsole(`${currentLanguage} code downloaded`, 'success');
        }

        // Load example code
        function loadExample(lang, index) {
            const example = codeExamples[lang][index];
            if (example && editor) {
                editor.setValue(example.code);
                logToConsole(`Loaded example: ${example.title}`, 'info');
            }
        }

        // Initialize the app when DOM is loaded
        document.addEventListener('DOMContentLoaded', function() {
            console.log("[v0] Initializing Code Playground");
            
            initTelegramWebApp();
            initCodeEditor();
            initEventListeners();
            populateExamples();
            
            console.log("[v0] Code Playground initialized");
        });
    </script>
</body>
</html>"""
    
    return HTMLResponse(content=html_content, status_code=200)

