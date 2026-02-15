# File_Integrity_Checker
# 🛡️ Linux File Integrity Monitoring Daemon

A Linux-based File Integrity Monitoring (FIM) tool built in Python that detects unauthorized file modifications, metadata tampering, file replacement attacks, and structural changes in real time. The monitor runs as a background systemd user service and provides instant desktop alerts when integrity violations are detected.

---

## 📌 Overview

This project implements a lightweight integrity monitoring daemon that:

- Establishes a trusted baseline of files
- Continuously monitors for changes
- Detects both content and metadata tampering
- Runs automatically in the background
- Sends real-time desktop notifications on detection

The tool is inspired by the fundamental concepts used in professional integrity monitoring systems such as Tripwire and AIDE.

---

## 🔐 Security Features

The monitor validates:

- SHA-256 file hash (content integrity)
- File size
- Modification time (mtime)
- File permissions
- User ID (UID)
- Group ID (GID)
- Inode number (detects delete–recreate attacks)

### Why Inode Tracking Matters

If an attacker deletes a file and recreates it with identical content, the hash may remain the same — but the inode will change. This tool detects that scenario.

---

## ⚙️ How It Works

### 1️⃣ Initialization Mode

Creates a trusted baseline:

```
python checker.py init
```

This generates:

- `baseline.json` → stores file metadata and hashes
- `Signature.json` → stores SHA-256 signature of the baseline for tamper detection

---

### 2️⃣ Monitoring Mode

When run without arguments, the program:

- Verifies baseline integrity
- Continuously monitors target directories
- Alerts on:
  - File modification
  - File deletion
  - New file creation
  - Permission changes
  - Ownership changes
  - File replacement

The monitor is deployed as a **systemd user service**, allowing it to:

- Start automatically at login
- Restart automatically if it crashes
- Run silently in the background
- Display desktop pop-up alerts

---

## 🖥️ System Integration

This project integrates with:

- Linux file system metadata (stat structure)
- systemd user services
- Desktop notification system (notify-send)
- Linux permission model

The service is managed using:

```
systemctl --user start integrity-monitor.service
systemctl --user enable integrity-monitor.service
systemctl --user status integrity-monitor.service
```

---

## 📂 Project Structure

```
file-integrity-monitor/
│
├── src/
│   └── checker.py
│
├── systemd/
│   └── integrity-monitor.service
│
├── README.md
├── requirements.txt
└── .gitignore
```

> `baseline.json` and `Signature.json` are generated at runtime and excluded via `.gitignore`.

---

## 🧠 Design Considerations

- Uses cryptographic hashing (SHA-256) for content validation
- Separates initialization and monitoring modes
- Protects baseline integrity using signature validation
- Detects both persistent tampering and structural replacement
- Designed to run with minimal CPU overhead
- Structured for future upgrade to event-driven monitoring (inotify)

---

## 🚀 Future Enhancements

- Event-driven monitoring using inotify
- Configurable target directories
- Logging system with severity levels
- Ignore rules and exclusions
- Centralized logging
- HMAC-based baseline protection

---

## 📈 Learning Outcomes

This project demonstrates practical understanding of:

- Linux file system internals
- Inode behavior and delete–recreate attack detection
- File metadata validation
- Background service management with systemd
- Desktop notification integration
- Integrity verification architecture
- Threat modeling for host-based monitoring

---

## 👨‍💻 Author

Adhyan Raghav  
Cybersecurity Enthusiast  
GitHub: https://github.com/AdhyanRaghav

---

> This project is intended for educational and defensive security research purposes.
