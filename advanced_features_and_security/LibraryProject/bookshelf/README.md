# LibraryProject Permissions & Groups

This project uses Django groups and permissions to control access to books.

## Custom Permissions
- `can_view` → View books
- `can_add` → Add books
- `can_create` → Edit books
- `can_delete` → Delete books


## User Groups
- **Admins** → All permissions
- **Editors** → View, add, edit books
- **Viewers** → Only view books

## How It Works
Permissions are enforced in views using `@permission_required`. Users must be in the appropriate group to perform actions. Unauthorized actions return a 403 error.
