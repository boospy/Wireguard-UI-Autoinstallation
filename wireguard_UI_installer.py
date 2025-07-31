#!/usr/bin/env python3
"""
Wireguard-UI Docker Installation Script for Ubuntu 24.04 LTS
Automated installation with ncurses interface
AI-Generated
"""

import curses
import subprocess
import os
import sys
import socket
import time
import threading
from pathlib import Path
from typing import Dict, List, Tuple


class WireguardInstaller:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.current_step = 0
        self.total_steps = 7
        self.user_inputs = {}
        self.process_running = False
        self.spinner_chars = "|/-\\"
        self.spinner_index = 0

        # Initialize default ncurses colors
        curses.start_color()
        curses.use_default_colors()

    def clear_screen(self):
        """Clear the screen"""
        self.stdscr.clear()

    def draw_header(self):
        """Draw header with title and progress"""
        title = "Wireguard-UI Docker Installation"
        subtitle = f"Ubuntu 24.04 LTS - Step {self.current_step + 1}/{self.total_steps}"

        # Center title
        x = (self.width - len(title)) // 2
        self.stdscr.addstr(1, x, title, curses.A_BOLD)

        # Center subtitle
        x = (self.width - len(subtitle)) // 2
        self.stdscr.addstr(2, x, subtitle)

        # Separator line
        self.stdscr.addstr(3, 0, "=" * self.width)

    def draw_progress_bar(self, current: int, total: int):
        """Draw progress bar"""
        progress = current / total
        bar_width = self.width - 20
        filled_width = int(bar_width * progress)

        bar = "█" * filled_width + "░" * (bar_width - filled_width)
        percentage = f"{progress * 100:.1f}%"

        self.stdscr.addstr(self.height - 3, 5, f"Progress: [{bar}] {percentage}")

    def show_message(self, message: str, y_offset: int = 5, attr: int = 0):
        """Display message on screen"""
        lines = message.split('\n')
        for i, line in enumerate(lines):
            if y_offset + i < self.height - 4:
                self.stdscr.addstr(y_offset + i, 2, line, attr)

    def show_spinner(self, message: str, y_pos: int = None):
        """Show spinner animation during process execution"""
        if y_pos is None:
            y_pos = self.height // 2

        spinner_char = self.spinner_chars[self.spinner_index % len(self.spinner_chars)]
        spinner_msg = f"{spinner_char} {message} {spinner_char}"

        # Center the spinner message
        x = (self.width - len(spinner_msg)) // 2
        self.stdscr.addstr(y_pos, x, spinner_msg, curses.A_BOLD)
        self.stdscr.refresh()

        self.spinner_index += 1

    def spinner_thread(self, message: str):
        """Thread function for spinner animation"""
        while self.process_running:
            self.show_spinner(message)
            time.sleep(0.1)

    def get_user_input(self, prompt: str, default: str = "") -> str:
        """Get user input with prompt"""
        self.show_message(prompt, 5)
        if default:
            self.show_message(f"(Default: {default})", 7, curses.A_DIM)

        curses.echo()
        curses.curs_set(1)

        input_y = 9 if default else 7
        self.stdscr.addstr(input_y, 2, "Input: ")
        self.stdscr.refresh()

        try:
            user_input = self.stdscr.getstr(input_y, 9, 60).decode('utf-8').strip()
            return user_input if user_input else default
        except KeyboardInterrupt:
            return default
        finally:
            curses.noecho()
            curses.curs_set(0)

    def execute_command(self, command: str, description: str = "") -> bool:
        """Execute command with spinner animation"""
        self.process_running = True

        # Start spinner in separate thread
        spinner_thread = threading.Thread(target=self.spinner_thread, args=(description or "Processing...",))
        spinner_thread.daemon = True
        spinner_thread.start()

        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            self.process_running = False

            # Clear spinner area
            self.stdscr.addstr(self.height // 2, 0, " " * self.width)

            if result.returncode == 0:
                self.show_message(f"✓ {description or 'Command executed successfully'}", self.height // 2,
                                  curses.A_BOLD)
                return True
            else:
                self.show_message(f"✗ Error: {description or 'Command failed'}", self.height // 2, curses.A_BOLD)
                if result.stderr:
                    self.show_message(f"Details: {result.stderr[:100]}...", self.height // 2 + 1, curses.A_DIM)
                return False

        except Exception as e:
            self.process_running = False
            self.show_message(f"✗ Exception: {str(e)}", self.height // 2, curses.A_BOLD)
            return False

    def wait_for_key(self, message: str = "Press any key to continue..."):
        """Wait for key press"""
        self.show_message(message, self.height - 5, curses.A_REVERSE)
        self.stdscr.refresh()
        self.stdscr.getch()

    def get_hostname(self) -> str:
        """Get server FQDN"""
        try:
            result = subprocess.run(['hostname', '-f'], capture_output=True, text=True)
            return result.stdout.strip() if result.returncode == 0 else socket.getfqdn()
        except:
            return socket.getfqdn()

    def collect_all_inputs(self):
        """Collect all user inputs at the beginning"""
        self.clear_screen()
        self.draw_header()

        # Welcome message
        welcome_msg = """Welcome to Wireguard-UI Docker Installation!

This script will install and configure:
- Wireguard with Ubuntu native binary
- Wireguard-UI as Docker container
- Nginx reverse proxy with SSL/TLS
- Systemd services for automatic management

Let's start by collecting configuration information."""

        self.show_message(welcome_msg, 5)
        self.wait_for_key()

        # Collect Wireguard-UI credentials
        self.clear_screen()
        self.draw_header()
        self.show_message("Wireguard-UI Configuration", 5, curses.A_BOLD)

        self.user_inputs['wgui_username'] = self.get_user_input(
            "Enter username for Wireguard-UI:", "admin"
        )

        self.user_inputs['wgui_password'] = self.get_user_input(
            "Enter password for Wireguard-UI:", "admin"
        )

        # Collect SSL certificate paths
        self.clear_screen()
        self.draw_header()
        self.show_message("SSL/TLS Certificate Configuration", 5, curses.A_BOLD)

        default_cert = "/docker/appdata/certs/wireguard-UI"

        self.user_inputs['ssl_certificate'] = self.get_user_input(
            "Path to SSL certificate (.crt):", f"{default_cert}.crt"
        )

        self.user_inputs['ssl_certificate_key'] = self.get_user_input(
            "Path to SSL certificate key (.key):", f"{default_cert}.key"
        )

        self.user_inputs['ssl_trusted_certificate'] = self.get_user_input(
            "Path to trusted certificate (CA):", f"{default_cert}-ca.crt"
        )

        # Get hostname
        self.user_inputs['hostname'] = self.get_hostname()

        # Confirmation
        self.clear_screen()
        self.draw_header()

        config_summary = f"""Configuration Summary:

Wireguard-UI:
  Username: {self.user_inputs['wgui_username']}
  Password: {self.user_inputs['wgui_password']}

SSL Certificates:
  Certificate: {self.user_inputs['ssl_certificate']}
  Private Key: {self.user_inputs['ssl_certificate_key']}
  CA Certificate: {self.user_inputs['ssl_trusted_certificate']}

Server Hostname: {self.user_inputs['hostname']}

The installation will now begin. This may take several minutes.
"""

        self.show_message(config_summary, 5)
        self.wait_for_key("Press any key to start installation...")

    def install_packages(self):
        """Install required packages"""
        self.current_step = 1
        self.clear_screen()
        self.draw_header()
        self.draw_progress_bar(self.current_step, self.total_steps)

        if not self.execute_command("apt update", "Updating package lists"):
            return False

        if not self.execute_command("apt install nginx wireguard wireguard-tools docker-compose-v2 -y",
                                    "Installing packages"):
            return False

        self.wait_for_key()
        return True

    def setup_directories_and_forwarding(self):
        """Create directories and configure IP forwarding"""
        self.current_step = 2
        self.clear_screen()
        self.draw_header()
        self.draw_progress_bar(self.current_step, self.total_steps)

        if not self.execute_command("mkdir -p /docker/appdata/certs", "Creating directories"):
            return False

        if not self.execute_command("cp /etc/sysctl.conf /etc/sysctl.conf.backup", "Backing up sysctl.conf"):
            return False

        if not self.execute_command("sed -i 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/' /etc/sysctl.conf",
                                    "Enabling IP forwarding in config"):
            return False

        if not self.execute_command("sysctl -w net.ipv4.ip_forward=1", "Activating IP forwarding"):
            return False

        self.wait_for_key()
        return True

    def create_docker_compose(self):
        """Create Docker Compose file"""
        self.current_step = 3
        self.clear_screen()
        self.draw_header()
        self.draw_progress_bar(self.current_step, self.total_steps)

        docker_compose_content = f"""services:
  wireguard-ui:
    image: ngoduykhanh/wireguard-ui:latest
    restart: always
    container_name: wireguard-ui
    cap_add:
      - NET_ADMIN
    # required to show active clients. with this set, you don't need to expose the ui port (5000) anymore
    network_mode: host
    environment:
     # - SENDGRID_API_KEY
     # - EMAIL_FROM_ADDRESS
     # - EMAIL_FROM_NAME
     # - SESSION_SECRET
      - WGUI_USERNAME={self.user_inputs['wgui_username']}
      - WGUI_PASSWORD={self.user_inputs['wgui_password']}
      - WGUI_DNS=5.1.66.255,185.150.99.255
     # - WG_CONF_TEMPLATE
      - WGUI_MANAGE_START=false
      - WGUI_MANAGE_RESTART=true
     # - SMTP_HOSTNAME
     # - SMTP_PORT=465
     # - SMTP_USERNAME
     # - SMTP_PASSWORD
     # - SMTP_AUTH_TYPE=LOGIN
     # - SMTP_ENCRYPTION=SSLTLS
      - BIND_ADDRESS=127.0.0.1:5000
    logging:
      driver: json-file
      options:
        max-size: 50m
    volumes:
      - ./db:/app/db
      - /etc/wireguard:/etc/wireguard
"""

        self.process_running = True
        spinner_thread = threading.Thread(target=self.spinner_thread, args=("Creating Docker Compose file",))
        spinner_thread.daemon = True
        spinner_thread.start()

        try:
            with open('/docker/appdata/docker-compose.yml', 'w') as f:
                f.write(docker_compose_content)
            self.process_running = False
            self.show_message("✓ Docker Compose file created", self.height // 2, curses.A_BOLD)
        except Exception as e:
            self.process_running = False
            self.show_message(f"✗ Error creating Docker Compose file: {e}", self.height // 2, curses.A_BOLD)
            self.wait_for_key()
            return False

        self.wait_for_key()
        return True

    def start_services(self):
        """Start Docker container and configure systemd services"""
        self.current_step = 4
        self.clear_screen()
        self.draw_header()
        self.draw_progress_bar(self.current_step, self.total_steps)

        if not self.execute_command("cd /docker/appdata && docker compose up -d", "Starting Docker container"):
            return False

        # Create systemd service files
        service_content = """[Unit]
Description=Restart WireGuard
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/bin/systemctl restart wg-quick@wg0.service

[Install]
RequiredBy=wgui.path
"""

        path_content = """[Unit]
Description=Watch /etc/wireguard/wg0.conf for changes

[Path]
PathModified=/etc/wireguard/wg0.conf

[Install]
WantedBy=multi-user.target
"""

        self.process_running = True
        spinner_thread = threading.Thread(target=self.spinner_thread, args=("Creating systemd services",))
        spinner_thread.daemon = True
        spinner_thread.start()

        try:
            with open('/etc/systemd/system/wgui.service', 'w') as f:
                f.write(service_content)
            with open('/etc/systemd/system/wgui.path', 'w') as f:
                f.write(path_content)
            self.process_running = False
            self.show_message("✓ Systemd services created", self.height // 2, curses.A_BOLD)
        except Exception as e:
            self.process_running = False
            self.show_message(f"✗ Error creating systemd services: {e}", self.height // 2, curses.A_BOLD)
            self.wait_for_key()
            return False

        if not self.execute_command("systemctl enable wgui.path wgui.service", "Enabling systemd services"):
            return False

        if not self.execute_command("systemctl start wgui.path wgui.service", "Starting systemd services"):
            return False

        self.wait_for_key()
        return True

    def configure_nginx(self):
        """Configure Nginx reverse proxy"""
        self.current_step = 5
        self.clear_screen()
        self.draw_header()
        self.draw_progress_bar(self.current_step, self.total_steps)

        hostname = self.user_inputs['hostname']

        nginx_config = f"""map $http_upgrade $connection_upgrade {{
        default upgrade;
        ''      close;
}}

upstream {hostname} {{
        server 127.0.0.1:5000;
}}

server {{
        listen 80;
        server_name {hostname};
        access_log /var/log/nginx/vpn_access.log;
        error_log /var/log/nginx/vpn_error.log;
        return 301 https://{hostname}$request_uri;

}}

server {{
    listen 443 ssl;
    server_name {hostname};
    access_log /var/log/nginx/vpn_access.log;
    error_log /var/log/nginx/vpn_error.log;

    client_max_body_size 100M;

    # SSL
    ssl_certificate {self.user_inputs['ssl_certificate']};
    ssl_certificate_key {self.user_inputs['ssl_certificate_key']};
    ssl_trusted_certificate {self.user_inputs['ssl_trusted_certificate']};


    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;    
    add_header Strict-Transport-Security "max-age=63072000" always;

    ssl_session_timeout 1d;
    ssl_session_cache shared:MozSSL:10m;  # about 40000 sessions
    ssl_session_tickets off;

        location / {{
        proxy_set_header Host $http_host;
        proxy_pass http://{hostname};
        proxy_set_header X-Forwarded-Proto $scheme;
        }}



        location /websockify {{
                proxy_pass http://{hostname};
                proxy_set_header Host $http_host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;

                 }}


        }}
"""

        self.process_running = True
        spinner_thread = threading.Thread(target=self.spinner_thread, args=("Creating Nginx configuration",))
        spinner_thread.daemon = True
        spinner_thread.start()

        try:
            with open('/etc/nginx/sites-available/wireguard', 'w') as f:
                f.write(nginx_config)
            self.process_running = False
            self.show_message("✓ Nginx configuration created", self.height // 2, curses.A_BOLD)
        except Exception as e:
            self.process_running = False
            self.show_message(f"✗ Error creating Nginx configuration: {e}", self.height // 2, curses.A_BOLD)
            self.wait_for_key()
            return False

        if not self.execute_command("ln -sf /etc/nginx/sites-available/wireguard /etc/nginx/sites-enabled/",
                                    "Enabling Nginx site"):
            return False

        if not self.execute_command("nginx -t", "Testing Nginx configuration"):
            return False

        if not self.execute_command("systemctl enable nginx.service", "Enabling Nginx service"):
            return False

        if not self.execute_command("systemctl restart nginx.service", "Starting Nginx service"):
            return False

        self.wait_for_key()
        return True

    def show_completion_summary(self):
        """Show installation completion summary"""
        self.current_step = 6
        self.clear_screen()
        self.draw_header()
        self.draw_progress_bar(self.current_step + 1, self.total_steps)

        hostname = self.user_inputs['hostname']

        summary = f"""
Installation completed successfully!

Wireguard-UI is now available at:
- HTTP:  http://{hostname}
- HTTPS: https://{hostname}

Login credentials:
- Username: {self.user_inputs['wgui_username']}
- Password: {self.user_inputs['wgui_password']}

Important notes:
- Ensure SSL certificates are properly configured
- Wireguard configuration is automatically monitored
- Docker container runs in host network mode

Next steps:
1. Place SSL certificates in /docker/appdata/certs/
2. Restart Nginx: systemctl restart nginx
3. Access Wireguard-UI via browser and configure

Services status:
- Docker container: Running
- Nginx: Running
- Systemd monitoring: Active
"""

        self.show_message(summary, 5)
        self.wait_for_key("Press any key to exit...")

    def run_installation(self):
        """Main installation routine"""
        try:
            # Collect all inputs first
            self.collect_all_inputs()

            # Execute installation steps
            steps = [
                ("Installing packages", self.install_packages),
                ("Setting up directories and IP forwarding", self.setup_directories_and_forwarding),
                ("Creating Docker Compose configuration", self.create_docker_compose),
                ("Starting services", self.start_services),
                ("Configuring Nginx reverse proxy", self.configure_nginx),
                ("Completing installation", self.show_completion_summary)
            ]

            for step_name, step_func in steps:
                if not step_func():
                    self.show_message(f"Installation failed at: {step_name}", self.height - 5, curses.A_BOLD)
                    self.wait_for_key()
                    return False

            return True

        except KeyboardInterrupt:
            self.show_message("Installation cancelled by user.", self.height - 5, curses.A_BOLD)
            self.wait_for_key()
            return False
        except Exception as e:
            self.show_message(f"Unexpected error: {str(e)}", self.height - 5, curses.A_BOLD)
            self.wait_for_key()
            return False


def main(stdscr):
    """Main function"""
    # Hide cursor
    curses.curs_set(0)

    # Create and run installer
    installer = WireguardInstaller(stdscr)
    installer.run_installation()


if __name__ == "__main__":
    # Check for root privileges
    if os.geteuid() != 0:
        print("This script must be run as root!")
        print("Please use: sudo python3 wireguard_installer.py")
        sys.exit(1)

    # Start ncurses
    curses.wrapper(main)
