### Example Workflow

1. **Create a User**:
    - Endpoint: `/auth/create-user`
    - Method: `POST`
    - Body:
      ```json
      {
          "username": "your_username",
          "password": "your_password",
          "user_type": "free"  # or "premium"
      }
      ```

2. **Login to Get JWT Token**:
    - Endpoint: `/auth/login`
    - Method: `POST`
    - Body:
      ```json
      {
          "username": "your_username",
          "password": "your_password"
      }
      ```
    - Response will include `access_token` and `expires_in` (expiration time in minutes).

3. **Access Protected Endpoints**:
    - Use the obtained JWT token to access protected endpoints.
