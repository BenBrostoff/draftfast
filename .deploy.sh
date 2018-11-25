echo "You are about to update to version ${1}. Please confirm upgrade with Y."

read confirmation
if [ $confirmation != "Y" ]
then
    echo No confirmation, exiting.
    exit
fi

python setup.py sdist
twine upload "dist/draftfast-${1}.tar.gz"
