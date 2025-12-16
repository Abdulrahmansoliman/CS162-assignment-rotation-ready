# Frontend - Rotation Ready

React + Vite application for the Rotation Ready platform, helping Minerva University students manage and share rotation city items.

## Frontend Responsibilities

The frontend is responsible for:

- **Rendering user and item data from backend APIs** - Fetches and displays categories, items, tags, and user information
- **Handling authentication state and protected routes** - Manages JWT tokens, login/logout flows, and route access control
- **Managing user interactions** - Add item forms, verify item actions, profile navigation, and search/filter functionality
- **Providing responsive and accessible UI components** - Mobile-first design with Radix UI primitives for accessibility

## Quick Start

```bash
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

## Features

- JWT-based authentication (login, signup, email verification)
- Browse items by category and rotation city
- Add/edit items with tags and custom attributes
- User profiles with profile pictures
- Search and filter items
- Responsive design (mobile-first)
- Item verification system

## Tech Stack

- **React 19.2.0** - UI framework
- **Vite** - Build tool & dev server (HMR, fast refresh)
- **React Router 7.9.6** - Client-side routing with protected routes
- **Tailwind CSS** - Utility-first styling
- **Radix UI** - Accessible component primitives
- **Vitest + Testing Library** - Testing framework
- **Lucide React** - Icon library

## Project Structure

```
src/
├── api/              # API clients (category, item, user, etc.)
├── features/         # Feature modules
│   ├── auth/         # Login, signup, verification
│   ├── home/         # Homepage
│   ├── addItem/      # Add/edit items
│   ├── profile/      # User profile
│   └── ...
├── routes/           # Route definitions
├── shared/           # Shared components & hooks
├── store/            # State management (auth)
└── lib/              # Utilities
```

## Development

### Available Scripts

```bash
npm run dev            # Start dev server
npm run build          # Build for production
npm run preview        # Preview production build
npm run lint           # Run ESLint
npm test              # Run tests
npm run test:coverage  # Tests with coverage
```

### API Integration

Backend API is proxied through Vite:
- API calls to `/api/*` → `http://localhost:5000`
- Configure in `vite.config.js`

All API calls use centralized `apiFetch` from `src/api/index.js`:

```javascript
import { apiFetch } from '@/api'
const items = await apiFetch('/item/', { method: 'GET' })
```

### Path Aliases

Use `@` for imports:
```javascript
import Component from '@/shared/components/Component'
```

## Testing

```bash
npm test                      # Run all tests
npm run test:coverage         # With coverage report
npm run test:feature:auth     # Test specific feature
```

Tests use Vitest + React Testing Library. See `tests/` for examples.

## Configuration

### Environment Setup

The backend must be running at `http://localhost:5000` for the frontend to work properly.

**Vite Proxy** (`vite.config.js`):
```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:5000',
      changeOrigin: true,
      secure: false,
    }
  }
}
```

### Key Files

- **Vite:** `vite.config.js` - Dev server, proxy, build config
- **Tailwind:** `tailwind.config.js` - Custom styling config
- **Tests:** `tests/setup.js` - Test environment setup
- **Router:** `src/routes/AppRouter.jsx` - Route definitions

## Authentication

### How It Works

1. User logs in → receives JWT access + refresh tokens
2. Tokens stored in `authStore` (Zustand)
3. `apiFetch` automatically includes token in headers
4. On 401 (expired token) → auto-refresh → retry request
5. On refresh failure → redirect to login

### Protected Routes

```javascript
<Route 
  path="/profile" 
  element={
    <ProtectedRoute>
      <ProfilePage />
    </ProtectedRoute>
  } 
/>
```

### Using Auth State

```javascript
import { useAuthStore } from '@/store/authStore'

const { user, token, login, logout } = useAuthStore()
const isLoggedIn = !!token
```

## Common Development Tasks

### Adding a New Page

1. Create component: `src/features/myFeature/MyPage.jsx`
2. Add route: `src/routes/AppRouter.jsx`
3. Add navigation link if needed

### Making API Calls

```javascript
// Use existing API clients
import { getItems } from '@/api/item'
const items = await getItems()

// Or use apiFetch directly
import { apiFetch } from '@/api'
const data = await apiFetch('/endpoint/', { 
  method: 'POST',
  body: JSON.stringify({ key: 'value' })
})
```

### Styling Components

```jsx
// Tailwind utility classes
<button className="px-4 py-2 bg-blue-500 hover:bg-blue-600 rounded">
  Click me
</button>

// Conditional classes with cn()
import { cn } from '@/lib/utils'
<div className={cn(
  "base-class",
  isActive && "active-class",
  disabled && "opacity-50 cursor-not-allowed"
)} />
```

## Troubleshooting

### Port Already in Use

```bash
# Kill process on port 5173
lsof -i :5173
kill -9 <PID>

# Or use different port
npm run dev -- --port 3000
```

### API Connection Failed

**Check backend is running:**
```bash
curl http://localhost:5000/api/v1/category/
```

If not running, start backend:
```bash
cd ../backend
python run.py
```

### Import Errors

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Tests Failing

```bash
# Update test snapshots
npm test -- -u

# Run specific test file
npm test LoginPage.test.jsx
```

## Deployment

Build for production:
```bash
npm run build  # Creates dist/ folder
```

Configured for Vercel deployment (see `vercel.json`).

## Code Quality

### Linting

```bash
npm run lint
```
## Contributing

1. Create feature branch: `git checkout -b feature/my-feature`
2. Make changes and test: `npm test`
3. Lint code: `npm run lint`
4. Commit: `git commit -m "Add feature"`
5. Push and create PR

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
## Resources

- [Backend README](../backend/README.md) - API setup and endpoints
- [Project Wiki](https://github.com/Abdulrahmansoliman/CS162-assignment-rotation-ready/wiki) - Comprehensive documentation
- [API Documentation](https://github.com/Abdulrahmansoliman/CS162-assignment-rotation-ready/wiki/API-Documentation) - Full API reference
- [Vite Documentation](https://vitejs.dev/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Radix UI](https://www.radix-ui.com/)

## License

This project is part of CS162 at Minerva University.
