from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from database import engine,sessionlocal
import model,schema
from auth import create_token,verify_token

app=FastAPI()

#Db dependency
def get_db():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()



model.Base.metadata.create_all(bind=engine)

#login api with token
@app.post("/login")
def login():
    return {
        "access_token":create_token({"user":"admin"}),
        "token_type":"bearer"
    }


@app.get("/")
def home():
    return {
        "message":"blog API started"
    }
    
#create Blog(protected api)

@app.post("/blogs",response_model=schema.BlogResponse)
def create_blog(blog:schema.BlogCreate,db:Session=Depends(get_db),user=Depends(verify_token)):
    new_blog=model.Blog(
        name=blog.name
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

#Read All blog

@app.get("/blogs",response_model=list[schema.BlogResponse])
def get_blogs(db:Session=Depends(get_db)):
    return db.query(model.Blog).all()

#read one blog

@app.get("/blogs/{blog_id}",response_model=schema.BlogResponse)
def get_blog(blog_id:int,db:Session=Depends(get_db)):
    blog=db.query(model.Blog).filter(blog_id==model.Blog.id).first()
    
    if not blog:
        raise HTTPException(
            status_code=404,
            detail="id not found"
        )
    
    return blog

#update blog(protected)
@app.put("/blogs/{blog_id}",response_model=schema.BlogResponse)
def update_blog(blog_id:int,blog:schema.BlogCreate,db:Session=Depends(get_db),user=Depends(verify_token)):
    existing_blog=db.query(model.Blog).filter(blog_id==model.Blog.id).first()
    
    if not blog:
        raise HTTPException(
            status_code=404,
            detail="id not in db"
        )
    existing_blog.name=blog.name
    
    db.commit()
    
    return existing_blog
    
#delete the blog(protected)
@app.delete("/blogs/{blog_id}")
def delete_blog(blog_id:int,db:Session=Depends(get_db),user=Depends(verify_token)):
    exist_blog=db.query(model.Blog).filter(model.Blog.id==blog_id).first()
    
    if not exist_blog:
        raise HTTPException(status_code=404,detail="blog not found")
    
    db.delete(exist_blog)
    db.commit()
    
    return {
        "message":"blog deleted successfully"
    }