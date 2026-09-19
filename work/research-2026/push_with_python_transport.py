import sys,urllib.request,urllib.error,http.server,threading,subprocess,os
remote,token=sys.argv[1:3]
class Proxy(http.server.BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_GET(self):self.forward()
 def do_POST(self):self.forward()
 def forward(self):
  body=self.rfile.read(int(self.headers.get('Content-Length','0'))) if self.command=='POST' else None
  headers={k:v for k,v in self.headers.items() if k.lower() in ['content-type','accept','git-protocol','user-agent']};headers['Authorization']='Bearer '+token
  req=urllib.request.Request(remote.rstrip('/')+self.path, data=body,headers=headers,method=self.command)
  try:
   with urllib.request.urlopen(req,timeout=90) as res:status=res.status;data=res.read();typ=res.headers.get('Content-Type','application/octet-stream')
  except urllib.error.HTTPError as e:status=e.code;data=e.read();typ=e.headers.get('Content-Type','text/plain')
  except Exception as e:print('Upstream transport failure',self.command,len(body or b''),repr(e),flush=True);self.send_error(502,str(type(e).__name__));return
  self.send_response(status);self.send_header('Content-Type',typ);self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),Proxy);threading.Thread(target=s.serve_forever,daemon=True).start()
try:
 p=subprocess.run(['git','-c','http.postBuffer=524288000','push',f'http://127.0.0.1:{s.server_port}','HEAD:main'],cwd='lobbying-map',capture_output=True,text=True,timeout=120);print(p.stdout,p.stderr);sys.exit(p.returncode)
finally:s.shutdown();s.server_close()
