# Django Prototype – Aristotle TV (First Attempt)

This folder contains the **initial prototype** of the Aristotle TV system, built using Django.

It was the first approach before switching to WordPress as the final platform, based on supervisor feedback to make the system accessible for non-programmers.

---

## Purpose

The Django version was designed to:
- Handle user registration and authentication
- Allow users to upload video/audio content
- Serve as the base for media processing and display
- Provide a customizable admin/backend panel for instructors

---

## Project Structure

- `ArUTv/` – Django project settings and root config
- `users/` – Handles authentication logic and user management
- `videoupload/` – Logic for uploading and storing media files
- `website/` – Views and templates for front-facing UI
- `Pipfile` / `Pipfile.lock` – Python environment and dependencies
- `manage.py` – Django project runner

---

## Status

This prototype was **not completed**, and development was discontinued after pivoting to WordPress.

However, it serves as a technical reference for what a custom backend solution could look like if deployed with Django.

---


## Why It Was Abandoned

After discussions with professors and users, we moved away from Django because:
- WordPress was more accessible for faculty and students without coding knowledge

---


