🎮 Inventory Shop System API

A backend RPG simulation engine built with FastAPI, designed to demonstrate clean system architecture, service orchestration, and stateful domain modeling.

This project simulates a game backend where players can:

progress through levels
manage inventory
interact with a transactional shop
engage in combat and quests
all through a structured, layered backend system.

🧠 Core Design Philosophy

This project is intentionally built to mirror real-world backend architecture patterns:

Separation of concerns across layers
Controller as orchestration layer (no business logic)
Service layer for domain behavior
Repository layer for persistence abstraction
Dependency injection for testability and modularity

The goal is not just functionality — but maintainable system design under evolving features.

🏗 System Architecture

FastAPI (API Layer)
        ↓
Controller (Orchestration Layer)
        ↓
Service Layer (Business Logic)
        ↓
Repository Layer (Data Access)
        ↓
SQLite Database
Key Architectural Properties:
Stateless API layer
Centralized player state management
Explicit dependency injection
Modular service boundaries
Clear separation between domain logic and persistence

⚙️ Core Features

👤 Player System
Persistent player state (HP, gold, XP, level)
Progression system with XP tracking
Player lifecycle management (revive, stats)

🛒 Shop System
Item purchase & sale mechanics
Stock-controlled transactions
Service-driven pricing logic

🎒 Inventory System
Per-player persistent inventory
Dynamic item tracking
Repository-backed storage layer

⚔️ Combat System
Deterministic combat resolution engine
Win/loss outcome handling
XP reward system integrated with events

🧾 Quest System
Quest tracking per player
State-aware progression structure

🔐 Authentication & Security

JWT-based authentication system
Token generated via /login/{playerId}
Route-level authorization enforcement
Player-scoped access control (no cross-player data leakage)

📡 API Overview

Authentication
POST /login/{playerId} → Generate JWT token
Player
GET /player/{playerId} → Retrieve player stats
Shop
GET /shop → List available items
POST /buy/{playerId} → Purchase items
Inventory
GET /inventory/{playerId} → View inventory

🧱 Architecture Highlights

🎯 Controller Layer

Acts purely as an orchestrator:

coordinates services
manages flow of actions
contains no business logic
⚙️ Service Layer

Encapsulates all domain behavior:

combat resolution
shop transaction logic
event handling system

🗄 Repository Layer

Handles persistence concerns:

SQLite integration via SQLAlchemy
player + inventory storage abstraction

💡 What This Project Demonstrates

This project showcases:

Backend system design beyond CRUD APIs
Service-oriented architecture (SOA principles)
Dependency injection patterns in Python
State-driven application modeling
Separation of domain logic vs orchestration
Real-world backend structuring habits

🛠 Tech Stack
FastAPI
Python
SQLite
SQLAlchemy
JWT (python-jose)

🚀 Summary

This project is a modular backend game engine, designed to demonstrate how complex stateful systems can be structured cleanly using layered architecture principles.