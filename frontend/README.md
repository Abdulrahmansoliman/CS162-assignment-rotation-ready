# Frontend (React + Vite)

The frontend is built with **React** and **Vite** and provides the user interface for authentication, searching, filtering, and browsing places across rotation cities.

---

## Tech Stack
- React
- Vite
- JavaScript
- CSS
- REST API integration with the backend

---

## Prerequisites
Make sure you have the following installed:
- Node.js (v18 or later recommended)
- npm

---

## Installation & Setup

### 1. Install dependencies

### 2. Start the development server

### 3. The app will start locally and typically be available at:

```bash
cd frontend
npm install
npm run dev
```

The expected URL after running the commands is: http://localhost:5173

---

## Backend Dependency 

This frontend depends on the backend being set up and running.

If the backend is not running or not reachable:
- Authentication may fail
- Data may not load
- Some pages may appear empty

Make sure the backend is configured and initialized before using the full application.

## Features & UI Overview

The frontend currently supports:
- User authentication and verification flow
- Search functionality
- Category-based browsing
- Filters such as distance, availability, operating hours, and price range
- Clean empty states when no results are available

---

## Project Structure (High Level)

```
frontend/
├── src/
│   ├── api/        # API request logic
│   ├── features/   # Feature-based UI components
│   ├── routes/     # Application routing
│   ├── shared/     # Shared components and utilities
│   └── pages/      # Page-level components
```

---

## Environment Variables

An .env.example file is provided to document required environment variables.

These variables are used to configure backend connectivity and runtime behavior.