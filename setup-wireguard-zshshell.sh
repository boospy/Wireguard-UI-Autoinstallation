#!/bin/bash

# ZSH Prompt Setup Script
# Automatisiert die Installation und Konfiguration einer benutzerdefinierten ZSH-Shell
# KI-Generated

set -e  # Script bei Fehlern beenden

echo "🚀 Starting ZSH Prompt Setup..."
echo "=================================="

# 1. Pakete installieren
echo "📦 Installing packages..."
apt update
apt install zsh eza -y

# 2. ZSH-Config von GitHub laden und installieren
echo "⬇️  Installing ZSH configuration from GitHub..."
bash <(curl -s https://raw.githubusercontent.com/mh-firouzjah/zsh-config/master/install.sh)

# 3. ZSH-Shell für Root aktivieren
echo "👤 Setting ZSH as default shell for root..."
usermod -s /bin/zsh root

# 4. MOTD-Datei erstellen
echo "📝 Creating welcome message..."
cat > /etc/update-motd.d/99-osit << 'EOF'
#!/bin/sh

green="\e[0;92m"
red="\e[31m"
bold="\e[1m"
reset="\e[0m"

echo
echo "${green} ----------------------------------------------"
echo " Welcome to the VPN dial-in server"
echo " ----------------------------------------------${reset}"
echo
echo
echo
EOF

# MOTD-Datei ausführbar machen
chmod +x /etc/update-motd.d/99-osit

# 5. P10k-Konfiguration kopieren und anpassen
echo "⚙️  Configuring Powerlevel10k..."
cp $HOME/.zsh/modules/p10k.zsh $HOME/.p10k.zsh

# Funktionen aktivieren (public_ip und vpn_ip einkommentieren)
sed -i 's/# *typeset -g POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS.*public_ip.*/  typeset -g POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS+=(public_ip)/' $HOME/.p10k.zsh
sed -i 's/# *typeset -g POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS.*vpn_ip.*/  typeset -g POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS+=(vpn_ip)/' $HOME/.p10k.zsh

# Alternativ: Direkte Suche und Aktivierung der Funktionen
sed -i '/public_ip/s/^[[:space:]]*#[[:space:]]*/  /' $HOME/.p10k.zsh
sed -i '/vpn_ip/s/^[[:space:]]*#[[:space:]]*/  /' $HOME/.p10k.zsh

# Hintergrundfarbe auf Rot setzen
sed -i 's/POWERLEVEL9K_DIR_BACKGROUND=.*/POWERLEVEL9K_DIR_BACKGROUND="1"/' $HOME/.p10k.zsh

# 6. Neue .zshrc erstellen
echo "📄 Creating new .zshrc configuration..."
rm -f ~/.zshrc

cat > ~/.zshrc << 'EOF'
# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.

echo
docker compose ls
echo
docker ps
echo


if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# Use powerline
USE_POWERLINE="true"
# Has weird character width
# Example:
#    is not a diamond
HAS_WIDECHARS="false"

source ~/.zsh/modules/config.zsh
source ~/.zsh/modules/prompt.zsh

# Remove folder background on `ls` command
zstyle ':completion:*' list-colors
export LS_COLORS="$LS_COLORS:ow=1;34:tw=1;34:"

alias ls='eza  --icons  --git'

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

cd /etc/wireguard
EOF

# Stylische Abschlussnachricht
echo
echo "✨ ================================================= ✨"
echo "🎉              INSTALLATION COMPLETE!              🎉"
echo "✨ ================================================= ✨"
echo
echo "🔥 Your awesome ZSH shell is now configured!"
echo "🚪 To activate the new ZSH shell, log in again."
echo
echo "📋 What was installed:"
echo "   • ZSH with custom prompt theme"
echo "   • EZA (modern ls replacement)"
echo "   • Custom welcome message"
echo "   • Powerlevel10k with public_ip & vpn_ip"
echo "   • Docker status display on login"
echo
echo "🎯 Ready to rock your terminal! 🚀"
echo
