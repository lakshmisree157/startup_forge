from fastapi import APIRouter, HTTPException, status, Query
from database import get_db_connection
from schemas.connection import ConnectionRequestCreate
from schemas.connection import IncomingConnectionRequest
from schemas.connection import Connection

router = APIRouter(prefix="/api/connections", tags=["Connections"])


@router.post("/request", status_code=status.HTTP_201_CREATED)
def send_connection_request(payload: ConnectionRequestCreate):
    sender_id = str(payload.sender_id)
    sender_role = payload.sender_role

    if sender_id == str(payload.receiver_id):
        raise HTTPException(
            status_code=400,
            detail="Cannot send connection request to yourself"
        )

    conn = get_db_connection()
    cur = conn.cursor()

    # Check duplicate pending request
    cur.execute(
        """
        SELECT 1
        FROM connection_requests
        WHERE sender_id = %s
          AND receiver_id = %s
          AND status = 'PENDING'
        """,
        (payload.sender_id, payload.receiver_id)
    )

    if cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(
            status_code=409,
            detail="Connection request already pending"
        )

    # INSERT request
    cur.execute(
        """
        INSERT INTO connection_requests (
            sender_id,
            sender_role,
            receiver_id,
            receiver_role,
            message,
            status
        )
        VALUES (
            %s, %s, %s, %s, %s, 'PENDING'
        )
        """,
        (
            payload.sender_id,
            sender_role,
            payload.receiver_id,
            payload.receiver_role,
            payload.message
        )
    )

    conn.commit()
    cur.close()
    conn.close()

    return {"status": "PENDING"}


@router.get("/requests/incoming", response_model=list[IncomingConnectionRequest])
def get_incoming_requests(user_id: int = Query(...)):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            id,
            sender_id,
            sender_role,
            message,
            status,
            created_at
        FROM connection_requests
        WHERE receiver_id = %s
          AND status = 'PENDING'
        ORDER BY created_at DESC
        """,
        (user_id,)
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        IncomingConnectionRequest(
            id=row[0],
            sender_id=row[1],
            sender_role=row[2],
            message=row[3],
            status=row[4],
            created_at=row[5]
        )
        for row in rows
    ]


@router.put("/requests/{request_id}/accept", status_code=status.HTTP_200_OK)
def accept_connection_request(request_id: int):
    conn = get_db_connection()
    cur = conn.cursor()

    # Check if request exists and is pending
    cur.execute(
        """
        SELECT sender_id, sender_role, receiver_id, receiver_role
        FROM connection_requests
        WHERE id = %s AND status = 'PENDING'
        """,
        (request_id,)
    )

    row = cur.fetchone()
    if not row:
        cur.close()
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Connection request not found or not pending"
        )

    sender_id, sender_role, receiver_id, receiver_role = row

    # Update request status to ACCEPTED and set responded_at
    cur.execute(
        """
        UPDATE connection_requests
        SET status = 'ACCEPTED', responded_at = CURRENT_TIMESTAMP
        WHERE id = %s
        """,
        (request_id,)
    )

    # Insert into connections table
    cur.execute(
        """
        INSERT INTO connections (
            user_a_id,
            user_a_role,
            user_b_id,
            user_b_role,
            connection_request_id
        )
        VALUES (
            %s, %s, %s, %s, %s
        )
        """,
        (sender_id, sender_role, receiver_id, receiver_role, request_id)
    )

    conn.commit()
    cur.close()
    conn.close()

    return {"status": "ACCEPTED"}


@router.put("/requests/{request_id}/reject", status_code=status.HTTP_200_OK)
def reject_connection_request(request_id: int):
    conn = get_db_connection()
    cur = conn.cursor()

    # Update request status to REJECTED and set responded_at
    cur.execute(
        """
        UPDATE connection_requests
        SET status = 'REJECTED', responded_at = CURRENT_TIMESTAMP
        WHERE id = %s AND status = 'PENDING'
        """,
        (request_id,)
    )

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Connection request not found or not pending"
        )

    conn.commit()
    cur.close()
    conn.close()

    return {"status": "REJECTED"}


@router.get("", response_model=list[Connection])
def get_connections(user_id: int = Query(...)):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            id,
            user_a_id,
            user_a_role,
            user_b_id,
            user_b_role,
            connection_request_id,
            created_at
        FROM connections
        WHERE user_a_id = %s OR user_b_id = %s
        ORDER BY created_at DESC
        """,
        (user_id, user_id)
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        Connection(
            id=row[0],
            user_a_id=row[1],
            user_a_role=row[2],
            user_b_id=row[3],
            user_b_role=row[4],
            connection_request_id=row[5],
            created_at=row[6]
        )
        for row in rows
    ]
