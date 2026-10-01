"""Drive an Emu198x binary over MCP stdio: mcp.py BIN steps.json [extra args]"""
import json, subprocess, sys
binary, steps_path = sys.argv[1], sys.argv[2]
p = subprocess.Popen([binary, '--mcp', *sys.argv[3:]], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
n = 0
def call(method, params=None, notify=False):
    global n
    msg = {'jsonrpc': '2.0', 'method': method}
    if params is not None: msg['params'] = params
    if not notify:
        n += 1; msg['id'] = n
    p.stdin.write(json.dumps(msg) + '\n'); p.stdin.flush()
    if notify: return None
    while True:
        line = p.stdout.readline()
        if not line: raise SystemExit('server closed')
        r = json.loads(line)
        if r.get('id') == n: return r
call('initialize', {'protocolVersion': '2024-11-05', 'capabilities': {}, 'clientInfo': {'name': 'loadcap', 'version': '1'}})
call('notifications/initialized', notify=True)
steps = json.load(open(steps_path))
for s in steps:
    if s.get('tool') == '__list':
        r = call('tools/list')
        for t in r['result']['tools']: print(t['name'], json.dumps(t['inputSchema'].get('properties', {}))[:300])
        continue
    r = call('tools/call', {'name': s['tool'], 'arguments': s.get('args', {})})
    res = r.get('result') or r.get('error')
    txt = ''.join(c.get('text', '') for c in (res.get('content') or [])) if isinstance(res, dict) else str(res)
    print('>>', s['tool'], json.dumps(s.get('args', {}))[:120], '|', ('ERROR ' if (isinstance(res, dict) and res.get('isError')) or 'error' in r else '') + txt[:int(s.get("max",400))])
p.stdin.close(); p.wait(timeout=30)
