import psycopg2
import psycopg2.sql
import select
from langgraph.agents import Agent
from utils.llm_provider import get_llm_provider, query_llm
from utils.db import get_data_from_db_json, get_data_from_db_txt

class Node(Agent):
    def __init__(self, name: str, llm_provider_name: str, db_query: str, listen_channels: list, notify_channels: list):
        super().__init__(name=name)  # Initialize LangGraph's Agent with a name
        self.name = name
        self.llm_provider = get_llm_provider(llm_provider_name)  # Get the LLM provider
        self.db_query = db_query  # Query for fetching data from the database
        self.listen_channels = listen_channels  # List of channels to listen to
        self.notify_channels = notify_channels  # List of channels to notify

        # Set up database connection
        self.conn = psycopg2.connect(dsn="dbname=your_db user=your_user password=your_password host=localhost port=5432")
        self.conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.conn.cursor()

        # Subscribe to the listen channels
        self.subscribe_to_channels()

    def subscribe_to_channels(self):
        """
        Subscribes the Node to its specified channels.
        """
        for channel in self.listen_channels:
            self.cursor.execute(f"LISTEN {channel};")
            print(f"{self.name}: Listening on channel {channel}")

    def send_notification(self, channel: str, message: str):
        """
        Send a notification to a PostgreSQL channel using NOTIFY.
        """
        # Safely format the query with psycopg2.sql
        query = psycopg2.sql.SQL("NOTIFY {}, %s").format(
            psycopg2.sql.Identifier(channel)
        )
        # Execute the query
        self.cursor.execute(query, (message,))
        print(f"{self.name}: Sent notification to channel {channel} with message: {message}")

    def listen_for_notifications(self):
        """
        Continuously listens for notifications from the PostgreSQL channels.
        """
        print(f"{self.name} listening on channels: {', '.join(self.listen_channels)}")
        while True:
            # Wait for notifications from the database
            if select.select([self.conn], [], [], 5) == ([], [], []):  # Timeout to avoid blocking forever
                print(f"{self.name}: No notifications received in the last 5 seconds.")
            else:
                # Process notifications
                self.conn.poll()
                while self.conn.notifies:
                    notify = self.conn.notifies.pop(0)
                    print(f"{self.name}: Received notification: {notify.payload}")
                    self.handle_notification(notify.payload)

    def handle_notification(self, payload: str):
        """
        Handle the received notification payload.
        """
        print(f"{self.name}: Handling notification with payload: {payload}")
        state = {}  # Example state
        result = self.process(state)  # Process the data with the provided payload
        print(f"{self.name}: Processed result: {result}")








    def process(self, state: dict) -> dict:
        """
        Process the state using LLM and database queries.
        """
        # Example of calling LLM with a prompt
        prompt = "Generate a summary of the data from the database."
        llm_response = self.query_llm(prompt)

        # Fetching data from DB
        db_json_data = self.fetch_data_from_db_json()
        db_txt_data = self.fetch_data_from_db_txt()

        # Return results as a dictionary
        return {
            "llm_response": llm_response,
            "db_json_data": db_json_data,
            "db_txt_data": db_txt_data
        }

    def __call__(self, state: dict) -> dict:
        """
        Allow the object to be called like a function, triggering the process.
        """
        result = self.process(state)
        print(f"{self.name}: Processing complete")
        return result
