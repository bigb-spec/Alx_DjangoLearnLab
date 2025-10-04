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

## Comments System

Users may comment on posts. Features:
- Model: `Comment(post, author, content, created_at, updated_at)`
- Only authenticated users can create comments.
- Authors of comments can edit or delete their own comments.
- Comments are shown on the post detail page (oldest-first).
- Comment creation uses `add_comment` view (POST) and redirects to post detail.
- Editing/deleting comments uses `CommentUpdateView` / `CommentDeleteView` with `UserPassesTestMixin` to ensure only the author can modify.

### Usage
- Add a comment: on `/posts/<post_id>/` complete the comment form (must be logged in).
- Edit: click "Edit" next to your comment, modify and save.
- Delete: click "Delete" next to your comment and confirm.
