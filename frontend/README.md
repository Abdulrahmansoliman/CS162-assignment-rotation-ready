# Frontend - Rotation Ready

React + Vite application for the Rotation Ready platform, helping Minerva University students manage and share rotation city items.

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

## Known Issues

**Performance:** Category API supports `?no_images=true` parameter but frontend doesn't use it (can reduce payload by 95%)

**Missing Feature:** Backend value endpoints (`/value/tag/<id>`) not integrated - no autocomplete for tag values

**Code Quality:** Some direct API calls instead of using abstraction layer (HomePage line 64)

See [../GITHUB_ISSUES_TO_CREATE.md](../GITHUB_ISSUES_TO_CREATE.md) for details.

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

### Best Practices

**Do:**
- Use functional components with hooks
- Handle loading and error states
- Implement proper form validation
- Use semantic HTML elements
- Add ARIA labels for accessibility
- Keep components small and focused
- Extract reusable logic to custom hooks

**Don't:**
- Mutate state directly
- Forget useEffect cleanup
- Make API calls in render
- Hardcode URLs or magic numbers
- Ignore ESLint warnings

## Contributing

1. Create feature branch: `git checkout -b feature/my-feature`
2. Make changes and test: `npm test`
3. Lint code: `npm run lint`
4. Commit: `git commit -m "Add feature"`
5. Push and create PR

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
