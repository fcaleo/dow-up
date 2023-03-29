from flask import Flask, request
# import asyncio

# async def rr(cmd):
#     proc = await asyncio.create_subprocess_shell(
#                 cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
#     stdout, stderr = await proc.communicate()
#     print(stdout, stderr)

# cmd = 'python bot.py'
# asyncio.get_event_loop_policy().get_event_loop().run_until_complete(rr(cmd))


app = Flask(__name__)

@app.route('/')
def textdbserver():
        return 'Server Online'

app.run(host='0.0.0.0', port=9865, debug=True)
