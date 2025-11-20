{
  "info": {
    "name": "Messaging App - Basic API",
    "description": "Collection for testing JWT auth, conversations and messages.",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
    "version": "1.0.0"
  },
  "variable": [
    { "key": "base_url", "value": "http://localhost:8000/messaging" },
    { "key": "username", "value": "user1" },
    { "key": "password", "value": "password123" },
    { "key": "access_token", "value": "" },
    { "key": "refresh_token", "value": "" },
    { "key": "conversation_id", "value": "" }
  ],
  "item": [
    {
      "name": "Obtain Token",
      "event": [
        {
          "listen": "test",
          "script": {
            "type": "text/javascript",
            "exec": [
              "pm.test('Status code is 200', function () { pm.response.to.have.status(200); });",
              "var json = pm.response.json();",
              "if (json.access) { pm.collectionVariables.set('access_token', json.access); }",
              "if (json.refresh) { pm.collectionVariables.set('refresh_token', json.refresh); }"
            ]
          }
        }
      ],
      "request": {
        "method": "POST",
        "header": [
          { "key": "Content-Type", "value": "application/json" }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\"username\": \"{{username}}\", \"password\": \"{{password}}\"}"
        },
        "url": {
          "raw": "{{base_url}}/api/token/",
          "host": ["{{base_url}}"],
          "path": ["api", "token", ""]
        }
      },
      "response": []
    },
    {
      "name": "Refresh Token",
      "event": [
        {
          "listen": "test",
          "script": {
            "type": "text/javascript",
            "exec": [
              "pm.test('Status code is 200', function () { pm.response.to.have.status(200); });",
              "var json = pm.response.json();",
              "if (json.access) { pm.collectionVariables.set('access_token', json.access); }"
            ]
          }
        }
      ],
      "request": {
        "method": "POST",
        "header": [
          { "key": "Content-Type", "value": "application/json" }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\"refresh\": \"{{refresh_token}}\"}"
        },
        "url": {
          "raw": "{{base_url}}/api/token/refresh/",
          "host": ["{{base_url}}"],
          "path": ["api", "token", "refresh", ""]
        }
      },
      "response": []
    },
    {
      "name": "Create Conversation",
      "event": [
        {
          "listen": "test",
          "script": {
            "type": "text/javascript",
            "exec": [
              "pm.test('Status code is 201 or 200', function () { pm.expect(pm.response.code).to.be.oneOf([200,201]); });",
              "var json = pm.response.json();",
              "if (json.id) { pm.collectionVariables.set('conversation_id', json.id); } else if (json.pk) { pm.collectionVariables.set('conversation_id', json.pk); }"
            ]
          }
        }
      ],
      "request": {
        "method": "POST",
        "header": [
          { "key": "Content-Type", "value": "application/json" },
          { "key": "Authorization", "value": "Bearer {{access_token}}" }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\"title\": \"Test Conversation\", \"participants\": [1,2]}"
        },
        "url": {
          "raw": "{{base_url}}/api/conversations/",
          "host": ["{{base_url}}"],
          "path": ["api", "conversations", ""]
        }
      },
      "response": []
    },
    {
      "name": "Send Message",
      "request": {
        "method": "POST",
        "header": [
          { "key": "Content-Type", "value": "application/json" },
          { "key": "Authorization", "value": "Bearer {{access_token}}" }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\"conversation\": {{conversation_id}}, \"content\": \"Hello from Postman\"}"
        },
        "url": {
          "raw": "{{base_url}}/api/messages/",
          "host": ["{{base_url}}"],
          "path": ["api", "messages", ""]
        }
      },
      "response": []
    },
    {
      "name": "List Messages (by conversation)",
      "request": {
        "method": "GET",
        "header": [
          { "key": "Authorization", "value": "Bearer {{access_token}}" }
        ],
        "url": {
          "raw": "{{base_url}}/api/messages/?conversation_id={{conversation_id}}",
          "host": ["{{base_url}}"],
          "path": ["api", "messages", ""],
          "query": [
            { "key": "conversation_id", "value": "{{conversation_id}}" }
          ]
        }
      },
      "response": []
    }
  ]
}
