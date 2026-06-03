from dotenv import load_dotenv
import  os

load_dotenv()

class settings:
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

settings = settings()    