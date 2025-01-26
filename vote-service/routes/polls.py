from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import get_db
from models import Poll, Option, UserOption, User
from schemas import PollCreate, PollResponse, OptionCreate, Vote, PollListResponse
from utils.security import get_current_user

router = APIRouter()

@router.post("/", response_model=PollResponse)
def create_poll(
    poll: PollCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Создаем опрос
        new_poll = Poll(
            title=poll.title,
            description=poll.description,
            owner_id=current_user.id
        )
        db.add(new_poll)
        db.flush()
        
        # Создаем варианты ответов
        for option in poll.options:
            new_option = Option(
                text=option.text,
                poll_id=new_poll.id
            )
            db.add(new_option)
        
        db.commit()
        db.refresh(new_poll)
        return new_poll
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error creating poll: {str(e)}"
        )


@router.delete("/{poll_id}")
def delete_poll(
    poll_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Находим опрос по ID
    poll = db.query(Poll).filter(Poll.id == poll_id).first()
    
    # Если опрос не найден
    if not poll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Poll not found"
        )
    
    # Проверяем, является ли текущий пользователь владельцем опроса
    if poll.owner_id != current_user.id:
        print("poll.owner_id = ", poll.owner_id)
        print("current_user.id = ", current_user.id)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the owner of this poll"
        )
    
    db.delete(poll)
    db.commit()
    
    return {"message": "Poll deleted successfully"}


@router.post("/{poll_id}/vote")
def vote(
    poll_id: int,
    vote: Vote,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Проверяем, существует ли опрос
    poll = db.query(Poll).filter(Poll.id == poll_id).first()
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")

    # Проверяем, существует ли вариант ответа в этом опросе
    option = db.query(Option).filter(
        Option.id == vote.option_id,
        Option.poll_id == poll_id
    ).first()
    
    if not option:
        raise HTTPException(status_code=404, detail="Option not found")

    # Проверяем, голосовал ли пользователь в этом опросе ранее
    existing_vote = db.query(UserOption).filter(
        UserOption.user_id == current_user.id,
        UserOption.poll_id == poll_id
    ).first()
    
    if existing_vote:
        raise HTTPException(
            status_code=400,
            detail="You have already voted in this poll"
        )

    # Создаем запись о голосовании
    new_vote = UserOption(
        user_id=current_user.id,
        option_id=vote.option_id,
        poll_id=poll_id
    )
    db.add(new_vote)
    db.commit()
    
    return {"message": "Vote recorded successfully"}



@router.get("/", response_model=list[PollListResponse])
def get_polls(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    # Запрос для получения опросов с количеством голосов
    polls_with_votes = db.query(
        Poll.id,
        Poll.title,
        Poll.description,
        func.count(UserOption.user_id).label("votes_count")
    ).outerjoin(
        UserOption, Poll.id == UserOption.poll_id
    ).group_by(
        Poll.id  # Группируем по опросам
    ).offset(skip).limit(limit).all()

    # Преобразуем результат в список словарей
    result = [
        {
            "id": poll.id,
            "title": poll.title,
            "description": poll.description,
            "votes_count": poll.votes_count
        }
        for poll in polls_with_votes
    ]

    return result