---
title: "Introduction"
---

# Welcome to DRF SuperSet Docs

drf-superset :rocket: is a simple boilerplate for the django framework that combines top plugins and adds an endpoint for authentication as well as other utilities.


## Plugins

This is a plugin that we use on our boilerplate.

* https://github.com/django-extensions/django-extensions
* https://www.django-rest-framework.org/
* https://github.com/jazzband/django-rest-framework-simplejwt
* https://github.com/axnsan12/drf-yasg


## Features

* JWT Authentication
    * `/api/login` - end point to get access token
    * `/api/register` - end point for registering new users
    * `/api/account/confirm/{token}` - end point to verify the user account
    * `/api/forgot-password` - endpoint for requesting a password reset
    * `/api/reset-password/verify/{token}` - end point to verify password reset token
    * `/api/reset-password/{token}` - endpoint to change the user's password

* OpenAPI
* RBAC
* Utilities
    * Send an email with templates based on the `templates/email` directory
    * Fernet encryption (used for token creation)

* Commands
    * `user` - To create a new user
    * `role` - To create a user role
    * `permission` - To create permissions for a user role
