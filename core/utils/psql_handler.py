import psycopg2
import json
import select
from typing import Dict, List, Any, Optional, Callable
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pathlib import Path

class PSQL_Handler:
    def __init__(self, db_params: Dict[str, str], schema_dir: str = "/container_psql/schemas"):
        """
        Initialize PostgreSQL handler with connection parameters and schema directory.
        
        Args:
            db_params: Database connection parameters dictionary
            schema_dir: Directory containing SQL schema files (default: /container_psql/schemas)
        """
        # Store initialization parameters
        self.db_params = db_params
        self.schema_dir = Path(schema_dir)
        
        # Initialize connection attributes
        self.conn = None  # Main connection for data operations
        self.notify_conn = None  # Separate connection for LISTEN/NOTIFY
        
        # Establish connections
        self._connect()
        
        # Initialize database with schemas
        self._init_db()

    def _connect(self) -> None:
        """Establish main and notification connections to PostgreSQL."""
        try:
            # Create main connection for regular operations
            self.conn = psycopg2.connect(**self.db_params)
            
            # Create separate connection for LISTEN/NOTIFY with AUTOCOMMIT
            self.notify_conn = psycopg2.connect(**self.db_params)
            self.notify_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            
        except psycopg2.Error as e:
            raise Exception(f"Database connection failed: {str(e)}")

    def _init_db(self) -> None:
        """Initialize database using SQL schema files from schema directory."""
        try:
            # Get all .sql files from schema directory
            schema_files = sorted(self.schema_dir.glob("*.sql"))
            
            # Execute each schema file in order
            with self.conn.cursor() as cur:
                for schema_file in schema_files:
                    cur.execute(schema_file.read_text())
                self.conn.commit()
                
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Database initialization failed: {str(e)}")

    def store_json(self, table: str, data: Dict[str, Any], notify: bool = True) -> int:
        """
        Store JSON data in specified table and optionally notify listeners.
        
        Args:
            table: Target table name
            data: Dictionary to store as JSONB
            notify: Whether to send notification (default: True)
            
        Returns:
            int: ID of inserted record
        """
        try:
            with self.conn.cursor() as cur:
                # Insert JSON data and return ID
                cur.execute(
                    f"INSERT INTO {table} (data) VALUES (%s) RETURNING id",
                    (json.dumps(data),)
                )
                record_id = cur.fetchone()[0]
                self.conn.commit()
                
                # Send notification if requested
                if notify:
                    self.notify(f"new_{table}", {
                        'id': record_id,
                        'table': table
                    })
                    
                return record_id
                
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Failed to store JSON data: {str(e)}")

    def get_json(self, table: str, record_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve JSON data from specified table by ID.
        
        Args:
            table: Source table name
            record_id: ID of record to retrieve
            
        Returns:
            Dictionary containing JSON data or None if not found
        """
        try:
            with self.conn.cursor() as cur:
                # Query for JSON data
                cur.execute(
                    f"SELECT data FROM {table} WHERE id = %s",
                    (record_id,)
                )
                result = cur.fetchone()
                
                # Return parsed JSON if found, None otherwise
                return json.loads(result[0]) if result else None
                
        except Exception as e:
            raise Exception(f"Failed to retrieve JSON data: {str(e)}")

    def listen(self, channel: str) -> None:
        """
        Start listening on specified notification channel.
        
        Args:
            channel: Channel name to listen on
        """
        try:
            with self.notify_conn.cursor() as cur:
                cur.execute(f"LISTEN {channel}")
                
        except Exception as e:
            raise Exception(f"Failed to start listening: {str(e)}")

    def notify(self, channel: str, payload: Dict[str, Any]) -> None:
        """
        Send notification with JSON payload to specified channel.
        
        Args:
            channel: Target channel name
            payload: Dictionary to send as JSON payload
        """
        try:
            with self.notify_conn.cursor() as cur:
                cur.execute(
                    f"NOTIFY {channel}, %s",
                    (json.dumps(payload),)
                )
                
        except Exception as e:
            raise Exception(f"Failed to send notification: {str(e)}")

    def handle_notifications(self, callback: Callable[[str, Dict[str, Any]], None], timeout: float = None) -> None:
        """
        Wait for and process notifications using callback function.
        
        Args:
            callback: Function to call with (channel, payload) for each notification
            timeout: Seconds to wait (None = wait forever)
        """
        try:
            # Check for notifications
            if select.select([self.notify_conn], [], [], timeout) != ([], [], []):
                self.notify_conn.poll()
                
                # Process all pending notifications
                while self.notify_conn.notifies:
                    # Get next notification
                    notification = self.notify_conn.notifies.pop(0)
                    
                    try:
                        # Parse payload and call callback
                        payload = json.loads(notification.payload)
                        callback(notification.channel, payload)
                        
                    except json.JSONDecodeError:
                        print(f"Invalid notification payload: {notification.payload}")
                        
        except Exception as e:
            raise Exception(f"Notification handling failed: {str(e)}")

    def execute_query(self, query: str, params: tuple = None) -> List[tuple]:
        """
        Execute custom SQL query with optional parameters.
        
        Args:
            query: SQL query string
            params: Query parameters tuple (optional)
            
        Returns:
            List of result tuples
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                results = cur.fetchall() if cur.description else []
                self.conn.commit()
                return results
                
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Query execution failed: {str(e)}")

    def close(self) -> None:
        """Close all database connections."""
        if self.conn:
            self.conn.close()
        if self.notify_conn:
            self.notify_conn.close()



if name == 'main':
    # Initialize handler
    db_params = {
        'dbname': 'your_db',
        'user': 'your_user',
        'password': 'your_password',
        'host': 'localhost',
        'port': '5432'
    }
    db = PSQL_Handler(db_params)

    # Store JSON data
    data = {'key': 'value', 'nested': {'data': 'here'}}
    record_id = db.store_json('your_table', data)

    # Set up notification handling
    def handle_notification(channel: str, payload: Dict[str, Any]) -> None:
        if channel == 'new_your_table':
            data = db.get_json('your_table', payload['id'])
            # Process new data...

    # Listen for notifications
    db.listen('new_your_table')

    # Main loop
    while True:
        db.handle_notifications(handle_notification, timeout=1.0)
        # Do other work...