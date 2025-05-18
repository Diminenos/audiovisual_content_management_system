# WordPress Integration – Aristotle TV

This folder contains the custom WordPress plugin that integrates the Aristotle TV backend with the WordPress frontend using RabbitMQ.

The plugin acts as the **entry point** for video/audio processing by publishing metadata to RabbitMQ when a new post is created.

---

## What It Does

1. Listens for the creation of a new **WordPress post** of type `video`.
2. Waits for a **Forminator form** submission to get the uploaded file path.
3. Combines the `post_id` and `file_path` into a JSON message.
4. Publishes the message to RabbitMQ using PHP's AMQP library.

This triggers the backend processing pipeline (e.g., transcription, tagging, NER, etc.).

---

## Plugin Structure

- `aristotle-tv-plugin.php`:  
  Main plugin file containing:
  - Hook into `wp_insert_post`
  - Hook into `forminator_form_after_save_entry`
  - Function to publish to RabbitMQ

- `vendor/`:  
  Composer dependencies (AMQP client library, etc.)

---

## RabbitMQ Configuration

The plugin connects to RabbitMQ with:
- Host: `localhost`
- Port: `5672`
- Exchange: `algo_exchange` (type `fanout`)
- Credentials are hardcoded in the script (you may want to move these to a config file or env loader for production use).

---




