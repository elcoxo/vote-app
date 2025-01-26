from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Post, User, Poll
from schemas import PostCreate, PostResponse
from utils.security import get_current_user

router = APIRouter()

@router.post("/", response_model=PostResponse)
def create_post(
    post: PostCreate,
    poll_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    poll = db.query(Poll).filter(Poll.id == poll_id).first()
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    
    new_post = Post(
        content=post.content,
        user_id=current_user.id,
        poll_id=poll_id,
        tonality=post.tonality
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{poll_id}", response_model=list[PostResponse])
def get_posts_by_poll(
    poll_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return db.query(Post).filter(Post.poll_id == poll_id).offset(skip).limit(limit).all()