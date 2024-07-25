mkdir data
mkdir data\albums
mkdir logs

echo Backing up sample photo dump, incase if you update the exifs
xcopy .\sample\MyPhotoDump .\sample\MyPhotoDump_bu\ /e
