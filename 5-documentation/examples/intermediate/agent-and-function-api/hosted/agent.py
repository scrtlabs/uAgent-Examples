import requests
from ai_engine import UAgentResponse, UAgentResponseType
from uagents import Context, Model, Protocol


class Coordinates(Model):
    location: str


location_protocol = Protocol("Location Coordinates")


async def location_coordinates(latitude, longitude):
    url = "https://geocoding-by-api-ninjas.p.rapidapi.com/v1/reversegeocoding"
    querystring = {"lat": latitude, "lon": longitude}

    headers = {
        "X-RapidAPI-Key": "YOUR_API_KEY",
        "X-RapidAPI-Host": "geocoding-by-api-ninjas.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring, timeout=5)

    data = response.json()[0]["name"]

    return data


@location_protocol.on_message(model=Coordinates, replies=UAgentResponse)
async def location_coordinates_calculator(ctx: Context, sender: str, msg: Coordinates):
    ctx.logger.info(msg.location)
    latitude, longitude = map(str.strip, msg.location.split(","))
    city = location_coordinates(latitude, longitude)
    ctx.logger.info(city)
    message = city
    await ctx.send(
        sender, UAgentResponse(message=message, type=UAgentResponseType.FINAL)
    )


agent.include(location_protocol)
