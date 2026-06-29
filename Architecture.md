# JARVIS AI Assistant — Architecture

## System Architecture Diagram

```mermaid
graph TB
    subgraph Client["🖥️ Client Browser"]
        UI["Thymeleaf + Bootstrap 5<br/>HTML / CSS / JS"]
    end

    subgraph SpringBoot["☕ Spring Boot Application (Port 8080)"]
        direction TB
        Controllers["Controllers<br/>Auth | Dashboard | Chat | Reminder"]
        Security["Spring Security<br/>BCrypt + Session Management"]
        Services["Service Layer<br/>UserService | ChatService | ReminderService"]
        Repositories["Spring Data JPA<br/>Repositories"]
    end

    subgraph PythonAI["🐍 Python AI Engine (Port 5000)"]
        direction TB
        Flask["Flask REST API"]
        Chatbot["Chatbot<br/>Gemini API"]
        Speech["Speech Engine<br/>TTS / STT"]
        TaskExec["Task Executor<br/>Websites / Apps"]
        Memory["Memory Manager<br/>JSON Persistence"]
    end

    subgraph Database["🗄️ MySQL Database"]
        DB["jarvis_db<br/>users | chat_history | reminders"]
    end

    subgraph External["🌐 External Services"]
        Gemini["Google Gemini API"]
        Google["Google Speech API"]
    end

    UI -->|"HTTP / AJAX"| Controllers
    Controllers --> Security
    Controllers --> Services
    Services --> Repositories
    Repositories -->|"JPA / Hibernate"| DB
    Services -->|"REST API"| Flask
    Flask --> Chatbot
    Flask --> Speech
    Flask --> TaskExec
    Flask --> Memory
    Chatbot -->|"API Call"| Gemini
    Speech -->|"API Call"| Google

    style Client fill:#1e293b,stroke:#06b6d4,color:#f1f5f9
    style SpringBoot fill:#1e293b,stroke:#3b82f6,color:#f1f5f9
    style PythonAI fill:#1e293b,stroke:#8b5cf6,color:#f1f5f9
    style Database fill:#1e293b,stroke:#10b981,color:#f1f5f9
    style External fill:#1e293b,stroke:#f59e0b,color:#f1f5f9
```

---

## ER Diagram

```mermaid
erDiagram
    USERS {
        BIGINT id PK "AUTO_INCREMENT"
        VARCHAR username UK "NOT NULL, max 50"
        VARCHAR email UK "NOT NULL, max 100"
        VARCHAR password "NOT NULL, BCrypt hash"
        ENUM role "ROLE_USER | ROLE_ADMIN"
        DATETIME created_at "Auto-set on create"
    }

    CHAT_HISTORY {
        BIGINT id PK "AUTO_INCREMENT"
        TEXT question "NOT NULL"
        LONGTEXT response "NOT NULL"
        DATETIME timestamp "Auto-set on create"
        BIGINT user_id FK "NOT NULL"
    }

    REMINDERS {
        BIGINT id PK "AUTO_INCREMENT"
        VARCHAR title "NOT NULL, max 255"
        DATETIME reminder_time "NOT NULL"
        ENUM status "PENDING | COMPLETED | DISMISSED"
        BIGINT user_id FK "NOT NULL"
        DATETIME created_at "Auto-set on create"
    }

    USERS ||--o{ CHAT_HISTORY : "has many"
    USERS ||--o{ REMINDERS : "has many"
```

---

## Component Overview

### Spring Boot Backend

| Component | Responsibility |
|-----------|---------------|
| **SecurityConfig** | Configures Spring Security filter chain, BCrypt encoder, form login, session management |
| **CustomUserDetailsService** | Loads user details from MySQL for authentication |
| **DataInitializer** | Seeds default admin user on first startup |
| **AuthController** | Handles login/register page rendering and form submission |
| **DashboardController** | Aggregates stats and recent activity for the dashboard |
| **ChatController** | Serves chat page and AJAX endpoints for messaging |
| **ReminderController** | Serves reminders page and full CRUD REST endpoints |
| **ChatService** | Bridges Spring Boot with the Python AI Engine via REST |
| **ReminderService** | Business logic for reminder lifecycle management |
| **UserService** | Registration with BCrypt encoding, admin bootstrapping |

### Python AI Engine

| Module | Responsibility |
|--------|---------------|
| **main.py** | Flask server, route definitions, module orchestration |
| **chatbot.py** | Gemini API integration with session management and fallback responses |
| **speech_engine.py** | Text-to-speech (pyttsx3) and speech-to-text (SpeechRecognition) |
| **task_executor.py** | Natural language command parsing, website/app launching |
| **memory_manager.py** | Thread-safe JSON persistence of conversation history |

---

## Data Flow

### Chat Message Flow

```mermaid
sequenceDiagram
    participant U as User Browser
    participant C as ChatController
    participant S as ChatService
    participant P as Python AI Engine
    participant G as Gemini API
    participant DB as MySQL

    U->>C: POST /api/chat {question}
    C->>S: processChat(request, user)
    S->>P: POST http://localhost:5000/api/chat
    P->>G: send_message(question)
    G-->>P: AI response
    P-->>S: {response, status}
    S->>DB: Save ChatHistory
    S-->>C: ChatResponseDto
    C-->>U: JSON response
```

### Authentication Flow

```mermaid
sequenceDiagram
    participant U as User Browser
    participant SC as SecurityConfig
    participant UDS as CustomUserDetailsService
    participant DB as MySQL

    U->>SC: POST /login {username, password}
    SC->>UDS: loadUserByUsername(username)
    UDS->>DB: SELECT * FROM users WHERE username=?
    DB-->>UDS: User entity
    UDS-->>SC: UserDetails
    SC->>SC: BCrypt.matches(password, hash)
    SC-->>U: Redirect to /dashboard + Session cookie
```

---

## Security Architecture

- **Password Hashing**: BCrypt with strength 12
- **Session Management**: Server-side sessions with 30-minute timeout, single session per user
- **CSRF Protection**: Enabled by default, tokens passed via meta tags for AJAX requests
- **Public Paths**: `/login`, `/register`, `/css/**`, `/js/**`, `/actuator/health`
- **Protected Paths**: Everything else requires authentication
