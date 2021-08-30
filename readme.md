'model-view-url'
url: map request to view
view: decide what data is generated by which model, and is rendered by which template

I initial setup
1. start skeleton project
    `django-admin startproject miniblog`

2. create application & register application@settings.py
    `python3 manage.py startapp blog`

3. hook up url mapper for homepage@website/project level
    defer application-level url-mapping to applications
    define static file path for development (deploy in production will use different mechanism)

4. local run
    4.1 update migrations whenever any model changes
`python3 manage.py makemigrations`
`python3 manage.py migrate`
`python3 manage.py runserver`
now the server should be up; and homepage [http://127.0.0.1:8000/blog/](http://127.0.0.1:8000/blog/) is up but no content

II homepage
5. model design: blog, comment, blogger(based on 'User')
6. index page 

III admin pages
7. superuser to add/edit/delete model instances
    add a few blogs, bloggers for test.  

IV basic pages
8. blog list, blog detail, blogger detail
    use class-based list view and detail view to handle views.py

V login related
9. use django out-of-box authentication mechanism
10. use modelform or generic-editing-views to handle create/update/delete blogs, comments with user input.
11. 'add new comment' 
    11.1 get context from super class
    11.2 assgin blog and commenter
    11.3 validdate form
    11.4 define success url

2. how to create user/blogger from website, instead of admin page