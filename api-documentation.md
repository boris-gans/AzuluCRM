# Azulu CRM API Documentation

Base URL: [https://azulucrm.fly.dev](https://azulucrm.fly.dev)

## Authentication

Protected endpoints require an `X-Admin-Password` header with the admin password.

Example:
```
X-Admin-Password: your_admin_password
```

## Endpoints

### Root Endpoint

- **GET /** - Welcome endpoint
  - Response: `{"message":"Welcome to the Azulu CRM API"}`

### Health Check

- **GET /health** - Health check endpoint for monitoring
  - Response: `{"status":"healthy"}`

### Events

#### Get All Events

- **GET /events** - Retrieve a list of all events
  - Query Parameters:
    - `skip` (integer, optional): Number of records to skip. Default: 0
    - `limit` (integer, optional): Maximum number of records to return. Default: 100
    - `upcoming` (boolean, optional): Filter to only show upcoming events. Default: false
  - Response: Array of Event objects

#### Get Single Event

- **GET /events/{event_id}** - Retrieve a specific event by ID
  - Path Parameters:
    - `event_id` (integer): The ID of the event to retrieve
  - Response: Event object
  - Status Codes:
    - 404: Event not found

#### Create Event

- **POST /events** - Create a new event
  - Authentication Required: Yes
  - Request Body: EventCreate object
  - Response: Created Event object

#### Update Event

- **PUT /events/{event_id}** - Update an existing event
  - Authentication Required: Yes
  - Path Parameters:
    - `event_id` (integer): The ID of the event to update
  - Request Body: EventUpdate object
  - Response: Updated Event object
  - Status Codes:
    - 404: Event not found

#### Delete Event

- **DELETE /events/{event_id}** - Delete an event
  - Authentication Required: Yes
  - Path Parameters:
    - `event_id` (integer): The ID of the event to delete
  - Response: No content (204)
  - Status Codes:
    - 404: Event not found

### Content

#### Get All Content

- **GET /content** - Retrieve all content items
  - Query Parameters:
    - `skip` (integer, optional): Number of records to skip. Default: 0
    - `limit` (integer, optional): Maximum number of records to return. Default: 100
  - Response: Array of Content objects

#### Get Content By Key

- **GET /content/{key}** - Retrieve content by key
  - Path Parameters:
    - `key` (string): The key of the content to retrieve
  - Response: Content object
  - Status Codes:
    - 404: Content with key not found

#### Create Content

- **POST /content** - Create a new content item
  - Authentication Required: Yes
  - Request Body: ContentCreate object
  - Response: Created Content object
  - Status Codes:
    - 400: Content with this key already exists

#### Update Content

- **PUT /content/{key}** - Update existing content
  - Authentication Required: Yes
  - Path Parameters:
    - `key` (string): The key of the content to update
  - Request Body: ContentUpdate object
  - Response: Updated Content object
  - Status Codes:
    - 404: Content with key not found

#### Delete Content

- **DELETE /content/{key}** - Delete content
  - Authentication Required: Yes
  - Path Parameters:
    - `key` (string): The key of the content to delete
  - Response: No content (204)
  - Status Codes:
    - 404: Content with key not found

### Cloudinary

#### Get Upload Signature

- **GET /cloudinary/signature** - Get signature for direct uploads to Cloudinary
  - Authentication Required: Yes
  - Response: Cloudinary signature object with the following fields:
    - `signature`: Signature for the upload
    - `timestamp`: Current timestamp
    - `cloudName`: Cloudinary cloud name
    - `apiKey`: Cloudinary API key

#### Direct Image Upload

- **POST /upload/image** - Upload an image directly through the backend
  - Authentication Required: Yes
  - Request: Multipart form data with an image file
  - Request Format: `multipart/form-data`
  - Response: JSON object with the following fields:
    - `success`: Boolean indicating if the upload was successful
    - `url`: The Cloudinary URL of the uploaded image
    - `public_id`: The Cloudinary public ID of the image
    - `format`: The image format
    - `width`: The image width
    - `height`: The image height
  - Status Codes:
    - 400: No file provided or file is not an image
    - 500: Upload failed (with error details)

## Data Models

### Event

```json
{
  "id": 1,
  "name": "Summer Festival",
  "venue_name": "Central Park",
  "address": "123 Park Avenue, New York, NY",
  "start_time": "2023-07-15T18:00:00",
  "end_time": "2023-07-15T23:00:00",
  "ticket_status": "Available",
  "ticket_link": "https://ticketsite.com/summer-festival",
  "lineup": ["DJ Cool", "The Band", "Famous Singer"],
  "genres": ["Electronic", "Rock", "Pop"],
  "description": "A fantastic summer festival with top artists",
  "poster_url": "https://res.cloudinary.com/dsjkhhpbl/image/upload/v1620000000/posters/summer-festival.jpg",
  "price": 49.99,
  "currency": "USD"
}
```

### EventCreate / EventUpdate

Same fields as Event, but without the `id` field. For EventUpdate, all fields are optional.

### Content

```json
{
  "id": 1,
  "key": "faq",
  "string_collection": ["Question 1?", "Answer 1", "Question 2?", "Answer 2"],
  "big_string": "Some large content text that needs to be displayed on the website."
}
```

### ContentCreate

Same fields as Content, but without the `id` field.

### ContentUpdate

```json
{
  "string_collection": ["Updated Question 1?", "Updated Answer 1"],
  "big_string": "Updated large content text."
}
```

All fields are optional in ContentUpdate.

## Notes

- The Event `ticket_status` field accepts the following values: "Available", "Sold Out", or "Sold At The Door"
- The Event `lineup` and `genres` fields are arrays of strings
- The Content `string_collection` field is an array of strings that can be used for various purposes like FAQs, bullet points, etc.
- The Content `big_string` field can be used for larger blocks of text like terms of service, about text, etc.

## Frontend Implementation Guide

This section provides guidance for frontend engineers on how to interact with the Azulu CRM API.

### Authentication Implementation

1. **Setting up Authentication:**

```javascript
// Create a utility file for API interactions (e.g., api.js)
const API_BASE_URL = 'https://azulucrm.fly.dev';
let adminPassword = null;

export const login = (password) => {
  adminPassword = password;
  // Optionally store in sessionStorage for persisting during the session
  sessionStorage.setItem('adminPassword', password);
};

export const logout = () => {
  adminPassword = null;
  sessionStorage.removeItem('adminPassword');
};

export const isLoggedIn = () => {
  if (!adminPassword && sessionStorage.getItem('adminPassword')) {
    adminPassword = sessionStorage.getItem('adminPassword');
  }
  return !!adminPassword;
};

// Helper function for making authenticated requests
export const fetchWithAuth = async (endpoint, options = {}) => {
  if (!isLoggedIn()) {
    throw new Error('Authentication required');
  }

  const defaultHeaders = {
    'Content-Type': 'application/json',
    'X-Admin-Password': adminPassword
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers
    }
  });

  // Handle 401 Unauthorized errors
  if (response.status === 401) {
    logout();
    throw new Error('Authentication failed');
  }

  return response;
};
```

2. **Create a Login Component:**

```jsx
import React, { useState } from 'react';
import { login } from './api';

function LoginForm({ onLoginSuccess }) {
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      // Set the password in the api utility
      login(password);
      
      // Test authentication with a simple request
      const response = await fetch('https://azulucrm.fly.dev/events', {
        headers: { 'X-Admin-Password': password }
      });
      
      if (response.ok) {
        onLoginSuccess();
      } else if (response.status === 401) {
        setError('Invalid password');
        logout();
      } else {
        setError('An error occurred');
      }
    } catch (err) {
      setError('Network error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Admin Login</h2>
      {error && <div className="error">{error}</div>}
      <div>
        <label>
          Password:
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>
      </div>
      <button type="submit" disabled={loading}>
        {loading ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
}

export default LoginForm;
```

### Image Upload Implementation

There are two ways to upload images to the Azulu CRM system:

#### Method 1: Direct Backend Upload (Recommended)

Using the new `/upload/image` endpoint is simpler and more reliable as it handles all Cloudinary interactions on the server:

```jsx
import React, { useState } from 'react';
import { fetchWithAuth } from './api';

function DirectImageUploader({ onUploadSuccess }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setUploadStatus('');
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    
    if (!selectedFile) {
      setUploadStatus('Please select a file to upload');
      return;
    }

    try {
      setIsUploading(true);
      setUploadStatus('Uploading image...');
      
      // Create form data
      const formData = new FormData();
      formData.append('file', selectedFile);
      
      // Upload to backend endpoint
      const response = await fetchWithAuth('/upload/image', {
        method: 'POST',
        headers: {
          // Don't set Content-Type here - it will be set automatically with the boundary
          'X-Admin-Password': sessionStorage.getItem('adminPassword')
        },
        body: formData
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Upload failed');
      }
      
      const result = await response.json();
      
      if (result.success) {
        setUploadStatus('Upload successful!');
        // Pass the image URL to the parent component
        onUploadSuccess(result.url);
      } else {
        setUploadStatus(`Upload failed: ${result.error || 'Unknown error'}`);
      }
    } catch (error) {
      setUploadStatus(`Error: ${error.message}`);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="image-uploader">
      <h3>Upload Event Poster</h3>
      <form onSubmit={handleUpload}>
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          disabled={isUploading}
        />
        <button type="submit" disabled={!selectedFile || isUploading}>
          {isUploading ? 'Uploading...' : 'Upload'}
        </button>
      </form>
      {uploadStatus && <p className={isUploading ? 'status' : 'success'}>{uploadStatus}</p>}
    </div>
  );
}

export default DirectImageUploader;
```

#### Method 2: Cloudinary Signature Approach (Alternative)

If you prefer to upload directly to Cloudinary from the frontend:

```javascript
import { fetchWithAuth } from './api';

export const getCloudinarySignature = async () => {
  const response = await fetchWithAuth('/cloudinary/signature');
  
  if (!response.ok) {
    throw new Error('Failed to get Cloudinary upload signature');
  }
  
  return response.json();
};
```

### Using the Image Uploader in an Event Form

```jsx
import React, { useState } from 'react';
import { fetchWithAuth } from './api';
import DirectImageUploader from './DirectImageUploader';

function EventForm() {
  const [eventData, setEventData] = useState({
    name: '',
    venue_name: '',
    address: '',
    start_time: '',
    end_time: '',
    ticket_status: 'Available',
    ticket_link: '',
    lineup: [],
    genres: [],
    description: '',
    poster_url: '',
    price: '',
    currency: 'USD'
  });
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setEventData({ ...eventData, [name]: value });
  };
  
  const handleArrayInput = (field, value) => {
    // Split comma-separated string into array
    setEventData({ ...eventData, [field]: value.split(',').map(item => item.trim()) });
  };
  
  const handleImageUploaded = (imageUrl) => {
    setEventData({ ...eventData, poster_url: imageUrl });
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const response = await fetchWithAuth('/events', {
        method: 'POST',
        body: JSON.stringify(eventData)
      });
      
      if (response.ok) {
        alert('Event created successfully!');
        // Reset form or redirect
      } else {
        const error = await response.json();
        alert(`Error: ${error.detail || 'Failed to create event'}`);
      }
    } catch (error) {
      alert(`Error: ${error.message}`);
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <h2>Create New Event</h2>
      
      <div className="form-group">
        <label>Event Name</label>
        <input
          type="text"
          name="name"
          value={eventData.name}
          onChange={handleChange}
          required
        />
      </div>
      
      {/* Add other form fields here */}
      
      <div className="form-group">
        <label>Event Poster</label>
        {eventData.poster_url ? (
          <div>
            <img
              src={eventData.poster_url}
              alt="Event poster preview"
              style={{ maxWidth: '200px' }}
            />
            <button type="button" onClick={() => handleImageUploaded('')}>
              Remove
            </button>
          </div>
        ) : (
          <DirectImageUploader onUploadSuccess={handleImageUploaded} />
        )}
      </div>
      
      <button type="submit">Create Event</button>
    </form>
  );
}

export default EventForm;
```

### CRUD Operations for Events

Here's how to implement basic CRUD operations for events:

1. **Fetch All Events:**

```javascript
import { API_BASE_URL } from './api';

export const fetchEvents = async (upcoming = false) => {
  const url = new URL(`${API_BASE_URL}/events`);
  
  if (upcoming) {
    url.searchParams.append('upcoming', 'true');
  }
  
  const response = await fetch(url);
  
  if (!response.ok) {
    throw new Error('Failed to fetch events');
  }
  
  return response.json();
};
```

2. **Fetch Single Event:**

```javascript
export const fetchEvent = async (eventId) => {
  const response = await fetch(`${API_BASE_URL}/events/${eventId}`);
  
  if (response.status === 404) {
    throw new Error('Event not found');
  }
  
  if (!response.ok) {
    throw new Error('Failed to fetch event');
  }
  
  return response.json();
};
```

3. **Create an EventList Component:**

```jsx
import React, { useEffect, useState } from 'react';
import { fetchEvents } from './api';

function EventList() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showUpcoming, setShowUpcoming] = useState(false);
  
  useEffect(() => {
    const loadEvents = async () => {
      try {
        setLoading(true);
        const data = await fetchEvents(showUpcoming);
        setEvents(data);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    
    loadEvents();
  }, [showUpcoming]);
  
  if (loading) return <div>Loading events...</div>;
  if (error) return <div>Error: {error}</div>;
  
  return (
    <div className="event-list">
      <div className="filters">
        <label>
          <input
            type="checkbox"
            checked={showUpcoming}
            onChange={(e) => setShowUpcoming(e.target.checked)}
          />
          Show upcoming events only
        </label>
      </div>
      
      {events.length === 0 ? (
        <p>No events found.</p>
      ) : (
        <div className="events-grid">
          {events.map(event => (
            <div key={event.id} className="event-card">
              {event.poster_url && (
                <img
                  src={event.poster_url}
                  alt={`Poster for ${event.name}`}
                  className="event-poster"
                />
              )}
              <h3>{event.name}</h3>
              <p className="event-venue">{event.venue_name}</p>
              <p className="event-date">
                {new Date(event.start_time).toLocaleDateString()}
              </p>
              <div className="event-status">{event.ticket_status}</div>
              <a href={`/events/${event.id}`}>View Details</a>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default EventList;
```

### CRUD Operations for Content

Content entries can be used to store dynamic text, FAQs, and other content for the website:

1. **Fetch Content by Key:**

```javascript
import { API_BASE_URL } from './api';

export const fetchContentByKey = async (key) => {
  try {
    const response = await fetch(`${API_BASE_URL}/content/${key}`);
    
    if (response.status === 404) {
      return null; // Content not found
    }
    
    if (!response.ok) {
      throw new Error(`Failed to fetch content: ${response.statusText}`);
    }
    
    return response.json();
  } catch (error) {
    console.error(`Error fetching content with key "${key}":`, error);
    throw error;
  }
};
```

2. **Create a DynamicContent Component:**

```jsx
import React, { useEffect, useState } from 'react';
import { fetchContentByKey } from './api';

function DynamicContent({ contentKey, fallbackText = 'Content not available' }) {
  const [content, setContent] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const loadContent = async () => {
      try {
        setLoading(true);
        const data = await fetchContentByKey(contentKey);
        setContent(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    
    loadContent();
  }, [contentKey]);
  
  if (loading) return <div>Loading...</div>;
  
  if (!content) return <div>{fallbackText}</div>;
  
  // Render string collection as a list if available
  if (content.string_collection && content.string_collection.length > 0) {
    return (
      <div className="dynamic-content">
        <ul>
          {content.string_collection.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
        {content.big_string && <div className="content-text">{content.big_string}</div>}
      </div>
    );
  }
  
  // Otherwise just render the big string
  return (
    <div className="dynamic-content">
      {content.big_string ? (
        <div className="content-text">{content.big_string}</div>
      ) : (
        <div>{fallbackText}</div>
      )}
    </div>
  );
}

export default DynamicContent;
```

3. **Using for Different Content Types:**

```jsx
// For About Us content
<DynamicContent contentKey="about" fallbackText="About Us content coming soon" />

// For FAQ content
<DynamicContent contentKey="faq" fallbackText="FAQs coming soon" />
```

### Best Practices for Frontend Implementation

1. **Error Handling:**
   - Implement consistent error handling across your application
   - Show user-friendly error messages
   - Log errors for debugging purposes

2. **Loading States:**
   - Always show loading indicators for asynchronous operations
   - Disable submit buttons during form submission
   - Consider skeleton loaders for lists and detailed content

3. **Data Validation:**
   - Validate form inputs before submitting to the API
   - Match the API's field requirements and constraints
   - Provide clear validation feedback to users

4. **Responsive Design:**
   - Ensure the frontend works well on mobile, tablet, and desktop screens
   - Use responsive image loading for events with the Cloudinary URL parameters
   - Optimize the admin interface for both desktop and mobile usage

5. **Performance:**
   - Implement pagination for event lists
   - Use the `upcoming` filter for showing relevant events
   - Consider caching frequently accessed content

6. **Testing:**
   - Test the API integration thoroughly
   - Verify error states and edge cases
   - Test the image upload flow with various file types and sizes 