# Day 12 Lab - Mission Answers

## Part 1: Localhost vs Production

### Exercise 1.1: Anti-patterns found
1. **Hardcoded Secrets**: The API key (`OPENAI_API_KEY`) and Database URL (`DATABASE_URL`) are hardcoded directly in `app.py` (lines 17-18). This is a major security risk as these secrets can be leaked via version control.
2. **Lack of Configuration Management**: Variables like `DEBUG` and `MAX_TOKENS` are hardcoded (lines 21-22). Production apps should use environment variables to allow different configurations without code changes.
3. **Inappropriate Logging**: The code uses `print()` for debugging (lines 33, 34, 38, 48). In production, structured JSON logging should be used to allow efficient log aggregation and parsing.
4. **No Health Check Endpoints**: The application lacks `/health` or `/ready` endpoints. Without these, container orchestrators cannot determine if the service is running correctly or when to restart it.
5. **Fixed Networking Configuration**: The host is set to `localhost` and the port is hardcoded to `8000` (lines 51-52). Production services must listen on `0.0.0.0` and should respect the `PORT` environment variable injected by the cloud provider.

### Exercise 1.3: Comparison table
| Feature | Basic (Develop) | Advanced (Production) | Why Important? |
|---------|---------|------------|----------------|
| Config  | Hardcoded in source code | Loaded from Environment Variables via Pydantic/`os.getenv` | Decouples configuration from code; prevents secret leaks in Git. |
| Health check | None | `/health` (Liveness) and `/ready` (Readiness) | Allows orchestrators like Kubernetes or Railway to monitor application health and manage traffic. |
| Logging | `print()` (Stdout) | Structured JSON Logging (`logging` module) | Enables automated log collection and analysis in platforms like Datadog or ELK. |
| Shutdown | Abrupt kill | Graceful shutdown (`SIGTERM` handling) | Ensures that active requests are completed before the process exits, preventing data loss or client errors. |

## Part 2: Docker

### Exercise 2.1: Dockerfile questions
1. **Base image**: `python:3.11` (Line 8). It's a full Python environment (~1GB).
2. **Working directory**: `/app` (Line 11).
3. **Why copy requirements.txt first?**: To take advantage of Docker layer caching. If the dependencies haven't changed, Docker reuses the cached layer and skips the `pip install` step, significantly speeding up builds.
4. **CMD vs ENTRYPOINT**: `CMD` provides default commands or arguments for the container which can be overridden at runtime. `ENTRYPOINT` sets the base command that always runs; any arguments passed to the container are appended to it.

### Exercise 2.3: Image size comparison
- **Develop (Single-stage)**: ~1 GB (based on `python:3.11`).
- **Production (Multi-stage)**: ~150-200 MB (based on `python:3.11-slim`).
- **Difference**: ~80-85% reduction.
- **Why?**: The `slim` image excludes many build tools and documentation files. Multi-stage builds only copy the final binaries/libraries needed to run, leaving behind the compilers and source files from the build stage.

### Exercise 2.4: Architecture Notes
The architecture uses **Nginx** as a Load Balancer / Reverse Proxy. It distributes traffic to multiple **Agent** container replicas. The agents are **Stateless** because they store session history in a shared **Redis** instance. **Qdrant** is used as the Vector Database for high-performance RAG operations.

## Part 4: API Security

### Exercise 4.1-4.3: Test results
- **No Key Provided**: Returns `401 Unauthorized`.
- **Invalid Key**: Returns `403 Forbidden`.
- **Rate Limit Exceeded**: Returns `429 Too Many Requests`.
- **JWT Authentication**: Token is requested via `/token` and must be provided in the `Authorization: Bearer <token>` header.

### Exercise 4.4: Cost guard implementation
Implemented a simple middleware or dependency that tracks token usage per request. It compares the total consumption against a `DAILY_BUDGET_USD` setting. Once the budget is reached, further requests are blocked with a `503 Service Unavailable` status until the counter resets (typically at midnight).

## Part 5: Scaling & Reliability

### Exercise 5.1-5.5: Implementation notes
- **Ready/Health probes**: `/health` checks if the process is alive; `/ready` checks if Redis and Qdrant connections are functional.
- **Graceful Shutdown**: Added handling for `SIGTERM` signals to allow FastAPI to stop accepting new requests and finish processing existing ones (30s timeout recommended).
- **Statelessness**: Refactored the conversation history logic to move memory out of local variables into Redis `lpush`/`lrange` operations.
