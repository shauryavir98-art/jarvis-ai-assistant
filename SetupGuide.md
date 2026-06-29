# JARVIS AI Assistant — Setup Guide

Step-by-step instructions to set up and run the JARVIS AI Assistant on your local machine.

---

## Prerequisites

| Tool | Version | Download |
|------|---------|----------|
| Java JDK | 21+ | [Adoptium](https://adoptium.net/) |
| MySQL Server | 8.0+ | [MySQL Downloads](https://dev.mysql.com/downloads/) |
| Python | 3.11+ | [Python.org](https://www.python.org/downloads/) |
| Git | Latest | [Git Downloads](https://git-scm.com/downloads) |

---

## Step 1: MySQL Database Setup

### 1.1 Start MySQL Server

Make sure MySQL is running on `localhost:3306`.

### 1.2 Create the Database

Open MySQL CLI or MySQL Workbench:

```sql
CREATE DATABASE jarvis_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 1.3 Verify Connection

```sql
USE jarvis_db;
SHOW TABLES;
```

Tables will be auto-created by Hibernate when Spring Boot starts (`ddl-auto=update`).

> **Note**: The application is configured with:
> - Username: `root`
> - Password: `Shaurya@1`
> 
> Modify `src/main/resources/application.properties` if your credentials differ.

---

## Step 2: Spring Boot Application

### 2.1 Navigate to Project Root

```bash
cd d:\AI PROTO\alj\alj
```

### 2.2 Compile the Project

```bash
.\mvnw.cmd clean compile
```

### 2.3 Run the Application

```bash
.\mvnw.cmd spring-boot:run
```

### 2.4 Access the Application

Open your browser and navigate to:

```
http://localhost:8080
```

### 2.5 Default Login

| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | `admin123` |

This admin user is automatically created on first startup by `DataInitializer`.

---

## Step 3: Python AI Engine (Optional)

The Spring Boot app works without the AI engine — it provides fallback responses. For full AI capabilities:

### 3.1 Navigate to AI Engine Directory

```bash
cd d:\AI PROTO\alj\alj\ai-engine
```

### 3.2 Create Virtual Environment (Recommended)

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3.3 Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note**: PyAudio may require additional setup on Windows. If `pip install PyAudio` fails:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

### 3.4 Configure Gemini API Key

Get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey):

```bash
set GEMINI_API_KEY=your_api_key_here
```

### 3.5 Run the AI Engine

```bash
python main.py
```

AI Engine will start on `http://localhost:5000`.

### 3.6 Verify AI Engine

```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{"status": "online", "engine": "JARVIS AI Engine", "version": "1.0.0"}
```

---

## Step 4: Verify Everything Works

### Checklist

- [ ] MySQL running on `localhost:3306`
- [ ] Database `jarvis_db` created
- [ ] Spring Boot running on `http://localhost:8080`
- [ ] Can login with `admin` / `admin123`
- [ ] Dashboard shows stats
- [ ] Chat page loads and sends messages
- [ ] Reminders page loads and creates reminders
- [ ] (Optional) Python AI Engine running on `http://localhost:5000`

---

## Quick Reference Commands

### MySQL
```bash
# Start MySQL (Windows service)
net start mysql

# Or via MySQL installer path
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqld.exe"

# MySQL CLI
mysql -u root -p
```

### Spring Boot
```bash
cd d:\AI PROTO\alj\alj

# Compile
.\mvnw.cmd clean compile

# Run
.\mvnw.cmd spring-boot:run

# Run tests
.\mvnw.cmd test

# Package JAR
.\mvnw.cmd clean package -DskipTests
```

### Python AI Engine
```bash
cd d:\AI PROTO\alj\alj\ai-engine

# Activate venv
.\venv\Scripts\activate

# Set API key
set GEMINI_API_KEY=your_key

# Run
python main.py
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| MySQL connection refused | Ensure MySQL is running: `net start mysql` |
| Access denied for user 'root' | Check password in `application.properties` |
| Port 8080 in use | Change `server.port` in `application.properties` |
| Python module not found | Run `pip install -r requirements.txt` |
| PyAudio install fails | Use `pipwin install pyaudio` on Windows |
| Gemini API errors | Verify `GEMINI_API_KEY` environment variable is set |
| CSRF token error on AJAX | Ensure meta tags are in the HTML `<head>` |
