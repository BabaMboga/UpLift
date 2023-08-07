from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Charity  

engine = create_engine('')
Session = sessionmaker(bind=engine)
session = Session()

def approve_or_delete_charity(charity_id, approve=True):
    
    charity = session.query(Charity).filter_by(charity_id=charity_id).first()
    if charity is None:
        return "Charity not found."

    elif approve:
        charity.status = True
        session.commit()
        return "Charity approved and visible to donors."
    else:
        session.delete(charity)
        session.commit()
        return "Charity deleted."

# Example Usage:

result = approve_or_delete_charity(charity_id=1, approve=True)
print(result)  
# Output: "Charity approved and visible to donors."


result = approve_or_delete_charity(charity_id=2, approve=False)
print(result) 
 # Output: "Charity deleted."
