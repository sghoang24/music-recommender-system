"""Execute Database."""

from sqlalchemy.orm import Session


def delete_all(db: Session, model):
    """Delete all records from a specified model/table."""
    db.query(model).delete(synchronize_session=False)
    db.commit()
