[![codecov](https://codecov.io/gh/ForSchool13372/InventoryShopSystem/branch/main/graph/badge.svg)](https://codecov.io/gh/ForSchool13372/InventoryShopSystem)

🎮 Inventory Shop System (Full-Stack)

🎮 Inventory Shop System (Full-Stack)

A full-stack RPG-style simulation system built with FastAPI (backend) and React (frontend), designed to demonstrate real-world full-stack architecture, authentication flow, and state-driven application design.

This project simulates a lightweight game economy where players can:

log in and manage a persistent player profile
buy and sell items in a shop system
manage an inventory system
track stats like gold, HP, and level
interact with a live backend API

🧠 Core Design Philosophy

This project focuses on real full-stack architecture, not just isolated features.

Key principles:

Clear separation between frontend and backend
Stateless API design with token-based authentication
Centralized game state management on the backend
Component-based UI architecture on the frontend
Clean data flow between systems

The goal is to simulate how real production applications are structured.

🏗 System Architecture
React Frontend
    ↓ (API calls)
FastAPI Backend
    ↓
Game Factory (Domain Logic Layer)
    ↓
Database (SQLite / SQLAlchemy)
Key Properties:
Stateless REST API layer
Token-based authentication (JWT)
Server-controlled game state
Modular domain logic via GameFactory
Separation between UI, API, and business logic

⚙️ Core Features

👤 Player System
Persistent player profile (gold, HP, level)
Authentication via player ID login
Server-side state management
🛒 Shop System
Dynamic item listings
Buy transactions with validation
Stock-aware item handling
🎒 Inventory System
Player-specific inventory
Real-time updates after transactions
Server-synced state
📊 Stats System
Live player stats display
Updates after every action
Backend-driven truth source
🔐 Authentication & Security
JWT-based authentication
Login via /login/{playerId}
Route-level authorization
Player-scoped access control
Prevents cross-player data access

📡 API Overview

Authentication
POST /login/{playerId} → returns JWT token
Player
GET /player/{playerId} → player stats
Shop
GET /shop → list items
POST /buy/{playerId} → purchase item
Inventory
GET /inventory/{playerId} → view inventory
Selling
POST /sell/{playerId} → sell item

🎨 Frontend (React)

The frontend is built with a component-based architecture:

Structure:
App.jsx → state + API orchestration layer
Login.jsx → authentication UI
Shop.jsx → item purchasing interface
Inventory.jsx → item management
PlayerStats.jsx → live stats display
Frontend Features:
Component separation for scalability
API-driven state updates
Loading states for UX feedback
Per-action UI feedback (buy/sell/login)
Clean data flow via props

🧱 Backend Architecture

FastAPI Layer
Handles routing and request validation
Stateless API design
Authentication enforcement
Game Factory (Domain Layer)
Encapsulates game logic
Handles transactions (buy/sell)
Manages player state transitions
Database Layer
SQLite with SQLAlchemy
Persistent player + inventory storage
Simple relational structure

💡 What This Project Demonstrates

This project shows the ability to:

Build a working full-stack application
Connect frontend and backend systems properly
Design clean component-based architecture
Implement authentication and authorization
Manage server-driven state
Structure code like a production application (not just a tutorial)
Implemented a comprehensive automated test suite using Pytest to validate core business logic, API endpoints, and edge cases, ensuring system reliability and regression safety

🛠 Tech Stack
FastAPI
Python
React (Vite)
JavaScript (ES6+)
SQLAlchemy
SQLite
JWT Authentication

🚀 Summary

This project is a full-stack game simulation system that demonstrates practical software engineering principles, including API design, authentication, state management, and component-based frontend architecture.

It is designed to reflect how real-world applications are structured across frontend and backend systems.