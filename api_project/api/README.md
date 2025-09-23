Authentication: Token-based authentication enabled using DRF.
Token endpoint: POST /api/token/ with {username, password}.
Permissions: Default is IsAuthenticated. 
To use an endpoint, include header: Authorization: Token <your_token>.