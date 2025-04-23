import os 
import glob
import os
app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24))  # Retrieve from environment variable or fallback to random key


__all__=[os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__) + "/*.py")]