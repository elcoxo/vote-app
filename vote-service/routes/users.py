# routes/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, Poll, Option, UserOption
from schemas import UserProfileResponse, UserVoteInfo
from utils.security import get_current_user

router = APIRouter()

@router.get("/{user_id}", response_model=UserProfileResponse)
def get_user_profile(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Проверяем, что запрашиваемый user_id совпадает с текущим пользователем
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own profile"
        )
    
    # Получаем информацию о пользователе
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Получаем список голосов пользователя с информацией о опросах и вариантах
    votes = (
        db.query(Poll.id.label("poll_id"), Poll.title.label("poll_title"), 
                 Option.id.label("option_id"), Option.text.label("option_text"))
        .join(Option, Option.poll_id == Poll.id)
        .join(UserOption, UserOption.option_id == Option.id)
        .filter(UserOption.user_id == user_id)
        .all()
    )
    
    # Преобразуем результат в список UserVoteInfo
    vote_info = [
        UserVoteInfo(
            poll_id=vote.poll_id,
            poll_title=vote.poll_title,
            option_id=vote.option_id,
            option_text=vote.option_text
        )
        for vote in votes
    ]
    
    # Формируем ответ
    return UserProfileResponse(
        username=user.username,
        email=user.email,
        votes=vote_info
    )