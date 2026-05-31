# 🎮 Inventory Shop System (Full-Stack)

[![Codecov](https://codecov.io/gh/ForSchool13372/InventoryShopSystem/branch/main/graph/badge.svg)](https://codecov.io/gh/ForSchool13372/InventoryShopSystem)
[![Tests](https://img.shields.io/badge/tests-pytest-green)]()
[![Backend](https://img.shields.io/badge/backend-FastAPI-009688)]()
[![Frontend](https://img.shields.io/badge/frontend-React-61DAFB)]()

A full-stack RPG simulation backend + frontend system with authentication, shop economy, combat logic, and automated testing + CI/CD.

---

## 🎮 Demo

![Gameplay Demo](assets/Shop.mp4)

---

## 🧠 Core Design Philosophy

This project focuses on real full-stack architecture, not just isolated features.

Key principles:
- Clear separation between frontend and backend
- Stateless REST API design with JWT authentication
- Centralized server-side game state management
- Modular service-layer architecture
- Clean and predictable data flow between systems

The goal is to simulate real production-style backend structure.

---

## 🏗 System Architecture

React Frontend → FastAPI Backend → Game Logic Layer → SQLite Database

Key properties:
- Stateless REST API design
- Token-based authentication (JWT)
- Centralized game state management
- Modular service-based architecture

---

## ⚙️ Core Features

### 👤 Player System
- Persistent player profiles (gold, HP, level, XP)
- JWT-based authentication
- Server-controlled state management

### 🛒 Shop System
- Dynamic item listings
- Buy/sell transactions with validation
- Stock-aware item handling

### 🎒 Inventory System
- Player-specific inventory
- Real-time updates after transactions
- Server-synced state

### ⚔️ Combat System
- Fight simulation system
- Win/lose outcomes
- XP reward handling
- Event-based updates

### 📊 Stats System
- Live player stats updates
- Backend-driven state source

---

## 🔐 Authentication & Security

- JWT-based authentication
- Login via `/login/{playerId}`
- Route-level authorization
- Player-scoped data access control

---

## 📡 API Overview

### Authentication
- `POST /login/{playerId}` → returns JWT token

### Player
- `GET /player/{playerId}` → player stats

### Shop
- `GET /shop` → list items
- `POST /buy/{playerId}` → purchase item
- `POST /sell/{playerId}` → sell item

### Inventory
- `GET /inventory/{playerId}` → view inventory

---

## 🎨 Frontend (React)

### Structure
- `App.jsx` → state + API orchestration layer
- `Login.jsx` → authentication UI
- `Shop.jsx` → item purchasing interface
- `Inventory.jsx` → inventory management
- `PlayerStats.jsx` → live stats display

### Features
- Component-based architecture
- API-driven state updates
- Loading states for UX feedback
- Toast notifications for actions
- Dark/light mode support

---

## 🧱 Backend Architecture

### FastAPI Layer
- Request handling & validation
- Authentication enforcement
- REST API design

### Game Logic Layer
- Handles buy/sell logic
- Player state updates
- Combat system logic

### Database Layer
- SQLite + SQLAlchemy
- Persistent player and inventory storage
- Simple relational structure

---

## 🧪 Testing & Quality

- Built comprehensive test suite using **Pytest**
- Unit tests for services
- Integration tests for API routes
- Edge case validation (invalid quantity, insufficient stock, etc.)
- CI pipeline ensures tests run on every push

---

## 💡 What This Project Demonstrates

- Full-stack system design (frontend + backend integration)
- Clean layered architecture (controller → service → data layer)
- REST API design with authentication & validation
- Test-driven development using Pytest
- CI/CD pipeline using GitHub Actions
- Code coverage tracking with Codecov

---

## 🛠 Tech Stack

- FastAPI
- Python
- React (Vite)
- JavaScript (ES6+)
- SQLAlchemy
- SQLite
- JWT Authentication
- Pytest
- GitHub Actions
- Codecov

---

## 🚀 CI/CD & Quality

- Automated testing via GitHub Actions
- Pytest suite covering services and API routes
- Code coverage reporting via Codecov
- CI prevents broken code from being merged

---

## 📈 Summary

This project demonstrates a full-stack RPG-style simulation system built with production-style software engineering practices including API design, authentication, state management, testing, and CI/CD workflows.

It reflects how real-world applications are structured across frontend and backend systems.