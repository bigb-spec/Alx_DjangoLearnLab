"# LibraryProject"

# Permissions & Groups Setup in Django

## Custom Permissions
- `can_view` → View books
- `can_create` → Create books
- `can_edit` → Edit books
- `can_delete` → Delete books

## Groups
- **Viewers** → [can_view]
- **Editors** → [can_view, can_create, can_edit]
- **Admins** → [can_view, can_create, can_edit, can_delete]

## Usage
- Permissions are enforced using `@permission_required` in views.
- Assign users to groups via Django Admin or using the `setup_groups()` script.
- Log in as users to confirm correct access control.
