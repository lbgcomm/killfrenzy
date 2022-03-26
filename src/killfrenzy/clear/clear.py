import asyncio
from asgiref.sync import sync_to_async

from threading import Thread
import os
import datetime
import traceback

import time

class Clear(Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True

        self.started = False
        self.loop = None        

    def run(self):
        self.started = True
        asyncio.run(self.start_clear())

        print("Starting clear thread on PID #" + str(os.getpid()) + ".")

    @sync_to_async
    def get_pps(self):
        import connections.models as mdls
        return list(mdls.Port_Punch.objects.all().values('ip', 'port', 'service_ip', 'service_port', 'dest_ip', 'last_seen', 'created'))

    @sync_to_async
    def del_pp(self, ip, port, sip, sport, dip):
        import connections.models as mdls
        mdls.Port_Punch.objects.filter(ip=ip, port=port, service_ip=sip, service_port=sport, dest_ip=dip).delete()
    
    async def clear_items(self):
        while True:
            pps = await self.get_pps()

            for pp in pps:
                created = pp["created"].timestamp()
                now = time.time()

                if (created + 300) < now:
                    # Delete.
                    await self.del_pp(pp["ip"], pp["port"], pp["service_ip"], pp["service_port"], pp["dest_ip"])
                    await asyncio.sleep(1)
                    
            await asyncio.sleep(5)


    async def start_clear(self):
        self.loop = asyncio.get_event_loop()

        while True:
            task = asyncio.create_task(self.clear_items())

            try:
                tasks = await asyncio.gather(task)
            except Exception as e:
                print("[CLEAR] start_clear() :: At least one task failed at gather().")
                print(e)
                print(traceback.format_exc())
                pass

            await asyncio.sleep(30)
    
clear_c = Clear()