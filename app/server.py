import asyncio
import os

from aiohttp import web

from app.models import db, WinningBond
from app.serializers import bond_history_serializer as bh_serializer
from app.queries import BIGGEST_WINNERS, MOST_TIMES_WON


def get_best_event_loop():
    try:
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except Exception:
        print('No support for UVLoop reverting base event loop')
    return asyncio.get_event_loop()


class WebApp:

    def __init__(self, host: str, port: int, conn: str):
        self.host = host
        self.port = port
        self.connection_string = conn
        self.loop = get_best_event_loop()
        self.db = None

    async def bond_history(self, request):
        bond_id = request.match_info['bond_id']
        bond_records = await WinningBond.query.where(WinningBond.bond == bond_id.upper()).gino.all()
        if bond_records:
            bh = bh_serializer(bond_records)
            return web.json_response(bh)
        return web.json_response({'message': 'this bond has never appeared in our records'})

    async def biggest_winners(self, request):
        result, bond_records = await db.status(BIGGEST_WINNERS)
        records = []
        for b in bond_records:
            records.append({'bond_number': b[0], 'total_won': b[1], 'times_won': b[2]})
        return web.json_response(records)

    async def most_times_won(self, request):
        result, bond_records = await db.status(MOST_TIMES_WON)
        records = []
        for b in bond_records:
            records.append({'bond_number': b[0], 'total_won': b[1], 'times_won': b[2]})
        return web.json_response(records)

    async def create_app(self, loop):
        self.db = await db.set_bind(self.connection_string)
        app = web.Application()
        app.router.add_get('/bond-history/{bond_id}', self.bond_history)
        app.router.add_get('/biggest-winners/', self.biggest_winners)
        app.router.add_get('/most-frequent-winners/', self.most_times_won)
        return app

    def run_server(self):
        loop = self.loop
        app = loop.run_until_complete(self.create_app(loop))
        web.run_app(app, host=self.host, port=self.port)
