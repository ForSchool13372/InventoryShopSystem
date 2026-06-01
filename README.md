# Inventory Shop System (Full-Stack)

[![Codecov](https://codecov.io/gh/ForSchool13372/InventoryShopSystem/branch/main/graph/badge.svg)](https://codecov.io/gh/ForSchool13372/InventoryShopSystem)
[![Tests](https://img.shields.io/badge/tests-pytest-green)]()
[![Backend](https://img.shields.io/badge/backend-FastAPI-009688)]()
[![Frontend](https://img.shields.io/badge/frontend-React-61DAFB)]()

A full-stack RPG simulation system featuring authentication, shop economy, combat logic, and a **service-layer backend architecture with CI/CD, testing, and production-style design patterns**.

---

## 🎮 Live Demo

Real-time gameplay simulation with shop transactions, inventory updates, and player progression.

![Demo](assets/demo.gif)

---

## 🧠 Core Design Philosophy

This project is designed to reflect **production-style backend engineering practices**, not just feature implementation.

Key principles:
- Clear separation between frontend and backend systems
- Stateless REST API design with token-based authentication
- Server-authoritative game state (no client-side trust)
- Modular service-layer architecture for business logic isolation
- Dependency injection for authentication and validation
- Fully testable and deterministic backend logic

The goal is to simulate real-world backend system design patterns used in production applications.

---

## 🏗 System Architecture

React Frontend → FastAPI Routes → Service Layer (Game Logic) → SQLite Database

Key properties:
- Thin controller layer (FastAPI routes handle request/response only)
- Centralized business logic in service layer (`Game` domain object)
- Dependency injection for authentication and player validation
- Transaction-safe database operations via SQLAlchemy
- Stateless REST API design

---

## ⚙️ Core Features

### 👤 Player System
- Persistent player profiles (gold, HP, level, XP)
- Server-authoritative state management
- Secure authorization via dependency layer
- Real-time stat updates from backend source of truth

### 🛒 Shop System
- Dynamic item listings with stock tracking
- Buy/sell transactions with full server-side validation
- Enforced pricing and inventory rules

### 🎒 Inventory System
- Player-specific persistent inventory
- Fully backend-synced state after transactions

### ⚔️ Combat System
- Server-side combat simulation
- Deterministic outcomes (win/lose)
- XP rewards and progression system
- Event-driven state updates via service layer

### 📊 Stats System
- Live player stats from backend state
- No client-side state authority

---

## 🔐 Authentication & Security

- Token-based authentication via request headers
- Route-level authorization enforcement
- Player-scoped data access control
- Dependency injection-based validation (`getAuthorizedGame`)
- Pydantic request validation
- Rate limiting for abuse prevention

---

## 📡 API Overview

### Authentication
- `POST /login/{playerId}` → returns session token

Response:
{
  "success": true,
  "data": {
    "token": "abc123"
  }
}

---

### Player
- `GET /player/{playerId}` → get player stats

Response:
{
  "success": true,
  "data": {
    "gold": 100,
    "hp": 100,
    "level": 1,
    "xp": 0
  }
}

---

### Shop
- `GET /shop` → list items
- `POST /buy/{playerId}` → purchase item (validated)
- `POST /sell/{playerId}` → sell item (validated)

Response:
{
  "success": true,
  "data": [
    {
      "itemName": "sword",
      "stock": 5,
      "price": 20
    }
  ]
}

---

### Inventory
- `GET /inventory/{playerId}` → view inventory

---

### System
- `GET /health` → health check

---

## 🎨 Frontend (React)

### Structure
- `App.jsx` → API orchestration layer + global state
- `Login.jsx` → authentication UI
- `Shop.jsx` → shop interface
- `Inventory.jsx` → inventory management
- `PlayerStats.jsx` → live stats display

### Features
- Component-based architecture
- API-driven state updates
- Loading and error states
- Toast notifications for actions
- Dark/light mode support

---

## 🧱 Backend Architecture

### FastAPI Layer (Controllers)
- Handles routing + request validation
- Delegates all logic to service layer
- Keeps endpoints thin and maintainable

### Service Layer (Game Logic)
- Core business logic (buy/sell/combat)
- Player state updates
- Encapsulated domain rules

### Dependency Layer
- Authentication + authorization
- Player validation
- Game session resolution (`getAuthorizedGame`, `getGame`)

### Database Layer
- SQLite + SQLAlchemy
- Transaction-safe persistence
- Simple relational schema (players, inventory, shop)

---

## 🧪 Testing & Quality

- Pytest-based test suite
- Unit tests for service logic
- Integration tests for API routes
- Edge case coverage (invalid input, insufficient stock, unauthorized access)
- CI pipeline runs tests on every commit

---

## 💡 What This Project Demonstrates

- Production-style full-stack system design
- Service-layer backend architecture (controller → domain → persistence)
- Secure REST API design with authentication & authorization
- Dependency injection patterns for scalable backend design
- Test-driven development using Pytest
- CI/CD pipeline with GitHub Actions
- Real-world state management across frontend/backend
- Backend observability through structured logging

---

## 🛠 Tech Stack

- FastAPI
- Python
- React (Vite)
- JavaScript (ES6+)
- SQLAlchemy
- SQLite
- Token-based authentication
- Pytest
- GitHub Actions
- Codecov

---

## 🚀 CI/CD & Quality

- Automated testing via GitHub Actions
- Full test suite runs on every push
- Code coverage tracking via Codecov
- CI prevents broken builds from merging
- Structured logging for debugging and observability
- Rate limiting for API protection

---

## 📈 Summary

This project demonstrates a full-stack RPG simulation system built with **production-grade backend engineering principles**, including service-layer architecture, authentication and authorization design, transactional state management, automated testing, and CI/CD workflows.

It reflects real-world backend system design patterns used in scalable web applications.