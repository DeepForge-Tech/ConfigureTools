sudo mv ~/Library/Containers/DeepForge/DeepForge-Toolset/Temp/com.DeepForge.UpdateManager.plist ~/Library/LaunchAgents/
sudo chown root:wheel ~/Library/LaunchAgents/com.DeepForge.UpdateManager.plist
sudo chmod 644 ~/Library/LaunchAgents/com.DeepForge.UpdateManager.plist
sudo launchctl bootstrap gui/501 ~/Library/LaunchAgents/com.DeepForge.UpdateManager.plist