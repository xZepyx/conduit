### Core Overview
The main purpose of this code is to interact with the OpenRouter AI API to generate chat completions using various models. The code is written in **Python**, utilizing the **httpx** library for asynchronous HTTP requests and **json** for data serialization. The architecture follows a simple, stateless design pattern, where each function handles a specific task without maintaining any internal state.

### Detailed Breakdown
#### Major Components and Their Purposes
1. **Model Mapping (`MODEL_MAP`)**: A dictionary that maps model names to their corresponding IDs.
2. **`stream_chat_completion` function**: Asynchronously streams chat completions for a given model and messages.
3. **`chat_completion` function**: Non-asynchronously fetches a single chat completion for a given model and messages.

#### Control Flow and Data Flow
- The `stream_chat_completion` function:
  - Maps the input model to its corresponding ID.
  - Constructs a payload with the mapped model, messages, and streaming flag.
  - Sends a POST request to the OpenRouter API with the payload.
  - Iterates over the response lines, parsing JSON data and yielding chat completion chunks.
- The `chat_completion` function:
  - Maps the input model to its corresponding ID.
  - Constructs a payload with the mapped model and messages.
  - Sends a POST request to the OpenRouter API with the payload.
  - Returns the response as JSON.

#### Important Functions, Classes, or Methods
- `async with httpx.AsyncClient()`: Establishes an asynchronous HTTP client session.
- `client.stream()` and `client.post()`: Send streaming and non-streaming POST requests, respectively.
- `response.aiter_lines()`: Iterates over the response lines asynchronously.

#### Key Variables and Data Structures
- `MODEL_MAP`: A dictionary mapping model names to IDs.
- `payload`: A dictionary containing the request data (model, messages, etc.).
- `headers`: A dictionary with the Authorization header and Content-Type.

#### Algorithms or Complex Logic
- The code uses asynchronous iteration to process the streaming response from the OpenRouter API.
- It uses JSON parsing to extract chat completion data from the response lines.

### Technical Implementation
#### Error Handling Patterns
- The code checks the response status code and raises an exception for non-200 status codes.
- It catches any exceptions that occur during JSON parsing and continues to the next iteration.

#### Important Logic Flows
- The `stream_chat_completion` function uses a streaming request to fetch chat completions in chunks.
- The `chat_completion` function uses a non-streaming request to fetch a single chat completion.

#### Performance Considerations
- The code uses asynchronous requests to improve performance.
- It sets a timeout of 120 seconds for non-streaming requests to avoid waiting indefinitely.

#### External Integrations or API Usage
- The code integrates with the OpenRouter AI API using HTTP requests.
- It uses the `httpx` library for asynchronous HTTP requests.

### Code Quality Notes
#### Best Practices Followed/Missed
- The code follows best practices by using asynchronous requests and handling errors.
- However, it misses some best practices by not providing detailed error messages and not validating the input model and messages.

#### Potential Optimizations
- The code can be optimized by adding input validation to handle invalid model names and messages.
- It can also be optimized by providing more detailed error messages to help with debugging.

#### Edge Cases to Consider
- The code should handle edge cases such as an invalid API key, network errors, and invalid response data.
- It should also handle cases where the response is too large or takes too long to process.