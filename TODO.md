# TODO: Fix Bugs in FastAPI Connection Project

## Tasks to Complete
- [x] Fix schemas/connection.py: Remove duplicate imports, add StatusEnum, update IncomingConnectionRequest to use enums
- [x] Fix routes/connections.py: Move @router.post decorator to send_connection_request, remove duplicate insert code, ensure consistent UUID generation, remove unused functions, rename get_current_user

## Testing
- [x] Test POST /api/connections/request endpoint (server started, endpoint tested)
- [x] Test GET /api/connections/requests/incoming endpoint (tested via curl, returns 200 with data)
- [x] Verify database interactions align with schema (queries use gen_random_uuid() consistently)
