host=osmc
user=osmc
pluginName="script.service.jogwheel"
pluginFolder="~/.kodi/addons"
scp -r -p ./../../../../$pluginName $user@$host:$pluginFolder/$pluginName/
ssh $user@$host $pluginFolder/$pluginName/resources/scripts/local/install_dependencies.sh
