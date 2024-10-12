from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def name_validation(self,key,name_authors):
        if not name_authors:
            raise ValueError("name required")
        existing_author = Author.query.filter_by(name=name_authors).first()
        if existing_author:
            raise ValueError("Name already exists")
        return name_authors
     

    @validates('phone_number')
    def phone_validation(self,key,phone_authors):
        if len(phone_authors) != 10:
            raise ValueError("Incorrect phone format")
        if not phone_authors.isdigit():
            raise ValueError("Phone Number must contains only digits")
        return phone_authors


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('title')
    def title_validate(self,key,post_title):
        if not post_title:
            raise ValueError("Post must have a title")
        return post_title
    
    @validates('content')
    def content_validate(self,key,post_content):
        if len(post_content) < 250:
            raise ValueError("Content too short")
        return post_content

    @validates('summary')
    def summary_validate(self,key,post_summary):
        if len(post_summary) > 250:
            raise ValueError("Summary too long")
        return post_summary

    @validates('category')
    def category_validate(self, key, post_category):
        allowed_categories = ['Health', 'Non-Fiction', 'Entertainment']
        if post_category not in allowed_categories:
            raise ValueError("Category is not valid")
        return post_category



    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
