
from schemas import MessageBase
from db.models import DbMessage, DbAdvertisement, DbUser
from sqlalchemy import desc
from fastapi import HTTPException,status
from sqlalchemy.orm.session import Session



def send_message (db: Session, request: MessageBase, sender_id:int):
    advertisement = db.query(DbAdvertisement).filter(request.advertisement_id == DbAdvertisement.id).first()
    if not advertisement:
        raise HTTPException (
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f"Advertisement with the ID {request.advertisement_id} not found!"
        )
    if request.receiver_id == sender_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't send a message to yourself",
        )

        # 3) Receiver must exist
    receiver = db.query(DbUser).filter(DbUser.id == request.receiver_id).first()
    if not receiver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Receiver with ID {request.receiver_id} not found!",
        )

    # 4) Conversation must include the advertisement owner.
    #    - If the sender is not the owner, the receiver MUST be the owner.
    #    - If the sender is the owner, they can message the non-owner.
    owner_id = advertisement.owner_id
    if sender_id != owner_id and request.receiver_id != owner_id:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=(
                "One of sender or receiver must be the advertisement owner "
                f"(owner_id={owner_id})."
            ),
        )

    new_message= DbMessage(
        sender_id=sender_id,
        receiver_id = request.receiver_id,
        advertisement_id = request.advertisement_id,
        content = request.content,
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message



def get_conversation(db: Session, user1_id: int, user2_id: int, advertisement_id:int):
    conversation = db.query(DbMessage).filter(
        ((DbMessage.sender_id == user1_id) & (DbMessage.receiver_id == user2_id) |
         (DbMessage.sender_id == user2_id) & (DbMessage.receiver_id == user1_id)),DbMessage.advertisement_id == advertisement_id
    ).order_by(desc(DbMessage.created_at)).all()
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'A converstaion with user ID {user2_id} and the advertisement ID {advertisement_id} not found!')
    return conversation

