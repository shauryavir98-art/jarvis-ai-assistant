# JARVIS AI Assistant

> **J**ust **A** **R**ather **V**ery **I**ntelligent **S**ystem

A full-stack AI-powered personal assistant built with Spring Boot, Thymeleaf, Spring Security, MySQL, and a Python AI Engine powered by Google Gemini.

![Java](https://img.shields.io/badge/Java-21-orange?style=flat-square)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.5-brightgreen?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square)
![MySQL](https://img.shields.io/badge/MySQL-8.0-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔐 **Authentication** | Spring Security with BCrypt password hashing, session management |
| 💬 **AI Chat** | Real-time chat powered by Google Gemini API with fallback responses |
| 🔔 **Reminders** | Create, manage, complete, and delete reminders |
| 📊 **Dashboard** | Stats overview with recent chats and upcoming reminders |
| 🎤 **Speech** | Speech-to-text and text-to-speech capabilities |
| 🌐 **Task Execution** | Open websites and launch applications via natural language |
| 📝 **Memory** | Persistent conversation history |
| 🎨 **Modern UI** | Dark theme with glassmorphism, gradients, and micro-animations |

---

## 🏗️ Tech Stack

### Backend (Spring Boot)
- **Java 21** + **Spring Boot 3.5**
- Spring Security (form login + BCrypt)
- Spring Data JPA + Hibernate
- Thymeleaf + Bootstrap 5
- MySQL 8.0
- Spring Boot Actuator
- JJWT 0.12.6

### AI Engine (Python)
- Flask 3.x REST API
- Google Generative AI (Gemini 2.0)
- SpeechRecognition + pyttsx3
- Memory persistence (JSON)

---

## 📁 Project Structure

```
alj/
├── src/main/java/com/example/alj/
│   ├── AljApplication.java          # Entry point
│   ├── config/
│   │   └── DataInitializer.java     # Default admin user
│   ├── controller/
│   │   ├── AuthController.java      # Login & registration
│   │   ├── ChatController.java      # Chat page & API
│   │   ├── DashboardController.java # Dashboard
│   │   └── ReminderController.java  # Reminders page & API
│   ├── dto/
│   │   ├── ChatRequestDto.java
│   │   ├── ChatResponseDto.java
│   │   ├── ReminderDto.java
│   │   └── UserRegistrationDto.java
│   ├── entity/
│   │   ├── ChatHistory.java
│   │   ├── Reminder.java
│   │   ├── ReminderStatus.java
│   │   ├── Role.java
│   │   └── User.java
│   ├── repository/
│   │   ├── ChatHistoryRepository.java
│   │   ├── ReminderRepository.java
│   │   └── UserRepository.java
│   ├── security/
│   │   ├── CustomUserDetailsService.java
│   │   └── SecurityConfig.java
│   └── service/
│       ├── ChatService.java
│       ├── ReminderService.java
│       └── UserService.java
├── src/main/resources/
│   ├── application.properties
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/
│   │       ├── chat.js
│   │       └── reminders.js
│   └── templates/
│       ├── chat.html
│       ├── dashboard.html
│       ├── login.html
│       ├── register.html
│       └── reminders.html
└── ai-engine/
    ├── main.py                      # Flask server
    ├── chatbot.py                   # Gemini AI integration
    ├── speech_engine.py             # TTS & STT
    ├── task_executor.py             # Open websites/apps
    ├── memory_manager.py            # Conversation persistence
    └── requirements.txt
```

---

## 🚀 Quick Start

### Prerequisites
- Java 21+
- MySQL 8.0+
- Python 3.11+
- Maven (included via `mvnw`)

### 1. Create MySQL Database
```sql
CREATE DATABASE jarvis_db;
```

### 2. Start Spring Boot
```bash
cd alj
.\mvnw.cmd spring-boot:run
```
Access at: **http://localhost:8080**

**Default admin account:**
- Username: `admin`
- Password: `admin123`

### 3. Start Python AI Engine (optional)
```bash
cd ai-engine
pip install -r requirements.txt
set GEMINI_API_KEY=your_api_key_here
python main.py
```
AI Engine runs at: **http://localhost:5000**

---

## 📡 API Endpoints

### Spring Boot (port 8080)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/login` | Login page |
| GET | `/register` | Registration page |
| GET | `/dashboard` | Dashboard |
| GET | `/chat` | Chat page |
| POST | `/api/chat` | Send chat message (AJAX) |
| GET | `/api/chat/history` | Get chat history (AJAX) |
| GET | `/reminders` | Reminders page |
| POST | `/api/reminders` | Create reminder (AJAX) |
| PUT | `/api/reminders/{id}/status` | Update status (AJAX) |
| DELETE | `/api/reminders/{id}` | Delete reminder (AJAX) |

### Python AI Engine (port 5000)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/chat` | AI chat response |
| POST | `/api/speech/tts` | Text-to-speech |
| POST | `/api/speech/stt` | Speech-to-text |
| POST | `/api/tasks` | Execute system task |
| GET | `/api/memory/history` | Conversation history |

---

## 📄 License

This project is for educational and personal use.
