from models import Prisoner, db
from datetime import datetime

def generate_prisoner_id():
    # Format: YYYY-XXX where XXX is sequential
    year = datetime.utcnow().year
    prefix = str(year)
    last = Prisoner.query.filter(Prisoner.prisoner_id.startswith(prefix)).order_by(Prisoner.prisoner_id.desc()).first()
    if last:
        last_seq = int(last.prisoner_id.split('-')[1])
        new_seq = f"{last_seq + 1:03d}"
    else:
        new_seq = "001"
    return f"{prefix}-{new_seq}"