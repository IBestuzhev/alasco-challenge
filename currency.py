import os
from urllib.parse import urlencode

from aiohttp import web, ClientSession
from aiohttp_validate import validate
from aiohttp_swagger import setup_swagger


routes = web.RouteTableDef()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CURRENCIES = ['EUR', 'USD', 'JPY']
CURRENCY_SCHEMA = {
    "type": "string",
    "pattern": f"({'|'.join(CURRENCIES)})"
}
CURRENCY_REQUEST_SCHEMA = {
    "type": "object",
    "properties": {
        "from": CURRENCY_SCHEMA,
        "to": CURRENCY_SCHEMA,
        "amount": {
            "type": "number",
            "minimum": 0
        }
    },
    "required": ["from", "to", "amount"]
}
CURRENCY_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "result": {
            "type": "number"
        }
    }
}


@routes.view('/api/convert/')
class ConvertView(web.View):
    """Handle currency convert requests"""

    def build_api_url(self, from_currency: str, to_currency: str) -> str:
        """
        Build URL for https://exchangeratesapi.io/

        We download latest data only for 2 currencies that we convert
        """
        base_url = 'https://api.exchangeratesapi.io/latest'
        params = {
            'base': from_currency,
            'symbols': to_currency,
        }
        return f'{base_url}?{urlencode(params)}'

    async def convert(self, from_currency: str,
                      to_currency: str, amount: float) -> float:
        """
        Fetch latest exchange rate from https://exchangeratesapi.io/ and
        convert `amount` to new currency
        """
        url = self.build_api_url(from_currency, to_currency)
        async with ClientSession() as session:
            async with session.get(url) as resp:
                rate = await resp.json()
                rate = rate['rates'][to_currency]
        return amount * rate

    @validate(request_schema=CURRENCY_REQUEST_SCHEMA,
              response_schema=CURRENCY_RESPONSE_SCHEMA)
    async def post(self, req_body: dict, request: web.Request) -> web.Response:
        """
        Convert currency
        ---
        description: Convert currency from and to JPY/EUR/USD
        tags:
        - currency
        produces:
        - application/json
        parameters:
        - in: body
          name: body
          required: true
          description: Currency to convert
          schema:
            $ref: '#/definitions/CurrencyRequest'
        responses:
            "200":
                description: successful operation.
                schema:
                    $ref: '#/definitions/CurrencyResponse'
            "400":
                description: Invalid request
        """
        return {
            'result': await self.convert(
                from_currency=req_body['from'],
                to_currency=req_body['to'],
                amount=req_body['amount']
            )
        }


def index_response(request: web.Request) -> web.Response:
    """
    Response with `index.html`.

    In real project this will be handled by web-server.
    """
    return web.FileResponse(os.path.join(BASE_DIR, 'currency', 'index.html'))


def _get_app():

    app = web.Application()
    app.router.add_routes(routes)

    setup_swagger(
        app,
        definitions={
            'CurrencyRequest': CURRENCY_REQUEST_SCHEMA,
            'CurrencyResponse': CURRENCY_RESPONSE_SCHEMA
        }
    )

    # Normally this will be served by nginx or another web-server.
    app.router.add_get('/', index_response)
    app.router.add_static('/static/',
                          os.path.join(BASE_DIR, 'currency', 'static'),
                          show_index=True)

    return app


if __name__ == '__main__':
    app = _get_app()
    web.run_app(app, port=int(os.environ.get('PORT', 8080)))
