#!/bin/bash

BASE_URL="http://localhost:5000/api"

echo "1. Register a new user"
curl -X POST "${BASE_URL}/users/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser2",
    "email": "test2@example.com",
    "password": "Password123"
  }'
echo -e "\n"

echo "2. Login with the user"
curl -X POST "${BASE_URL}/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser2",
    "password": "Password123"
  }'
echo -e "\n"

# After running the login command, copy the access_token and refresh_token values
# and replace them in the commands below

echo "3. Access protected endpoint (get users list)"
# Replace ACCESS_TOKEN with the token from login response
curl -X GET "${BASE_URL}/users/" \
  -H "Authorization: Bearer ACCESS_TOKEN"
echo -e "\n"

echo "4. Refresh token"
# Replace REFRESH_TOKEN with the refresh token from login response
curl -X POST "${BASE_URL}/auth/refresh" \
  -H "Authorization: Bearer REFRESH_TOKEN"
echo -e "\n"

echo "5. Logout"
# Replace ACCESS_TOKEN with the token from login response
curl -X POST "${BASE_URL}/auth/logout" \
  -H "Authorization: Bearer ACCESS_TOKEN"
echo -e "\n"
