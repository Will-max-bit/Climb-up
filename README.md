# ClimbUp

Repo for PDX Code guild captstone

## Overview
------

ClimbUp will be a social media app focusing on sharing climbing information, scheduling meet ups and general social media features, posting, liking, etc

### Technologies used

* Django 3.1
* VueJS
* Bootstrap

## Features
------

- User System
  - [ ] User sign up form
  - [ ] User log out
  - [ ] Update profile
  - [ ] Delete Profile
- Posts
  - [ ] Create a post
  - [ ] Delete a post
  - [ ] Mark themselves as going to another users post
- [ ] Public homepage with posts from other users and the user
- [ ] Profile home page with user's posts, photos, information

## Data Model
----
* City
  * name (charfield)
* Post
  * title (charfiel)
  * text (textfield)
  * city (foreignkey to City)
  * author (foreignkey to User)
  * attendees (many-to-many with User)
  * created_date (datetimefield)
  * scheduled_date (datetimefield)
* User (extends built-in user)
  * profile picture (ImageField)

## Pages
-------
- Index
  - greeting
  - list of posts
    -likes on post
  - button for creating a new post
  - header
    - link to profile page
    - log-in link if not logged in
    - log-out link if logged in
- New Post
  - form with all the Post model fields
  - image field 
  - location field
- Post Detail
  - edit post
  - delete post
    - stretch- comment on post

## Schedule
----
* Week 1
    * create models for Posts
    * create models for Users
    * create index template and view
    * show test posts in page
    * add forms for new posts, photos & signup
    * add profile homepage with own users posts
* Week 2
    * fix issues from week 1
    * add ability to mark self on other user post
    * Update profile
    * begin styling for readability
    * edit post
    * delete post
    * like other user post
    * public page with all posts in city of User 
* Week 3
    * Fix recurring issues from weeks 1/2
    * finish any styling on app


* TinyMCE editor for post text