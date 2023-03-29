import asyncio

async def rr(cmd):
    proc = await asyncio.create_subprocess_shell(
                cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    print(stdout, stderr)
    return True

cmd = 'python3 web.py'
web = asyncio.run_coroutine_threadsafe(rr(cmd), asyncio.get_event_loop_policy().get_event_loop())
