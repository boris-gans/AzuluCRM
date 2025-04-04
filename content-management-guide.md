https://github.com/Torteous44/AzuluCRM.git# Content Management Guide

## Overview

This guide explains how to use the content management endpoints to manage dynamic content in your application, including the moving banner on the homepage.

## Content API Endpoints

The content API provides a flexible key-value storage system where each content item has:
- A unique `key` identifier
- Optional `string_collection` (array of strings)
- Optional `big_string` (large text content)

### Authentication

All write operations (POST, PUT, DELETE) require authentication using the admin password:

```
X-Admin-Password: your_admin_password
```

### Endpoints

#### 1. Create Content

**POST /content/**

Create a new content item with a unique key.

Request body:
```json
{
  "key": "content_key_name",
  "string_collection": ["Item 1", "Item 2", "Item 3"],
  "big_string": "Optional large text content"
}
```

Example (Creating a moving banner):
```json
{
  "key": "movingBanner",
  "string_collection": [
    "MARCH 28 2025",
    "AZULU IS BACK",
    "AMSTERDAM"
  ]
}
```

Response: The created content object with an ID.

#### 2. Get All Content

**GET /content/**

Retrieve all content items. Useful for admin dashboards.

Query parameters:
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100)

Response: Array of all content objects.

#### 3. Get Content by Key

**GET /content/{key}**

Retrieve a specific content item by its key.

Example: `GET /content/movingBanner`

Response: The content object with the specified key.

#### 4. Update Content

**PUT /content/{key}**

Update an existing content item. You only need to include the fields you want to update.

Request body:
```json
{
  "string_collection": ["New Item 1", "New Item 2"],
  "big_string": "Updated text content"
}
```

Example (Updating the moving banner):
```json
{
  "string_collection": [
    "MARCH 28 2025",
    "AZULU IS BACK",
    "AMSTERDAM",
    "NEW LOCATION ANNOUNCED SOON"
  ]
}
```

Response: The updated content object.

#### 5. Delete Content

**DELETE /content/{key}**

Delete a content item by its key.

Response: No content (204 status code)

## Common Use Cases

### Managing the Moving Banner

The moving banner on the homepage uses a content item with a string collection. Each string in the collection will be displayed as a separate item in the rotating banner.

1. **Create the banner** (first time setup):
   ```
   POST /content/
   
   {
     "key": "movingBanner",
     "string_collection": [
       "MARCH 28 2025",
       "AZULU IS BACK",
       "AMSTERDAM"
     ]
   }
   ```

2. **Update the banner** (change existing items):
   ```
   PUT /content/movingBanner
   
   {
     "string_collection": [
       "MARCH 28 2025",
       "AZULU IS BACK",
       "AMSTERDAM",
       "TICKETS ON SALE NOW"
     ]
   }
   ```

3. **Retrieve the banner content** (for display):
   ```
   GET /content/movingBanner
   ```

### Managing FAQ Content

FAQs can be stored as alternating questions and answers in a string collection:

```json
{
  "key": "faq",
  "string_collection": [
    "Question 1?", 
    "Answer 1", 
    "Question 2?", 
    "Answer 2"
  ]
}
```

## API Request Examples

### Using cURL

```bash
# Create content
curl -X POST https://yourdomain.com/content/ \
  -H "Content-Type: application/json" \
  -H "X-Admin-Password: your_admin_password" \
  -d '{"key":"movingBanner","string_collection":["MARCH 28 2025","AZULU IS BACK","AMSTERDAM"]}'

# Get content
curl https://yourdomain.com/content/movingBanner

# Update content
curl -X PUT https://yourdomain.com/content/movingBanner \
  -H "Content-Type: application/json" \
  -H "X-Admin-Password: your_admin_password" \
  -d '{"string_collection":["MARCH 28 2025","AZULU IS BACK","AMSTERDAM","TICKETS ON SALE NOW"]}'
```

### Using JavaScript (Fetch API)

```javascript
// Create content
async function createBanner() {
  const response = await fetch('https://yourdomain.com/content/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Admin-Password': 'your_admin_password'
    },
    body: JSON.stringify({
      key: 'movingBanner',
      string_collection: ['MARCH 28 2025', 'AZULU IS BACK', 'AMSTERDAM']
    })
  });
  return response.json();
}

// Get content
async function getBanner() {
  const response = await fetch('https://yourdomain.com/content/movingBanner');
  return response.json();
}

// Update content
async function updateBanner() {
  const response = await fetch('https://yourdomain.com/content/movingBanner', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'X-Admin-Password': 'your_admin_password'
    },
    body: JSON.stringify({
      string_collection: ['MARCH 28 2025', 'AZULU IS BACK', 'AMSTERDAM', 'TICKETS ON SALE NOW']
    })
  });
  return response.json();
}
```

## Mailing List Feature

The API includes endpoints for managing a mailing list. Users can subscribe to the mailing list, while admins can view and manage the list.

### Public Endpoints

These endpoints are accessible without authentication:

#### 1. Subscribe to Mailing List

**POST /mailing-list/subscribe**

Add a user to the mailing list.

Request body:
```json
{
  "name": "John Doe",
  "email": "john.doe@example.com"
}
```

Response: The created mailing list entry with subscription status.

#### 2. Unsubscribe from Mailing List

**GET /mailing-list/unsubscribe/{email}**

Allow a user to unsubscribe from the mailing list.

Example: `GET /mailing-list/unsubscribe/john.doe@example.com`

Response:
```json
{
  "message": "Successfully unsubscribed"
}
```

### Admin Endpoints

These endpoints require admin authentication:

#### 1. Get All Mailing List Entries

**GET /mailing-list/**

Retrieve all mailing list entries.

Query parameters:
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100)
- `subscribed_only`: Only show active subscribers (default: true)

Example: `GET /mailing-list/?subscribed_only=false`

Response: Array of mailing list entries.

#### 2. Get Specific Mailing List Entry

**GET /mailing-list/{entry_id}**

Retrieve a specific mailing list entry by ID.

Example: `GET /mailing-list/1`

Response: The mailing list entry with the specified ID.

#### 3. Delete Mailing List Entry

**DELETE /mailing-list/{entry_id}**

Delete a mailing list entry by ID.

Example: `DELETE /mailing-list/1`

Response: No content (204 status code)

### API Request Examples

#### Using cURL

```bash
# Subscribe to mailing list
curl -X POST https://yourdomain.com/mailing-list/subscribe \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john.doe@example.com"}'

# Unsubscribe from mailing list
curl https://yourdomain.com/mailing-list/unsubscribe/john.doe@example.com

# Get all mailing list entries (admin)
curl https://yourdomain.com/mailing-list/ \
  -H "X-Admin-Password: your_admin_password"
```

#### Using JavaScript (Fetch API)

```javascript
// Subscribe to mailing list
async function subscribeToMailingList(name, email) {
  const response = await fetch('https://yourdomain.com/mailing-list/subscribe', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      name: name,
      email: email
    })
  });
  return response.json();
}

// Unsubscribe from mailing list
async function unsubscribeFromMailingList(email) {
  const response = await fetch(`https://yourdomain.com/mailing-list/unsubscribe/${email}`);
  return response.json();
}

// Get all mailing list entries (admin)
async function getMailingList() {
  const response = await fetch('https://yourdomain.com/mailing-list/', {
    headers: {
      'X-Admin-Password': 'your_admin_password'
    }
  });
  return response.json();
}
```

### Frontend Implementation Example

Here's a simple form to collect email subscriptions:

```html
<form id="subscribe-form">
  <h3>Subscribe to our newsletter</h3>
  <div>
    <label for="name">Name:</label>
    <input type="text" id="name" name="name" required>
  </div>
  <div>
    <label for="email">Email:</label>
    <input type="email" id="email" name="email" required>
  </div>
  <button type="submit">Subscribe</button>
  <div id="result-message"></div>
</form>

<script>
  const form = document.getElementById('subscribe-form');
  const resultMessage = document.getElementById('result-message');
  
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    
    try {
      const response = await fetch('https://yourdomain.com/mailing-list/subscribe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, email })
      });
      
      const result = await response.json();
      
      if (response.ok) {
        resultMessage.textContent = 'Thank you for subscribing!';
        form.reset();
      } else {
        resultMessage.textContent = `Error: ${result.detail || 'Something went wrong'}`;
      }
    } catch (error) {
      resultMessage.textContent = 'Error: Unable to connect to the server';
      console.error(error);
    }
  });
</script>
``` 