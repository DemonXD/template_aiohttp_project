from aiohttp.web import json_response
from global_ import PublicManager


async def handle(request):
    # 获取get url 的参数
    # request.match_info.get('name', "Anonymous")
    PublicManager.logger.info("run handle handler")
    return json_response({
                    "code": 200,
                    "data": "pong"
                },
                status=200
            )
