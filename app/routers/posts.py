from .. import models,schemas,oauth2
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List,Optional
from sqlalchemy import func

router=APIRouter(tags=['Posts'])


@router.get("/posts",response_model=List[schemas.PostOut])
def get_posts(db: Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user),limit: int = 10, skip: int = 0,search: Optional[str] = ""): 
    #Note type for current user wont matter
    # cursor.execute(""" SELECT * FROM posts """)
    # posts=cursor.fetchall()

    #posts=db.query(models.Post).filter(models.Post.owner_id==current_user.id).all() If you want all posts from current user only
    
    #SQL for this is SELECT posts.*, COUNT(votes.post_id) as votes FROM posts LEFT OUTER JOIN votes ON
    # posts.id=votes.post_id WHERE posts.id=1 GROUP BY posts.id
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id).filter(models.Post.title.contains(search))\
        .limit(limit).offset(skip).all()
    return posts

@router.get("/posts/{id}",response_model=schemas.PostOut)
def get_post(id: int, db: Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id=(%s)""",(str(id),))
    # post=cursor.fetchone()

    #post=db.query(models.Post).filter(models.Post.id==id).first()

    post=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True).\
            group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id:{id} wasn't found")

    return post

#Pydantic Model's dict method converts model to dict inplace
@router.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db: Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
    # (post.title,post.content,post.published))

    # new_post=cursor.fetchone()

    # conn.commit()

    new_post=models.Post(owner_id=current_user.id,**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post) #Acts like RETURNING

    return new_post 


@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

    # cursor.execute("""DELETE FROM posts WHERE id=(%s) RETURNING *""",(str(id),))
    # deleted_post=cursor.fetchone()

    post_query=db.query(models.Post).filter(models.Post.id == id)
    
    if not post_query.first():
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"Post with id:{id} does not exist")

    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    #conn.commit()
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT) #Since we are returning no content


@router.put("/posts/{id}",response_model=schemas.Post)
def update_post(id: int, post:schemas.PostCreate,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.published,str(id)))

    # updated_post=cursor.fetchone()

    post_query = db.query(models.Post).filter(models.Post.id == id)


    if not post_query.first():
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"Post with id:{id} does not exist")

    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="Not authorized to perform requested action")

    post_query.update(post.dict(), synchronize_session=False) #Don't unpack
    db.commit()
    updated_post=post_query.first()
    # conn.commit()

    return updated_post  