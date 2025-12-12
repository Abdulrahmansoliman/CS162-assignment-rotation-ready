## Team Sprint Planning - December 10, 2025

### Backend
**Categories endpoints (high priority)**
- Finish implementing category-related endpoints (e.g., get all categories, category CRUD if needed).
- Ensure category endpoints are aligned with existing tag/item implementations.
- Make sure categories are available for:
  - Add Item page
  - Main page filters

**Items endpoints**
- Implement Get All Items endpoint.
- Implement Get Item by ID endpoint.
- Ensure item schema supports:
  - name
  - location
  - walking distance
  - category
  - existing tags
  - any text fields needed for search

**Tags and values behavior**
- Confirm tag endpoints are complete (get tags, create tags, etc.).
- Support value types:
  - **Boolean**: yes/no handled on front end; no need to fetch values.
  - **Numeric**: entered directly; no need to fetch existing values.
  - **Text**: must be able to fetch existing values of a specific tag (for autocomplete/search).
- Ensure the "values of specific tag" endpoint only returns values for text tags.

**Code quality & branching**
- Resolve existing conflicts and avoid large, conflicted PRs by:
  - Creating new branches from updated main for remaining work (e.g., backend-category, backend-values).
  - Ensure new PRs are small, focused, and rebased on the latest main.

**Integration readiness**
- Verify all endpoints required by:
  - Add Item page
  - Item details page
  - Main page
- Are implemented and documented so the front end can call them without touching backend code.

### Frontend

**1. Add Item Page (existing but incomplete)**
- Review and revise the existing Add Item page based on Moustafa's upcoming comments.
- Integrate with backend:
  - Fetch categories from backend and list them.
  - Use tag endpoints and value behavior (especially text tags with selectable values).
  - Implement search/filter in tag selection as needed (e.g., searchable text values, multiple tags, etc.).
- Ensure the payload matches the backend Create Item schema:
  - name, location, walking distance, category, existing tags, any text fields.

**2. Item Page (new – Shayan)**
- Create the Item Details page using the same data model as the Add Item page:
  - Show name, location, walking distance, categories, and tags.
  - Fetch item data using: Get Item by ID endpoint.
  - Layout should roughly mirror the information used on Add Item (read-only or detail view).

**3. Main Page (new/redo – Haya)**
- Re-implement the Main Page focusing strictly on front-end concerns (no backend edits):
  - Use the Figma prototype as the visual reference.
  - Use only existing backend endpoints; do not modify backend code.
- Functionality:
  - Fetch and display all items (from Get All Items).
  - Show categories and support filtering by category.
  - Implement search bar:
    - Search by name first (name matches appear higher).
    - Then fall back / also match by text fields if defined (items with matching text appear after exact name matches).
  - (For now) skip advanced features like:
    - View details / directions buttons behavior, beyond minimal needed.
    - Pagination (not necessary yet given few items).
- Icons:
  - Use the icon set Haya previously used or icons provided in the shared folder / group.
  - If exact Figma icons aren't available, use close equivalents from your usual icon source.

**4. Tags & "Add Tag" UX**
- Implement a front-end component for creating/selecting tags:
  - User can enter:
    - tag name
    - value type (Boolean / Text / Numeric) via a dropdown.
  - For text tags, support searching/selecting existing values (backed by the "values of specific tag" endpoint).
  - For Boolean and numeric, handle directly on the front end without needing backend lookups.

**5. Coordination & Constraints**
- Frontend must:
  - Not modify backend files or logic.
  - Rely on existing endpoints and flag missing ones to backend (Abdelrahman / Hectar / Moustafa).
- Aim to:
  - Have a running prototype with:
    - Add Item
    - Item page
    - Main page
  - By the target date **Thursday**
  - Then iterate with additional features later.

---

## Backend Meeting - November 22, 2025
## Attendees
Moustafa, Abdulrahmansoliman, Hectar

# Agenda
Review current backend architecture
Discuss repository pattern implementation
Plan rotation city API endpoint

# Discussion Points
Repository Pattern Design
Reviewed repository pattern example from commit 46a0982
Current implementation uses static methods with tight coupling to ORM
Agreed this approach limits testability and violates SOLID principles
Decision: Adopt repository pattern with abstract interfaces and concrete implementations

# Architecture Agreement
Create abstract repository interfaces using Python ABC
Implement concrete repositories with SQLAlchemy
Use dependency injection in services
Enable proper unit testing with mocked dependencies
