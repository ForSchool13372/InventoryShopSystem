🎮 Inventory Shop System API

A FastAPI backend for a lightweight RPG-style shop system featuring player stats, inventory management, and transactional item buying.

🚀 Features
Player state tracking (gold, HP, level, XP)
Item shop with buy functionality
Inventory management system
Structured backend architecture using service-based design
Persistent storage using SQLite (SQLAlchemy)

▶️ How to Run
pip install fastapi uvicorn sqlalchemy
uvicorn api:app --reload

📡 API Endpoints
GET /player

Returns current player stats.

GET /inventory

Returns player inventory items.

GET /shop

Returns available shop items and stock.

POST /buy

Purchase items from the shop.

Example Request:
{
  "itemName": "sword",
  "quantity": 2
}

🧠 Design Overview

This project demonstrates:

Backend API design using FastAPI
Service-based architecture (Controller → Services → DB)
State management for player progression
Basic transactional logic for shop system

🛠 Tech Stack
FastAPI
SQLite
SQLAlchemy
Python