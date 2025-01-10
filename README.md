# EvilBurp A Evilginx Phishlet Generator

A Burp Suite extension for automatically generating Evilginx phishlets for security testing and research.

## Features
- Automatic domain capture from browsed sites
- Authentication token detection from Set-Cookie headers
- Login form field identification
- Automatic phishlet generation in YAML format
- Direct save to Evilginx phishlets directory
- Burp Suite context menu integration

## Limitations
- No automatic subdomain detection
- Cannot handle JavaScript authentication
- Basic form field mapping only
- Limited cookie filtering capabilities
- Manual login path configuration required
- No multi-step authentication support
- Basic content replacement rules
- No custom header configuration
- Manual landing page setup required
- No SSL/TLS certificate management

## Requirements
- Burp Suite Professional
- Python 2.7 or Python 3.x
- Jython 2.7+ (for Burp Suite)
- PyYAML library
- Evilginx 3.0.0 or higher

## Setup
1. Install required dependencies:
```bash
pip install pyyaml
```

2. Configure Burp Suite Python Environment:
   - Go to Extender > Options
   - Set Python Environment to use Jython

3. Install the Extension:
   - Go to Extender > Extensions
   - Click "Add"
   - Select Python as Extension Type
   - Select the phishlet_generator.py file
   - Click "Next"

4. Configure Phishlet Path:
   - Modify `self.phishlet_path` in the code to match your Evilginx installation
   - Default path: `~/evilginx/phishlets/`

## Usage
1. Browse target website through Burp Suite proxy
2. Navigate login forms and authentication flows
3. Right-click anywhere in Burp Suite
4. Select "Generate & Save Evilginx Phishlet"
5. Phishlet will be saved to configured directory

## Security Notice
This tool is for authorized security testing and research only. Always obtain proper permissions before testing.

## Contributing
Pull requests are welcome. Please ensure updates maintain core functionality.

