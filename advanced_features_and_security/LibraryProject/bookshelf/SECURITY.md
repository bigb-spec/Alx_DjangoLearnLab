# Security Best Practices Implemented

## Settings
- `DEBUG = False` → prevents sensitive debug info leaks.
- `SECURE_BROWSER_XSS_FILTER`, `X_FRAME_OPTIONS`, `SECURE_CONTENT_TYPE_NOSNIFF` → protect against XSS and clickjacking.
- `CSRF_COOKIE_SECURE`, `SESSION_COOKIE_SECURE` → cookies only over HTTPS.
- `SECURE_HSTS_*` → enforce HTTPS via HSTS.

## CSRF Protection
- All forms include `{% csrf_token %}`.

## SQL Injection Protection
- All queries use Django ORM (`filter`, `get`, etc.).
- Input validated via Django forms.

## Content Security Policy (CSP)
- `django-csp` middleware added.
- Only trusted domains allowed for scripts, styles, fonts.

## Testing
- Manually tested forms to confirm CSRF errors when token missing.
- Attempted XSS injection in form fields → HTML escaped by Django templates.
- Verified HTTPS cookie enforcement.