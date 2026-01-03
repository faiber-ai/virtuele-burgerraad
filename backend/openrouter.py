"""OpenRouter API client for Virtuele Burgerraad."""

import asyncio
import httpx
import re
import logging
from typing import List, Dict, Any, Optional

from .config import (
    OPENROUTER_API_KEY,
    OPENROUTER_API_URL,
    PERSONA_MODEL,
    PERSONAS,
    get_persona_system_prompt,
)

logger = logging.getLogger(__name__)


async def query_openrouter(
    prompt: str,
    system_prompt: str,
    model: str,
    timeout: float = 60.0,
    max_retries: int = 3,
) -> Dict[str, Any]:
    """
    Query OpenRouter API with retry logic and exponential backoff.

    Args:
        prompt: User prompt to send
        system_prompt: System prompt for the model
        model: OpenRouter model identifier
        timeout: Request timeout in seconds
        max_retries: Maximum number of retry attempts

    Returns:
        Response dict with 'content', 'sentiment_score', and 'error' flag
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://virtuele-burgerraad.faiber.ai",
        "X-Title": "Virtuele Burgerraad",
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    }

    last_error = None

    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    OPENROUTER_API_URL,
                    headers=headers,
                    json=payload,
                )

                # Check for rate limiting or server errors (retry these)
                if response.status_code == 429 or response.status_code >= 500:
                    last_error = f"HTTP {response.status_code}"
                    if attempt < max_retries - 1:
                        wait_time = 2**attempt  # 1s, 2s, 4s
                        logger.warning(
                            f"Retry {attempt + 1}/{max_retries} after {wait_time}s: {last_error}"
                        )
                        await asyncio.sleep(wait_time)
                        continue

                response.raise_for_status()

                data = response.json()
                content = data["choices"][0]["message"]["content"]

                # Extract sentiment score
                sentiment_score = extract_sentiment_score(content)

                return {
                    "content": content,
                    "sentiment_score": sentiment_score,
                    "error": False,
                }

        except httpx.TimeoutException as e:
            last_error = f"Timeout: {e}"
            logger.warning(f"Attempt {attempt + 1}/{max_retries} timeout: {e}")

        except httpx.HTTPStatusError as e:
            last_error = f"HTTP error: {e}"
            # Don't retry on 4xx client errors (except 429)
            if 400 <= e.response.status_code < 500 and e.response.status_code != 429:
                logger.error(f"Client error, not retrying: {e}")
                break
            logger.warning(f"Attempt {attempt + 1}/{max_retries} failed: {e}")

        except Exception as e:
            last_error = str(e)
            logger.warning(f"Attempt {attempt + 1}/{max_retries} error: {e}")

        # Wait before retry (exponential backoff)
        if attempt < max_retries - 1:
            wait_time = 2**attempt
            await asyncio.sleep(wait_time)

    # All retries failed - return graceful degradation response
    logger.error(f"All {max_retries} attempts failed: {last_error}")
    return {
        "content": f"[Reactie kon niet worden opgehaald: {last_error}]",
        "sentiment_score": 0.0,
        "error": True,
    }


def extract_sentiment_score(content: str) -> float:
    """
    Extract sentiment score from model response.

    Looks for pattern: SENTIMENT_SCORE: [-1.0 to 1.0]

    Args:
        content: Model response text

    Returns:
        Float between -1.0 and 1.0, defaults to 0.0 if not found
    """
    pattern = r"SENTIMENT_SCORE:\s*([-]?\d*\.?\d+)"
    match = re.search(pattern, content, re.IGNORECASE)

    if match:
        try:
            score = float(match.group(1))
            # Clamp to valid range
            return max(-1.0, min(1.0, score))
        except ValueError:
            pass

    # Default to neutral if not found or invalid
    return 0.0


async def query_persona(
    persona: Dict[str, Any],
    policy_text: str,
) -> Dict[str, Any]:
    """
    Query a single persona for their reaction to policy text.

    Args:
        persona: Persona dict from PERSONAS list
        policy_text: The policy text to react to

    Returns:
        Dict with persona info and their reaction
    """
    system_prompt = get_persona_system_prompt(persona)

    result = await query_openrouter(
        prompt=policy_text,
        system_prompt=system_prompt,
        model=PERSONA_MODEL,
    )

    return {
        "persona_id": persona["id"],
        "name": persona["name"],
        "leeftijd": persona["leeftijd"],
        "profiel": persona["profiel"],
        "kernzorg": persona["kernzorg"],
        "reaction": result["content"],
        "sentiment_score": result["sentiment_score"],
        "error": result["error"],
    }


async def query_personas_parallel(policy_text: str) -> List[Dict[str, Any]]:
    """
    Query all 15 personas in parallel for their reactions.

    Args:
        policy_text: The policy text to analyze

    Returns:
        List of 15 persona reaction dicts
    """
    tasks = [query_persona(persona, policy_text) for persona in PERSONAS]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Handle any exceptions that slipped through
    processed_results = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            logger.error(f"Persona {PERSONAS[i]['name']} failed: {result}")
            processed_results.append(
                {
                    "persona_id": PERSONAS[i]["id"],
                    "name": PERSONAS[i]["name"],
                    "leeftijd": PERSONAS[i]["leeftijd"],
                    "profiel": PERSONAS[i]["profiel"],
                    "kernzorg": PERSONAS[i]["kernzorg"],
                    "reaction": f"[Fout: {str(result)}]",
                    "sentiment_score": 0.0,
                    "error": True,
                }
            )
        else:
            processed_results.append(result)

    return processed_results


# Keep legacy function for backwards compatibility
async def query_model(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float = 120.0,
) -> Optional[Dict[str, Any]]:
    """
    Query a single model via OpenRouter API (legacy function).

    Args:
        model: OpenRouter model identifier
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds

    Returns:
        Response dict with 'content', or None if failed
    """
    if not messages:
        return None

    # Extract system and user prompts from messages
    system_prompt = ""
    user_prompt = ""
    for msg in messages:
        if msg["role"] == "system":
            system_prompt = msg["content"]
        elif msg["role"] == "user":
            user_prompt = msg["content"]

    result = await query_openrouter(
        prompt=user_prompt,
        system_prompt=system_prompt,
        model=model,
        timeout=timeout,
    )

    if result["error"]:
        return None

    return {
        "content": result["content"],
        "reasoning_details": None,
    }
