import json, asyncpg, traceback, sys


class InitDB:
    def __init__(self):
        self.pool = None
        self.config = None

    def load_config(self):
        with open('config.json', 'r') as config_file:
            return json.load(config_file)

    
    async def initialize(self):
        self.config = self.load_config()
        try:
            self.pool = await asyncpg.create_pool(
                user=self.config['db_user'], password=self.config['db_password'], database=self.config['db_name'], host=self.config['db_host']
            )
            print("Database pool initialized")
            # logging.info("Database pool initialized")
        except Exception as e:
            traceback.print_exc()
            print(f"Failed to initialize database pool: {e}")
            # logging.error(f"Failed to initialize database pool: {e}")