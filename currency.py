import os
from urllib.parse import urlencode

from aiohttp import web, ClientSession
from aiohttp_validate import validate


routes = web.RouteTableDef()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CURRENCIES = ['EUR', 'USD', 'JPY']
CURRENCY_SCHEMA = {
    "type": "string",
    "pattern": f"({'|'.join(CURRENCIES)})"
}


@routes.view('/api/convert/')
class ConvertView(web.View):
    # TODO: Add swagger
    # TODO: Add docstrings

    def build_api_url(self, from_currency: str, to_currency: str) -> str:
        base_url = 'https://api.exchangeratesapi.io/latest'
        params = {
            'base': from_currency,
            'symbols': to_currency,
        }
        return f'{base_url}?{urlencode(params)}'

    async def convert(self, from_currency: str,
                      to_currency: str, amount: float) -> float:
        url = self.build_api_url(from_currency, to_currency)
        async with ClientSession() as session:
            async with session.get(url) as resp:
                rate = await resp.json()
                rate = rate['rates'][to_currency]
        return amount * rate

    @validate(request_schema={
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
    })
    async def post(self, req_body: dict, request: web.Request) -> web.Response:
        return {
            'result': await self.convert(
                from_currency=req_body['from'],
                to_currency=req_body['to'],
                amount=req_body['amount']
            )
        }


def index_response(request):
    # TODO: Add note about frontend
    return web.FileResponse(os.path.join(BASE_DIR, 'currency', 'index.html'))


def _get_app():

    app = web.Application()
    app.router.add_routes(routes)

    app.router.add_get('/', index_response)
    app.router.add_static('/static/',
                          os.path.join(BASE_DIR, 'currency', 'static'),
                          show_index=True)

    return app


if __name__ == '__main__':
    app = _get_app()
    web.run_app(app, port=int(os.environ.get('PORT', 8080)))
