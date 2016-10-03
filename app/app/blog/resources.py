from flask import Blueprint, request

from flask_restful import Api, Resource
from flask_restful import abort, fields, marshal_with, reqparse

from app.blog.models import BlogPost as Post
from app.blog.forms import CreateOrUpdateBlogForm
from app.blog.services import BlogService

blog_bp = Blueprint('blog_api', __name__)
api = Api(blog_bp)

post_fields = {
    'id': fields.Integer,
    'created': fields.DateTime,
    'modified': fields.DateTime,
    'title': fields.String,
    'content': fields.String,
    'slug': fields.String,
    'published': fields.Boolean
}

list_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'slug': fields.String,
}

class BlogPostDetail(Resource):
    service = BlogService()

    @marshal_with(post_fields)
    def get(self, slug):
        """
        Returns a single blog post by slug
        ---
        definitions:
        - schema:
            id: Blog
            properties:
                id:
                  type: integer
                  description: Generated by the database
                created:
                  type: string
                  format: date-time
                  description: Set once, when the blog post has been created
                modified:
                  type: string
                  format: date-time
                  description: Set every time the blog post is modified
                title:
                  type: string
                  description: Title of the blog post
                content:
                  type: string
                  description: Content of the blog post
                slug:
                  type: string
                  description: Automatically generated based on the title
                published:
                  type: boolean
                  description: Indicates whether the blog post is published or not
        responses:
          200:
            description: Blog response
            schema:
              $ref: '#/definitions/Blog'
          404:
            description: Blog post not found
        parameters:
        - name: slug
          in: path
          description: slug of the blog post
          required: true
          type: string
        """
        post = self.service.get_by_slug(slug)

        if not post:
            abort(404, error="Post {} doesn't exist".format(slug))

        return post

    def delete(self, slug):
        """
        Delete a single blog post by slug
        ---
        responses:
          204:
            description: Blog post has been deleted
          404:
            description: Blog post not found
        parameters:
        - name: slug
          in: path
          description: slug of the blog post
          required: true
          type: string
        """
        post = self.service.get_by_slug(slug)

        if not post:
            abort(404, error="Post {} doesn't exist".format(slug))

        self.service.delete(post)

        return {}, 204

    @marshal_with(post_fields)
    def put(self, slug):
        """
        Update a blog post by slug
        ---
        definitions:
        - schema:
            id: UpdateBlog
            properties:
                title:
                    type: string
                    description: title of the blog post
                content:
                    type: string
                    description: content of the blog post
        consumes:
          - application/json
        responses:
          200:
            description: Blog response
            schema:
              $ref: '#/definitions/Blog'
          404:
            description: Blog post not found
          400:
            description: Input is invalid
        parameters:
        - name: slug
          in: path
          description: slug of the blog post
          required: true
          type: string
        - name: post
          in: body
          required: true
          schema:
            $ref: '#/definitions/UpdateBlog'
        """
        post = self.service.get_by_slug(slug)

        if not post:
            abort(404, error="Post {} doesn't exist".format(slug))

        form = CreateOrUpdateBlogForm(data=request.get_json(force=True))

        if not form.validate():
            abort(400, errors=form.errors)

        form.populate_obj(post)
        self.service.save_update(post)

        return post, 200


class BlogPostList(Resource):
    service = BlogService()

    @marshal_with(list_fields)
    def get(self):
        """
        Returns all the blog posts
        ---
        definitions:
        - schema:
            id: BlogList
            properties:
                id:
                  type: integer
                  description: Generated by the database
                title:
                  type: string
                  description: Title of the blog post
                slug:
                  type: string
                  description: Automatically generated based on the title
        responses:
          200:
            description: Blog post list response
            schema:
              type: array
              items:
                $ref: '#/definitions/BlogList'
        """
        return self.service.get_all()

    @marshal_with(post_fields)
    def post(self):
        """
        Create a new blog post
        ---
        consumes:
          - application/json
        responses:
          201:
            description: Blog post response
            schema:
              $ref: '#/definitions/Blog'
          409:
            description: Blog post already exist
          400:
            description: Input is invalid
        parameters:
        - name: post
          in: body
          required: true
          schema:
            $ref: '#/definitions/UpdateBlog'
        """
        form = CreateOrUpdateBlogForm(data=request.get_json(force=True))

        if not form.validate():
            abort(400, errors=form.errors)

        post = Post(title=form.title.data, content=form.content.data)

        existing_post = self.service.get_by_title(post.title)
        if existing_post:
            abort(409, error="Post {} already exist".format(post.title))

        self.service.save_update(post)

        return post, 201

api.add_resource(BlogPostDetail, '/<string:slug>')
api.add_resource(BlogPostList, '/')
