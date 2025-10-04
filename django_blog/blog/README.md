## 📝 Blog Post Management

This Django app enables full CRUD functionality for blog posts.

### Features
- Create, read, update, and delete posts.
- Only authors can edit or delete their own posts.
- List and detail views are publicly accessible.
- Built using class-based views and Django ModelForms.

### Key Files
- `blog/models.py` → Post model
- `blog/forms.py` → Post form
- `blog/views.py` → CRUD class-based views
- `blog/urls.py` → URL patterns
- `templates/blog/` → HTML templates

### Usage
Run the server and visit `/posts/` to view all posts.
Authenticated users can add posts at `/posts/new/`.
