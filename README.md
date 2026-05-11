Inventory Shop System API

A FastAPI backend for a simple RPG-style shop system with player stats, buying, and inventory tracking.

How to run it?

pip install fastapi uvicorn
uvicorn api:app --reload

## EndPoints

- GET /player
- POST /buy
- GET /inventory

Example Request
POST /buy
{
	"itemName": "sword",
	"quantity": 2
}

This project demonstrates backend API design, state management, and basic game logic using FastAPI.