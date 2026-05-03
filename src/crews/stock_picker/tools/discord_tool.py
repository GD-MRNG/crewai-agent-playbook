from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import requests


class DiscordMessage(BaseModel):
    """A stock pick decision to be sent to the Discord channel"""
    company: str = Field(..., description="The name of the company selected for investment.")
    rationale: str = Field(..., description="One sentence explaining why this company was chosen.")


class DiscordNotificationTool(BaseTool):

    name: str = "Send a Discord Notification"
    description: str = (
        "Sends a stock pick decision to a Discord channel via webhook. "
        "Provide the chosen company name and a one-sentence rationale."
    )
    args_schema: Type[BaseModel] = DiscordMessage

    def _run(self, company: str, rationale: str) -> str:
        webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
        if not webhook_url:
            return '{"notification": "error", "reason": "DISCORD_WEBHOOK_URL not set"}'

        message = f"**Stock Pick: {company}**\n{rationale}"
        print(f"Discord: {message}")
        payload = {"content": message}
        response = requests.post(webhook_url, json=payload)
        if response.status_code in (200, 204):
            return '{"notification": "ok"}'
        return f'{{"notification": "error", "status": {response.status_code}}}'
